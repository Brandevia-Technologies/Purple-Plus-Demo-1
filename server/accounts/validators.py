from django.core.validators import RegexValidator

class NINValidator(RegexValidator):
    regex = r'^\d{11}$'
    message = 'Invalid NIN format. Must be 11 digits.'
    code = 'invalid_code_format'