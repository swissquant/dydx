def parse(_position: dict) -> dict:
    match _position:
        case {"market": market, "status": "OPEN", "entryPrice": entry_price, "size": size}:
            position = {
                "market": market,
                "entry_price": float(entry_price),
                "size": float(size),
            }
        case {"market": market, "status": "CLOSED"}:
            position = {
                "market": market,
                "entry_price": 0.0,
                "size": 0.0,
            }

    return position
