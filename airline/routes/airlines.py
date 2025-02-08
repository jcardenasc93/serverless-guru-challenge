from uuid import UUID
from fastapi import status
from fastapi import APIRouter
from airline.db import airline_table
from airline.responses import AirlineResponse
from airline.schemas import AirlineCreateRequest, AirlineUpdateRequest
from common.errors import APIErrorException


airline_router = APIRouter(tags=["airlines"])


@airline_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_airline(request: AirlineCreateRequest) -> AirlineResponse:
    try:
        new_airline = airline_table.create_airline(data=request)
    except Exception as e:
        raise APIErrorException(
            detail=f"Error from data source: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return AirlineResponse(data=new_airline)


@airline_router.get("/")
async def fetch_airlines() -> AirlineResponse:
    try:
        airlines = airline_table.fetch_airlines()
    except Exception as e:
        raise APIErrorException(
            detail=f"Error from data source: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return AirlineResponse(data=airlines)


@airline_router.get("/{airline_uuid}")
async def fetch_airline_by_uuid(airline_uuid: UUID) -> AirlineResponse:
    try:
        airline = airline_table.fetch_airline_by_uuid(airline_uuid)
    except Exception as e:
        raise APIErrorException(
            detail=f"Error from data source: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if airline is None:
        raise APIErrorException(
            detail="No airline found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return AirlineResponse(data=airline)


@airline_router.put("/{airline_uuid}")
async def update_airline(
    airline_uuid: UUID, request: AirlineUpdateRequest
) -> AirlineResponse:
    try:
        airline = airline_table.update_airline(airline_uuid=airline_uuid, data=request)
    except Exception as e:
        raise APIErrorException(
            detail=f"Error from data source: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return AirlineResponse(data=airline)
