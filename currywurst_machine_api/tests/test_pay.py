from fastapi.testclient import TestClient
from src.api import app
from src.payloads import Payment

client = TestClient(app)


def test_pay_success(empty_eur_inserted, currywurst_price):
    empty_eur_inserted["5"] = 1

    payment = Payment(
        currywurst_price=currywurst_price, eur_inserted=empty_eur_inserted
    )
    
    response = client.post("/pay", json=payment.dict())
    import pdb;pdb.set_trace()
    assert response.status_code == 200
    assert response.json() == {
        "machine_id": 123456,
        "status": "success",
        "returned_coins": {
            '2': 1,
            '1': 1,
            '0.5': 1,
            '0.2': 1,
            '0.1': 0,
            '0.05': 1,
            '0.02': 1,
            '0.01': 0,
        },
        "error_msg": None,
    }


# def test_bad_empty_eur_inserted_payload(empty_eur_inserted, currywurst_price):
#     empty_eur_inserted[0.51] = 1
#     payment_json = {
#         "eur_inserted": empty_eur_inserted,
#         "currywurst_price": currywurst_price,
#     }
#     response = client.post("/pay", json=payment_json)

#     assert response.status_code == 400
#     assert response.json() == {
#         "machine_id": 123456,
#         "status": "failed",
#         "returned_coins": None,
#         "error_msg": "Invalid coin/note value: 0.51",
#     }
