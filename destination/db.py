from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4
import boto3
from boto3.dynamodb.conditions import Key
import logging

from botocore.exceptions import ClientError
from destination.schemas import (
    DestinationCreateRequest,
    DestinationRead,
    DestinationUpdateRequest,
)
from destination.config import app_settings

logger = logging.getLogger(__name__)

TABLE_NAME = app_settings.DYNAMODB_DESTINATION_TABLE


class DestinationTable:
    """Wrapper for interact with destination table from dynamoDB"""

    def __init__(self, dynamodb_resource: Any) -> None:
        self._dyn_resource = dynamodb_resource
        self._table: Any = self._dyn_resource.Table(TABLE_NAME)

    def fetch_airline_destinations(self, airline_uuid: UUID) -> list[DestinationRead]:
        try:
            destinations = self._table.query(
                IndexName="airline-index",
                KeyConditionExpression=Key("airline_uuid").eq(str(airline_uuid)),
            )
        except ClientError as e:
            err = e.response
            msg = f"Couldn't fetch data from '{TABLE_NAME}' table. Details: {err['Error']['Message']}"
            logger.error(msg=msg)
            raise e

        return [DestinationRead(**airline) for airline in destinations]

    def fetch_destination_by_uuid(self, uuid: UUID) -> DestinationRead | None:
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
        return DestinationRead(**obj[0])

    def create_destination(self, data: DestinationCreateRequest) -> DestinationRead:
        destination_uuid = uuid4()
        now = datetime.now(tz=timezone.utc)
        destination_data = DestinationRead(
            uuid=str(destination_uuid),
            city=data.city,
            country=data.country,
            airline_uuid=data.airline_uuid,
            active=True,
            created_at=str(now),
            updated_at=str(now),
        )
        try:
            data_dict = destination_data.model_dump()
            data_dict["active"] = int(True)
            self._table.put_item(Item=data_dict)
        except ClientError as e:
            err = e.response
            logger.error(
                msg=f"Couldn't create new item on '{TABLE_NAME}' table. Details: {err['Error']['Message']}"
            )
            raise e
        except Exception as e:
            raise e

        return destination_data

    def update_destination(
        self, destination_uuid: UUID, data: DestinationUpdateRequest
    ) -> DestinationRead:
        now = datetime.now(tz=timezone.utc)

        update_expr_parts = []
        expr_attr_values = {}

        update_expr_parts.append("active = :a")
        expr_attr_values[":a"] = int(data.active)
        update_expr_parts.append("updated_at = :t")
        update_expr = "SET " + ", ".join(update_expr_parts)
        expr_attr_values[":t"] = str(now)

        try:
            response = self._table.update_item(
                Key={"uuid": str(destination_uuid)},
                UpdateExpression=update_expr,
                ExpressionAttributeValues=expr_attr_values,
                ReturnValues="ALL_NEW",
            )
        except ClientError as e:
            err = e.response
            logger.error(
                msg=f"Couldn't update item on '{TABLE_NAME}' table. Details: {err['Error']['Message']}"
            )
            raise e
        except Exception as e:
            raise e
        new_data = response["Attributes"]
        return DestinationRead(**new_data)


if app_settings.ENVIRONMENT != "local":
    destination_table = DestinationTable(
        dynamodb_resource=boto3.resource(
            "dynamodb", region_name=app_settings.AWS_REGION
        )
    )
else:
    destination_table = DestinationTable(
        dynamodb_resource=boto3.resource(
            "dynamodb",
            region_name="us-east-1",
            endpoint_url="http://localhost:4566",
            aws_access_key_id="dummy-access-key",
            aws_secret_access_key="dummy-secret-key",
        )
    )
