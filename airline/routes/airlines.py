from uuid import UUID
from fastapi import Response, status
from fastapi import APIRouter
from airline.db import airline_table
from airline.responses import AirlineResponse
from airline.schemas import AirlineCreateRequest
from common.errors import APIErrorException


airline_router = APIRouter(prefix="/api/v1", tags=["airlines"])


@airline_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_airline(request: AirlineCreateRequest) -> AirlineResponse:
    try:
        new_airline = airline_table.create_airline(data=request)
    except Exception as e:
        raise APIErrorException(
            detail="Error from data source",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return AirlineResponse(data=new_airline)


@airline_router.get("/")
async def fetch_airlines() -> AirlineResponse:
    try:
        airlines = airline_table.fetch_airlines()
    except Exception as e:
        raise APIErrorException(
            detail="Error from data source",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return AirlineResponse(data=airlines)


@airline_router.get("/{airline_uuid}")
async def fetch_airline_by_uuid(
    airline_uuid: UUID, response: Response
) -> AirlineResponse:
    try:
        airline = airline_table.fetch_airline_by_uuid(airline_uuid)
    except Exception as e:
        raise APIErrorException(
            detail="Error from data source",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return AirlineResponse(data=airline)
