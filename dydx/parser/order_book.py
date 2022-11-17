def parse_order_book(_order_book: dict[str, list[dict]]) -> dict[str, list[dict]]:
    order_book = {
        "bids": parse_quotes(_order_book["bids"]),
        "asks": parse_quotes(_order_book["asks"]),
    }

    return order_book


def parse_quotes(_quotes: list[dict]) -> list[dict]:
    quotes = []
    for quote in _quotes:
        quotes.append(
            {
                "size": float(quote["size"]),
                "price": float(quote["price"]),
            }
        )

    return quotes
