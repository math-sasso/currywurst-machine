from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from typing import Dict

from .machine import CurrywurstMachine
from .payloads import Payment
from .redis_publisher import RedisPublisher
from .custom_exceptions import (
    InsuficientInsertedMoneyException,
    NotExactChangeAvailableException,
)

app = FastAPI()
cw_machine = CurrywurstMachine()
redis_publisher = RedisPublisher(redis_host="redis")
machine_id = (
    123456  # Can come from other place. But will keep here for sake of simplicity
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle RequestValidationError.

    Parameters
    ----------
    request : Request
        Request object
    exc : RequestValidationError
        RequestValidationError object

    Returns
    -------
    Dict
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

@app.post("/refill_coins")
async def pay():
    cw_machine.refill_coins()

@app.post("/pay")
async def pay(payment: Payment):
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
        return JSONResponse(
            content = response,
            status_code= status.HTTP_200_OK
            )

    except (InsuficientInsertedMoneyException, NotExactChangeAvailableException) as e:
        
        return JSONResponse(
            content = {"machine_id": machine_id,"status": "failed", "returned_coins": None, "error_msg": str(e)},
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR
            )
