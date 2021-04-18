def first_match(iterable, default=None, pred=None):
    return next(filter(pred, iterable), default)
