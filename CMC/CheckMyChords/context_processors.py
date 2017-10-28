import datetime

def version(request):
    ctx = {
        'date': datetime.date.today(),
        'version': 'v. 0.1.1',
    }
    return ctx

