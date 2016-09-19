import sys
sys.path.insert(0, "pushbullet.py")

from .__version__ import __version__
from .botbullet import Botbullet
from .bot import Bot
from .module import Module
from .errors import *

Botbullet = Botbullet
