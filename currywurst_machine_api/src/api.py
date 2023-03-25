from fastapi import FastAPI
from .machine import CurrywurstMachine
from .payloads import Payment
from .redis_publisher import RedisPublisher
app = FastAPI()
cw_machine = CurrywurstMachine()
redis_publisher = RedisPublisher(redis_host="redis")

@app.post("/pay")
async def pay(payment: Payment):

    try:
        returned_coins = cw_machine.return_coins(
            currywurst_price=payment.currywurst_price,
            eur_inserted=payment.eur_inserted
        )

        machine_id = 123456 # Can come from other place. 
        response = {"machine_id":machine_id,"status": "success", "returned_coins": returned_coins, "error_code": None}
        redis_publisher.publish_purchase(params=response)
        return response
    
    except ValueError as e:
        return {"status": "failed", "returned_coins": None, "error_code": str(e)}