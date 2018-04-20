import dateutil.parser

DATETIME_FORMAT_SHOW = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT_SHOW = "%Y-%m-%d"
DATETIME_FORMAT_VALUE = "%Y-%m-%dT%H:%M:%S"
DATE_FORMAT_VALUE = "%Y-%m-%d"

def TZString2DateTime(s):
    if s is None:
        return None
    return dateutil.parser.parse(s)

def TZString2Date(s):
    if s is None:
        return None
    return TZString2DateTime(s).date()

def Date2String_SHOW(date):
    if date is None:
        return None
    return date.strftime(DATE_FORMAT_SHOW)

def DateTime2String_SHOW(date):
    if date is None:
        return None
    return date.strftime(DATETIME_FORMAT_SHOW)

def Date2String_VALUE(date):
    if date is None:
        return None
    return date.strftime(DATE_FORMAT_VALUE)

def DateTime2String_VALUE(date):
    if date is None:
        return None
    return date.strftime(DATETIME_FORMAT_VALUE)
