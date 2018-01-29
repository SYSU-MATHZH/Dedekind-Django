import random
import time
import hashlib
from token import TOKEN

if __name__ == '__main__':
    url = r"https://localhost:8000/student/2/sualist"
    nonce = str(random.randint(0, 2147483647))
    timestamp = str(int(time.time()))
    s = bytes(nonce + timestamp + TOKEN, encoding='utf8')
    signature = hashlib.sha1(s).hexdigest()
    print(url + '?nonce=%s&timestamp=%s&signature=%s' % (nonce, timestamp, signature))
