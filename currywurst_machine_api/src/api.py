import os

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .custom_exceptions import (InsuficientInsertedMoneyException,
                                NotExactChangeAvailableException)
from .machine import CurrywurstMachine
from .payloads import Payment
from .redis_publisher import RedisPublisher

app = FastAPI()
cw_machine = CurrywurstMachine()
redis_publisher = RedisPublisher(redis_host=os.getenv("REDIS_SERVICE", "redis"))
machine_id = (
    123456  # Can come from other place. But will keep here for sake of simplicity
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handles RequestValidationError exceptions that occur in the payload of the request.

    Args:
    request (Request): The FastAPI request object.
    exc (RequestValidationError): The RequestValidationError that occurred.

    Returns:
    JSONResponse: A JSON response object containing the error message and relevant details.
    """
    error_msg_cascade = ""
    for i, error in enumerate(exc.errors()):
        error_msg_cascade += error["msg"]
        if i + 1 != len(exc.errors()):
            error_msg_cascade += "\n"
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "machine_id": machine_id,
            "status": "failed",
            "returned_coins": None,  # exc.body["eur_inserted"],
            "error_msg": error_msg_cascade,
        },
    )


@app.post("/refill-coins")
async def refill_coins() -> JSONResponse:
    """Refills the coins in the Currywurst Machine.

    Returns:
    JSONResponse: A JSON response object containing a message indicating that the coin reservoir is full.
    """
    cw_machine.refill_coins()
    return JSONResponse(content={"Reservatory": "Full"}, status_code=status.HTTP_200_OK)


@app.get("/show-available-coins")
async def show_available_coins() -> JSONResponse:
    """Return a JSONResponse with a dictionary of available coins in the Currywurst vending machine.

    Returns:
        JSONResponse: A JSONResponse object with a dictionary of available coins in the vending machine.
    """
    return JSONResponse(
        content={"Coins": cw_machine.coins}, status_code=status.HTTP_200_OK
    )


@app.get("/show-stored-notes")
async def show_stored_notes() -> JSONResponse:
    """Return a JSONResponse with a dictionary of stored notes in the Currywurst vending machine.

    Returns:
        JSONResponse: A JSONResponse object with a dictionary of stored notes in the vending machine.
    """
    return JSONResponse(
        content={"Notes": cw_machine.notes}, status_code=status.HTTP_200_OK
    )


@app.post("/pay")
async def pay(payment: Payment) -> JSONResponse:
    """Processes a payment for a Currywurst and returns the appropriate response.

    Args:
    payment (Payment): A Payment object containing the payment details.

    Returns:
    JSONResponse: A JSON response object containing the status of the payment and relevant details.
    """
    try:
        returned_coins = cw_machine.return_coins(
            currywurst_price=payment.currywurst_price, eur_inserted=payment.eur_inserted
        )

        response = {
            "machine_id": machine_id,
            "status": "success",
            "returned_coins": returned_coins,
            "error_msg": None,
        }
        redis_publisher.publish_purchase(params=response)
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)

    except (InsuficientInsertedMoneyException, NotExactChangeAvailableException) as e:
        response = (
            {
                "machine_id": machine_id,
                "status": "failed",
                "returned_coins": None,
                "error_msg": str(e),
            },
        )
        redis_publisher.publish_purchase(params=response)
        return JSONResponse(
            content=response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
