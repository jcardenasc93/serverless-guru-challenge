from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4
import boto3
from boto3.dynamodb.conditions import Key
import logging

from botocore.exceptions import ClientError
from airline.schemas import AirlineCreateRequest, AirlineRead
from airline.config import app_settings

logger = logging.getLogger(__name__)

TABLE_NAME = app_settings.DYNAMODB_AIRLINE_TABLE


class AirlineTable:
    """Wrapper for interact with airline table from dynamoDB"""

    def __init__(self, dynamodb_resource: Any) -> None:
        self._dyn_resource = dynamodb_resource
        self._table: Any = self._dyn_resource.Table(TABLE_NAME)

    def fetch_airlines(self) -> list[AirlineRead]:
        try:
            airlines = self._table.scan()["Items"]
        except ClientError as e:
            err = e.response
            msg = f"Couldn't fetch data from '{TABLE_NAME}' table. Details: {err['Error']['Message']}"
            logger.error(msg=msg)
            raise e

        return [AirlineRead(**airline) for airline in airlines]

    def fetch_airline_by_uuid(self, uuid: UUID) -> AirlineRead | None:
        try:
            response = self._table.query(
                KeyConditionExpression=Key("uuid").eq(str(uuid)),
            )
        except ClientError as e:
            err = e.response
            logger.error(
                msg=f"Couldn't fetch data for {uuid=} from '{TABLE_NAME}' table. Details: {err['Error']['Message']}"
            )
            raise e

        obj = response.get("Items", [])
        if not obj:
            return None
        return AirlineRead(**obj[0])

    def create_airline(self, data: AirlineCreateRequest) -> AirlineRead:
        airline_uuid = uuid4()
        now = datetime.now(tz=timezone.utc)
        airline_data = AirlineRead(
            name=data.name,
            country=data.country,
            uuid=str(airline_uuid),
            created_at=str(now),
            updated_at=str(now),
        )
        try:
            data_dict = airline_data.model_dump()
            self._table.put_item(Item=data_dict)
        except ClientError as e:
            err = e.response
            logger.error(
                msg=f"Couldn't create new item on '{TABLE_NAME}' table. Details: {err['Error']['Message']}"
            )
            raise e
        except Exception as e:
            raise e

        return airline_data


if app_settings.ENVIRONMENT != "local":
    airline_table = AirlineTable(
        dynamodb_resource=boto3.resource(
            "dynamodb", region_name=app_settings.AWS_REGION
        )
    )
else:
    airline_table = AirlineTable(
        dynamodb_resource=boto3.resource(
            "dynamodb",
            region_name="us-east-1",
            endpoint_url="http://localhost:4566",
            aws_access_key_id="dummy-access-key",
            aws_secret_access_key="dummy-secret-key",
        )
    )
