import dateutil.parser
import datetime
import project.sua.models as myModels

DATETIME_FORMAT_SHOW = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT_SHOW = "%Y-%m-%d"
DATETIME_FORMAT_VALUE = "%Y-%m-%dT%H:%M:%S"
DATE_FORMAT_VALUE = "%Y-%m-%d"

YEAR_CHOICES = []
for r in range(2016, datetime.datetime.now().year):
    YEAR_CHOICES.append((r, r + 1))

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


def get_deleteds(model, serializer, request):
    set = model.objects.order_by('-deletedAt').exclude(deletedAt=None)
    set_data = serializer(
        set,
        many=True,
        context={
            'request': request
        }
    )

    datas = set_data.data

    for i in range(len(datas)):
        datas[i]['deletedAt'] = set[i].deletedAt

    return list(set_data.data)


def sort_by_deletedAt(elem):
    return elem['deletedAt']



#计算传入的suas列表的公益时数总和
def TotalSuahours(suas):
    total_suahours = 0
    if len(suas) != 0 :
        for sua in suas:
            total_suahours += sua.suahours
    return total_suahours
