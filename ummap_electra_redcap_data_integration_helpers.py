def lengthen_str(x, length, leading_str):
    """Ensure that `x`, if a string, is of length `length`

    :param x:
    :param length: Length to enforce `x` to be
    :type  length: int
    :return: `x` lengthened to
    """
    if isinstance(x, str):
        len_x = len(x)
        if length >= len_x:
            return x if len_x == length else leading_str * (length - len_x) + x
    else:
        return x