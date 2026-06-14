PRODUCTS = [
    {
        "id": "classic-milk-tea",
        "name": "Classic Milk Tea",
        "category": "Milk Tea",
        "price": 149,
        "description": "Assam black tea, creamy milk, and chewy tapioca pearls.",
        "badge": "Best Seller",
    },
    {
        "id": "brown-sugar-boba",
        "name": "Brown Sugar Boba",
        "category": "Signature",
        "price": 189,
        "description": "Caramel brown sugar syrup, fresh milk, and warm pearls.",
        "badge": "Signature",
    },
    {
        "id": "mango-green-tea",
        "name": "Mango Green Tea",
        "category": "Fruit Tea",
        "price": 169,
        "description": "Green tea with Alphonso mango, popping boba, and ice.",
        "badge": "Tropical",
    },
    {
        "id": "taro-latte",
        "name": "Taro Latte",
        "category": "Latte",
        "price": 179,
        "description": "Nutty taro, milk, tapioca pearls, and a soft purple finish.",
        "badge": "Creamy",
    },
    {
        "id": "masala-chai-boba",
        "name": "Masala Chai Boba",
        "category": "India Special",
        "price": 159,
        "description": "Indian masala chai with boba pearls and a smooth milk base.",
        "badge": "Local Favorite",
    },
    {
        "id": "strawberry-matcha",
        "name": "Strawberry Matcha",
        "category": "Premium",
        "price": 219,
        "description": "Layered strawberry puree, matcha, milk, and crystal boba.",
        "badge": "Premium",
    },
]


ORDERS = []
CATERING_REQUESTS = []
LOYALTY_MEMBERS = []


def product_by_id(product_id):
    return next((product for product in PRODUCTS if product["id"] == product_id), None)
