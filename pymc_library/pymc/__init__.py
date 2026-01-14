# pymc/__init__.py
# Expose core classes/functions (importable via: from pymc import X)
from .core import Var, MCFunction, Namespace
from .entities import Entity, all_players, nearest_player, self_player, all_entities, random_player
from .commands import give, tp, setblock, say, summon, ExecuteChain
from .compiler import Compiler
from .datapack import Datapack
from .errors import PyMCError, PyMCSyntaxError, PyMCValidationError

# Library metadata
__version__ = "1.0.0"
__name__ = "PyMC"
__description__ = "Pure Python JMC Clone: Write Minecraft Datapacks with Python Logic"