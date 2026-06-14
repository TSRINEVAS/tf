import time
import uuid

from boba_data import CATERING_REQUESTS, LOYALTY_MEMBERS, ORDERS, product_by_id


def clean_text(value):
    return str(value or "").strip()


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
    missing_fields = [field for field in required_fields if not clean_text(customer.get(field))]
    if missing_fields:
        return None, {"error": "Missing customer fields", "fields": missing_fields}

    order_summary = calculate_order(items)
    if not order_summary["items"]:
        return None, {"error": "Cart is empty"}

    order = {
        "id": "BOBA-" + uuid.uuid4().hex[:8].upper(),
        "created_at": int(time.time()),
        "customer": {
            "name": clean_text(customer["name"]),
            "phone": clean_text(customer["phone"]),
            "address": clean_text(customer["address"]),
            "payment": clean_text(customer["payment"]),
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


def create_catering_request(payload):
    required_fields = ["name", "phone", "event_date", "guest_count", "event_type"]
    missing_fields = [field for field in required_fields if not clean_text(payload.get(field))]
    if missing_fields:
        return None, {"error": "Missing catering fields", "fields": missing_fields}

    try:
        guest_count = int(payload.get("guest_count", 0))
    except (TypeError, ValueError):
        guest_count = 0

    if guest_count < 10:
        return None, {"error": "Catering starts at 10 guests"}

    request = {
        "id": "CAT-" + uuid.uuid4().hex[:8].upper(),
        "created_at": int(time.time()),
        "name": clean_text(payload.get("name")),
        "phone": clean_text(payload.get("phone")),
        "event_date": clean_text(payload.get("event_date")),
        "guest_count": guest_count,
        "event_type": clean_text(payload.get("event_type")),
        "notes": clean_text(payload.get("notes")),
        "status": "requested",
    }
    CATERING_REQUESTS.append(request)
    return request, None


def create_loyalty_member(payload):
    required_fields = ["name", "phone"]
    missing_fields = [field for field in required_fields if not clean_text(payload.get(field))]
    if missing_fields:
        return None, {"error": "Missing loyalty fields", "fields": missing_fields}

    phone = clean_text(payload.get("phone"))
    existing_member = next((member for member in LOYALTY_MEMBERS if member["phone"] == phone), None)
    if existing_member:
        return existing_member, None

    member = {
        "id": "BBI-" + uuid.uuid4().hex[:6].upper(),
        "created_at": int(time.time()),
        "name": clean_text(payload.get("name")),
        "phone": phone,
        "favorite": clean_text(payload.get("favorite")) or "Surprise me",
        "points": 50,
        "status": "active",
    }
    LOYALTY_MEMBERS.append(member)
    return member, None
