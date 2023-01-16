from typing import Any


def parse_positions(_positions: list) -> dict[str, dict[str, Any]]:
    positions = {}
    for _position in _positions:
        position = parse_position(_position)
        positions[position["market"]] = position

    return positions


def parse_position(_position: dict) -> dict[str, Any]:
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
        case {"market": market, "status": "LIQUIDATED"}:
            position = {
                "market": market,
                "entry_price": 0.0,
                "size": 0.0,
            }
        case {"market": market}:
            position = {
                "market": market,
                "entry_price": 0.0,
                "size": 0.0,
            }

    return position
