from decimal import Decimal


def to_decimal(value: str, precision: int = 4) -> Decimal:

    return round(Decimal(value), precision)
