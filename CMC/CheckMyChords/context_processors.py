import datetime

def version(request):
    ctx = {
        'date': datetime.date.today(),
        'version': 'v. 0.1.0',
    }
    return ctx

