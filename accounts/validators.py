from django.core.validators import RegexValidator

class NINValidator(RegexValidator):
    regex = r'^\d{11}$'  # Example: Three uppercase letters followed by four digits
    message = 'Invalid NIN format. Must be 11 digits.'
    code = 'invalid_code_format'