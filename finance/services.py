import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(unit):
    """Создает продукт в страйпе."""

    product = stripe.Product.create(name=unit.id)

    return product


def create_stripe_price(amount, product):
    """Создает цену в страйпе."""

    price = stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        # recurring={"interval": "month"}, #  Регулярное списание средств (рассрочка)
        product_data={"name": product},
    )

    return price


def create_stripe_session(price):
    """Создает сессию на оплату в страйпе."""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )

    return session.get("id"), session.get("url")


def create_stripe_checkout(session_id):

    checkout = stripe.checkout.Session.retrieve(
        session_id,
    )

    return checkout
