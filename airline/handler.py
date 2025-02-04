from mangum import Mangum

from airline.app import app


# Wraps FastAPI app with Mangum for AWS Lambda
handler = Mangum(app)
