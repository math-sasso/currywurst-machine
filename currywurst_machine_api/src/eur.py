class EUR:
    def __init__(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("EUR value must be a number")
        if round(value, 2) != value:
            raise ValueError("EUR value must have two decimal places")
        self.value = value

    def __repr__(self):
        return f"EUR({self.value:.2f})"

    def __float__(self):
        return float(self.value)

    def __eq__(self, other):
        if isinstance(other, EUR):
            return self.value == other.value
        elif isinstance(other, (int, float)):
            return round(self.value, 2) == round(other, 2)
        else:
            return False