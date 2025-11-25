import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class PhoneNumberValidator:

    def __call__(self, value:str):
        if not re.match(r'^\d+$',value):
            raise ValidationError