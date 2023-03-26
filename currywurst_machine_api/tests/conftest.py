import pytest


@pytest.fixture
def empty_eur_inserted():
    return {
        500.0: 0,
        200.0: 0,
        100.0: 0,
        50.0: 0,
        20.0: 0,
        10.0: 0,
        5.0: 1,
        2.0: 0,
        1.0: 0,
        0.5: 0,
        0.2: 0,
        0.1: 0,
        0.05: 0,
        0.02: 0,
        0.01: 0,
    }


@pytest.fixture
def currywurst_price():
    return 1.23
