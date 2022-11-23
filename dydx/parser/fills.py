def parse(_fill: dict) -> dict:
    match _fill:
        case {
            "id": id,
            "orderId": order_id,
            "market": market,
            "side": str(side),
            "price": price,
            "size": size,
            "fee": fee,
            "type": str(type),
            "liquidity": str(liquidity),
            "createdAt": created_at,
        }:
            fill = {
                "id": id,
                "order_id": order_id,
                "market": market,
                "side": side.lower(),
                "price": float(price),
                "size": float(size),
                "fee": float(fee),
                "type": type.lower(),
                "liquidity": liquidity.lower(),
                "time": created_at,
            }

            return fill
        case _:
            return {}
