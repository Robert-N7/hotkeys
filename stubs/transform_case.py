def _transform_upper(text, transform_first):
    new = ''
    upper_next = transform_first
    for c in text:
        if c in ('_', ',', ' '):
            upper_next = True
        elif upper_next:
            new += c.upper()
            upper_next = False
        else:
            new += c
    return new


def _transform_lower(text, separator):
    separator = separator
    new = ''
    first = True
    last_was_separator = False
    for c in text:
        if c in ('_', '-', ' '):
            new += separator
            last_was_separator = True
        elif c.isupper():
            if not first and not last_was_separator:
                new += separator
            new += c.lower()
        else:
            new += c
    return new


def camel_case(text):
    return _transform_upper(text, False)


def pascal_case(text):
    return _transform_upper(text, True)


def snake_case(text):
    return _transform_lower(text, '_')


def kebab_case(text):
    return _transform_lower(text, '-')
