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



# def SuasFilter(suas,request):
    
    



#计算传入的suas列表的公益时数总和
def TotalSuahours(suas):
    total_suahours = 0
    if len(suas) != 0 :
        for sua in suas:
            total_suahours += sua.suahours
    return total_suahours