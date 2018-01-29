from django.core.management.base import BaseCommand, CommandError
from sua.models import Nonce
import time


EXPIRE_TIME = 60


class Command(BaseCommand):
    help = '清理过期的Nonce'

    def handle(self, *args, **options):
        cleanNonces = Nonce.objects.filter(timestamp__lte=int(time.time())-EXPIRE_TIME)
        cleanedNonceIDs = []
        for nonce in cleanNonces:
            cleanedNonceIDs.append(nonce.pk)
            nonce.delete()
        self.stdout.write('删除了%s个Nonce' % len(cleanedNonceIDs))
