def parse(_order: dict) -> dict:
    match _order:
        case {
            "id": id,
            "market": market,
            "side": str(side),
            "price": price,
            "size": size,
            "remainingSize": remaining_size,
            "type": str(type),
            "createdAt": created_at,
            "status": str(status),
        }:
            order = {
                "id": id,
                "market": market,
                "side": side.lower(),
                "price": float(price),
                "size": float(size),
                "filled": float(size) - float(remaining_size),
                "type": type.lower(),
                "time": created_at,
                "status": status.lower(),
            }

            return order
        case _:
            return {}
