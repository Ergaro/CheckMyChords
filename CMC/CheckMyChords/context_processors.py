import datetime

def version(request):
    ctx = {
        'date': datetime.date.today(),
        'version': 'v. 0.0.3',
    }
    return ctx

