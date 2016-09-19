import sys
import os
pushbullet_path = os.path.abspath('pushbullet.py')
if os.path.exists(pushbullet_path):
    sys.path.insert(0, pushbullet_path)

from .__version__ import __version__
from .botbullet import Botbullet
from .bot import Bot
from .module import Module
from .errors import *

Botbullet = Botbullet
