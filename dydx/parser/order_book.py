def parse_order_book(_order_book: dict[str, list[dict]]) -> dict[str, dict[str, dict[float, float]]]:
    order_book = {
        "quotes": {
            "bids": parse_quotes(_order_book["bids"]),
            "asks": parse_quotes(_order_book["asks"]),
        },
        "offsets": {
            "bids": parse_offsets(_order_book["bids"]),
            "asks": parse_offsets(_order_book["asks"]),
        },
    }

    return order_book


def parse_quotes(_quotes: list[dict]) -> dict[float, float]:
    quotes: dict[float, float] = {}  # quotes[price] -> size
    for quote in _quotes:
        quotes[float(quote["price"])] = float(quote["size"])

    return quotes


def parse_offsets(_quotes: list[dict]) -> dict[float, float]:
    offsets: dict[float, float] = {}  # quotes[price] -> offset
    for quote in _quotes:
        offsets[float(quote["price"])] = float(quote["offset"])

    return offsets
