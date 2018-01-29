from sua.models import Nonce
from .api import EXPIRE_TIME
import time


def cleanNonce():
        cleanNonces = Nonce.objects.filter(timestamp__lte=int(time.time())-EXPIRE_TIME)
        cleanedNonceIDs = []
        for nonce in cleanNonces:
            cleanedNonceIDs.append(nonce.pk)
            nonce.delete()
