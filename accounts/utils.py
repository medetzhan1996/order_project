import phonenumbers
from datetime import date


def is_valid_phone_number(phone):
    """
    Проверяет, является ли предоставленный номер телефона действительным.
    """
    try:
        parsed_phone = phonenumbers.parse(phone, None)
        return phonenumbers.is_valid_number(parsed_phone)
    except phonenumbers.NumberParseException:
        return False


def calculate_age(date_of_birth):
    """
    Рассчитывает возраст на основе даты рождения.
    """
    today = date.today()
    return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
