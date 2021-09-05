
def not_empty(val):
    if not val:
        raise ValidationError('value can not be empty')
