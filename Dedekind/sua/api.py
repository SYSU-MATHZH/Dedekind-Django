from .models import Nonce
import time

EXPIRE_TIME = 120


def check_signature(request):
    if request.method == 'GET':
        nonce = request.GET.get('nonce')
        timestamp = request.GET.get('timestamp')
        signature = request.GET.get('signature')
        if nonce is None or timestamp is None or signature is None or (int(time.time()) - int(timestamp)) >= EXPIRE_TIME:
            return False
        else:
            non = Nonce.objects.filter(nonce=int(nonce), timestamp=int(timestamp))
            if non.count() == 0:
                non = Nonce.objects.create(nonce=int(nonce), timestamp=int(timestamp))
                if non.getSignature() == signature:
                    return True
                else:
                    return False
            else:
                return False
    else:
        return False
