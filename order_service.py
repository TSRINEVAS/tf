import time
import uuid

from boba_data import ORDERS, product_by_id


def calculate_order(items):
    normalized_items = []
    subtotal = 0

    for item in items:
        product = product_by_id(item.get("id"))
        quantity = int(item.get("quantity", 0))
        if product is None or quantity <= 0:
            continue

        line_total = product["price"] * quantity
        subtotal += line_total
        normalized_items.append(
            {
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity,
                "line_total": line_total,
            }
        )

    packaging_fee = 15 if normalized_items else 0
    delivery_fee = 35 if subtotal and subtotal < 499 else 0
    total = subtotal + packaging_fee + delivery_fee

    return {
        "items": normalized_items,
        "subtotal": subtotal,
        "packaging_fee": packaging_fee,
        "delivery_fee": delivery_fee,
        "total": total,
    }


def create_order(customer, items):
    required_fields = ["name", "phone", "address", "payment"]
    missing_fields = [field for field in required_fields if not str(customer.get(field, "")).strip()]
    if missing_fields:
        return None, {"error": "Missing customer fields", "fields": missing_fields}

    order_summary = calculate_order(items)
    if not order_summary["items"]:
        return None, {"error": "Cart is empty"}

    order = {
        "id": "BOBA-" + uuid.uuid4().hex[:8].upper(),
        "created_at": int(time.time()),
        "customer": {
            "name": customer["name"].strip(),
            "phone": customer["phone"].strip(),
            "address": customer["address"].strip(),
            "payment": customer["payment"].strip(),
        },
        "items": order_summary["items"],
        "subtotal": order_summary["subtotal"],
        "packaging_fee": order_summary["packaging_fee"],
        "delivery_fee": order_summary["delivery_fee"],
        "total": order_summary["total"],
        "eta": "25-35 minutes",
        "status": "received",
    }
    ORDERS.append(order)
    return order, None
