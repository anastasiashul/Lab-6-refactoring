#Магические числа
discount_on_SAVE10=0.10
discount_on_SAVE20 = 0.20
min_total_for_SAVE20 = 200
discount_on_less_total_for_SAVE20 = 0.05
VIP_discount=50
min_total_for_VIP=100
discount_on_less_total_for_vip = 10
tax_const=0.21

#Разбор запроса 
def parse_request(request: dict):
    user_id = request.get("user_id")
    items = request.get("items")
    coupon = request.get("coupon")
    currency = request.get("currency") or "USD"
    return user_id, items, coupon, currency


#Валидация полей запроса

def validate_fields(user_id, items):
    if user_id is None:
        raise ValueError("user_id is required")
    if items is None:
        raise ValueError("items is required")
# Валидация товаров
def validate_items(items):
    if type(items) is not list:
        raise ValueError("items must be a list")
    if len(items) == 0:
        raise ValueError("items must not be empty")

    for it in items:
        if "price" not in it or "qty" not in it:
            raise ValueError("item must have price and qty")
        if it["price"] <= 0:
            raise ValueError("price must be positive")
        if it["qty"] <= 0:
            raise ValueError("qty must be positive")


#Расчет суммы
def count_subtotal(items):
    subtotal = 0
    for it in items:
        subtotal = subtotal + it["price"] * it["qty"]
    return subtotal


#Расчет скидки
def count_disscount(coupon, subtotal):
    discount = 0
    if coupon is None or coupon == "":
        discount = 0
    elif coupon == "SAVE10":
        discount = int(subtotal * discount_on_SAVE10)
    elif coupon == "SAVE20":
        if subtotal >= min_total_for_SAVE20:
            discount = int(subtotal * discount_on_SAVE20)
        else:
            discount = int(subtotal * discount_on_less_total_for_SAVE20)
    elif coupon == "VIP":
        discount = VIP_discount
        if subtotal < min_total_for_VIP:
            discount = discount_on_less_total_for_vip
    else:
        raise ValueError("unknown coupon")
    return discount


#Расчет налога
def count_tax(total):
    return int(total * tax_const)


#Основная функция
def process_checkout(request: dict) -> dict:
    user_id, items, coupon, currency = parse_request(request)
    validate_fields(user_id, items)
    validate_items(items)

    subtotal = count_subtotal(items)
    discount=count_disscount(coupon, subtotal)
    total_after_discount = max(subtotal - discount, 0)
    
    tax = count_tax(total_after_discount)
    total = total_after_discount + tax

    order_id = str(user_id) + "-" + str(len(items)) + "-" + "X"

    return {
        "order_id": order_id,
        "user_id": user_id,
        "currency": currency,
        "subtotal": subtotal,
        "discount": discount,
        "tax": tax,
        "total": total,
        "items_count": len(items),
    }
