from fastapi.testclient import TestClient
from src.api import app
from src.payloads import Payment

client = TestClient(app)


def test_pay_success(empty_eur_inserted, currywurst_price):
    """Test a successful payment for a currywurst.

    The test checks that a payment can be made for the correct amount and that change is returned.
    """
    empty_eur_inserted["5"] = 1

    payment = Payment(
        currywurst_price=currywurst_price, eur_inserted=empty_eur_inserted
    )
    
    response = client.post("/pay", json=payment.dict())
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


def test_bad_empty_eur_inserted_payload_fail(empty_eur_inserted, currywurst_price):
    """Test that an invalid Euro coin or note value fails.

    The test verifies that a request with an invalid coin or note value results in an HTTP 400 Bad Request error.
    """
    empty_eur_inserted[0.51] = 1
    payment_json = {
        "eur_inserted": empty_eur_inserted,
        "currywurst_price": currywurst_price,
    }
    response = client.post("/pay", json=payment_json)
    assert response.status_code == 400
    assert response.json() == {
        "machine_id": 123456,
        "status": "failed",
        "returned_coins": None,
        "error_msg": "Invalid coin/note value: 0.51",
    }


def test_no_change_available_fail(empty_eur_inserted, currywurst_price):
    """Test that the vending machine can give exact change.

    The test checks that if the vending machine does not have enough coins or notes to give exact change, a failure message is returned.
    """
    empty_eur_inserted[500] = 1000
    payment_json = {
        "eur_inserted": empty_eur_inserted,
        "currywurst_price": currywurst_price,
    }
    response = client.post("/pay", json=payment_json)
    assert response.status_code == 500
    assert response.json()[0] == {
        "machine_id": 123456,
        "status": "failed",
        "returned_coins": None,
        "error_msg": "Exact change not possible",
    }

def test_money_inserted_not_enough_fail(empty_eur_inserted, currywurst_price):
    """Test that insufficient money is handled correctly.

    The test checks that if the amount of money inserted is less than the price of the currywurst, the payment fails.
    """
    empty_eur_inserted[1] = 1
    payment_json = {
        "eur_inserted": empty_eur_inserted,
        "currywurst_price": currywurst_price,
    }
    response = client.post("/pay", json=payment_json)
    assert response.status_code == 500
    assert response.json()[0] == {
        "machine_id": 123456,
        "status": "failed",
        "returned_coins": None,
        "error_msg": "Insufficient money inserted",
    }
