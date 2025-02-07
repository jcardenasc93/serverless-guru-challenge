from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from airline.routes.airlines import airline_router
from airline.config import app_settings
from common.errors import APIError, APIErrorException
from mangum import Mangum

app = FastAPI(title="Airlines API")


@app.exception_handler(APIErrorException)
async def api_exception_handler(_, exc: APIErrorException) -> JSONResponse:
    error_response = APIError(detail=exc.detail, error_type=exc.error_type)
    return JSONResponse(
        status_code=exc.status_code, content=error_response.model_dump()
    )


@app.exception_handler(RequestValidationError)
async def api_exception_handler(_, exc: RequestValidationError) -> JSONResponse:
    error_response = APIError(
        detail=exc.errors(), error_type=RequestValidationError.__name__
    )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content=error_response.model_dump()
    )


app.include_router(airline_router, prefix="/airlines/api/v1")

handler = Mangum(app)
