from destination.schemas import DestinationRead
from common.responses import BaseResponse


class DestinationResponse(BaseResponse):
    data: DestinationRead | list[DestinationRead] | None
