
# __all__ = ['str_month_to_years_and_months']

def str_months_to_years_and_months(months):
    years,months = divmod(months, 12)
    str_formatted = (
        years,
        'years' if years>1 else 'year' if years>0 else '',
        ',' if years>0 else '',
        months,
        'months' if months>1 else 'month' if months>0 else '',
    )
    return "{} {}{} {} {}".format(*str_formatted)

def get_public_attributes(obj):
    """ Returns a tuple of public attributes of an object/class. """
    return tuple([d for d in dir(obj) if not d.startswith('_')])