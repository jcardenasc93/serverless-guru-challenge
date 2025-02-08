from fastapi import status
from fastapi import APIRouter
from destination.db import destination_table
from destination.responses import DestinationResponse
from destination.schemas import DestinationCreateRequest
from common.errors import APIErrorException


destination_router = APIRouter(tags=["destinations"])


@destination_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_destination(request: DestinationCreateRequest) -> DestinationResponse:
    try:
        new_destination = destination_table.create_destination(data=request)
    except Exception as e:
        raise APIErrorException(
            detail=f"Error from data source: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return DestinationResponse(data=new_destination)
