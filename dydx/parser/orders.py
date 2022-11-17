def format(_order: dict) -> dict:
    match _order:
        case {
            "id": id,
            "market": market,
            "side": str(side),
            "price": price,
            "size": size,
            "remainingSize": remaining_size,
            "type": type,
            "createdAt": created_at,
            "status": status,
        }:
            order = {
                "id": id,
                "ticker": market,
                "side": side.lower(),
                "price": float(price),
                "size": float(size),
                "filled": float(size) - float(remaining_size),
                "type": type,
                "time": created_at,
                "status": status,
            }

            return order
        case _:
            return {}
