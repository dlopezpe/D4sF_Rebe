from .models import Log


def savelog(context = {},request = {}):
    # get ip user firs
    ipUser = getRequestIp(request) if not type(request) is dict else False
    model = Log()
    model.user_email = context['user_email']
    if ipUser:
        model.ip = ipUser
    
    
    if request.path:
        model.path = request.path

    if request.method:
        model.method = request.method
    
    if 'app_name' in context:
        model.app_name = context['app_name']

    model.message = context['message']
    model.status = context['status'] # success, warning, error
    model.extra_data = context['extra_data']

    model.save(using="logs")

def getRequestIp(request):
    # get ip from request
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = 'None'
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    return ip

def getFrontAction(method):
    if method == 'POST':
        return 'CREATE'
    elif method in ['PUT', 'PATCH']:
        return 'UPDATE'
    elif method == 'DELETE':
        return 'DELETE'
    return 'UNKNOWN'

# def identify_model(data):
#     if 'campo_especifico_trazas' in data:
#         return 'Trazas'
#     elif 'campo_especifico_otro_modelo' in data:
#             return 'OtroModelo'
#     return 'Desconocido'

