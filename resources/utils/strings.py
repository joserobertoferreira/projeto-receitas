def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_positive_number(value):
    try:
        number = float(value)
        if number > 0:
            return True
        else:
            return False
    except ValueError:
        return False


def is_negative_number(value):
    try:
        number = float(value)
        if number < 0:
            return True
        else:
            return False
    except ValueError:
        return False
