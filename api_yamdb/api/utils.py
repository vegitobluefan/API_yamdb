from django.core.exceptions import ValidationError

def return_response(msg):
    """Метод для dry."""
    raise ValidationError(msg)

def validate_username(data):
    """Функция для проверки me."""
    if data == 'me':
        return_response(
        'Выберите другой username')