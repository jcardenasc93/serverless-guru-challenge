from airline.schemas import AirlineRead
from common.responses import BaseResponse


class AirlineResponse(BaseResponse):
    data: AirlineRead | list[AirlineRead] | None
