from .models import Order
from random import randint


def generate_unique_order_number():
    """Генерирует уникальный случайный шестизначный номер."""
    number = '{:06}'.format(randint(1, 999999))
    while Order.objects.filter(order_number=number).exists():
        number = '{:06}'.format(randint(1, 999999))
    return number
