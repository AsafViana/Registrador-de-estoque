import string as s
from random import *

ch = s.ascii_letters + s.digits + s.punctuation

senha = ''.join(choice(ch)for x in range(randint(8, 16)))

print(senha)