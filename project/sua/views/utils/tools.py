import dateutil.parser

DATETIME_FORMAT_SHOW = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT_SHOW = "%Y-%m-%d"
DATETIME_FORMAT_VALUE = "%Y-%m-%dT%H:%M:%S"
DATE_FORMAT_VALUE = "%Y-%m-%d"

def TZString2DateTime(s):
    return dateutil.parser.parse(s)

def TZString2Date(s):
    return TZString2DateTime(s).date()

def Date2String_SHOW(date):
    return date.strftime(DATE_FORMAT_SHOW)

def DateTime2String_SHOW(date):
    return date.strftime(DATETIME_FORMAT_SHOW)

def Date2String_VALUE(date):
    return date.strftime(DATE_FORMAT_VALUE)

def DateTime2String_VALUE(date):
    return date.strftime(DATETIME_FORMAT_VALUE)
