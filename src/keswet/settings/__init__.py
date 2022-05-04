from .base import *
from decouple import config

DEBUG = config("DEBUG")

if DEBUG == True:
    from .dev import *

elif DEBUG == False:
    from .prod import *