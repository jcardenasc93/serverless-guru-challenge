from uuid import UUID
from fastapi import status
from fastapi import APIRouter
from starlette.status import HTTP_400_BAD_REQUEST
from destination.db import destination_table
from destination.responses import DestinationResponse
from destination.schemas import DestinationCreateRequest
from common.errors import APIErrorException
from destination.services.airlines_service import AirlinesService


destination_router = APIRouter(tags=["destinations"])


@destination_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_destination(request: DestinationCreateRequest) -> DestinationResponse:
    airline_uuid = request.airline_uuid
    try:
        is_valid_airline = AirlinesService().check_airline(airline_uuid)
    except Exception as e:
        raise APIErrorException(
            detail=f"Error from external services: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    if is_valid_airline is False:
        raise APIErrorException(
            detail=f"Not valid airline found for {airline_uuid=}",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    try:
        new_destination = destination_table.create_destination(data=request)
    except Exception as e:
        raise APIErrorException(
            detail=f"Error from data source: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return DestinationResponse(data=new_destination)


@destination_router.get("/")
async def fetch_airline_destinations(
    airline_uuid: UUID = None,
) -> DestinationResponse:
    destinations = []
    if airline_uuid is None:
        try:
            destinations = destination_table.fetch_destinations()
        except Exception as e:
            raise APIErrorException(
                detail=f"Error from data source: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    else:
        try:
            is_valid_airline = AirlinesService().check_airline(str(airline_uuid))
        except Exception as e:
            raise APIErrorException(
                detail=f"Error from external services: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        if is_valid_airline is False:
            raise APIErrorException(
                detail=f"Not valid airline found for {airline_uuid=}",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            destinations = destination_table.fetch_airline_destinations(airline_uuid)
        except Exception as e:
            raise APIErrorException(
                detail=f"Error from data source: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return DestinationResponse(data=destinations)


@destination_router.get("/{destination_uuid}")
async def fetch_destination_by_uuid(destination_uuid: UUID) -> DestinationResponse:
    try:
        destination = destination_table.fetch_destination_by_uuid(destination_uuid)
    except Exception as e:
        raise APIErrorException(
            detail=f"Error from data source: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    if destination is None:
        raise APIErrorException(
            detail="No destination found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return DestinationResponse(data=destination)
