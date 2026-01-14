# pymc/entities.py
from .errors import PyMCSyntaxError, validate_selector

# --------------------------
# ✅ ENTITY/SELECTOR CLASS (all MC entities/players, JMC equivalent: @a/@p/etc.)
# --------------------------
class Entity:
    """
    Represents a Minecraft entity/player selector (JMC equivalent: @a, @p, @s, @e, @r)
    Add filters (tags, positions, NBT) with simple methods — no manual bracket syntax!
    Auto-validates selectors and generates valid MC selector strings.
    """
    def __init__(self, base_selector: str):
        validate_selector(base_selector)  # ✅ Auto error check selector
        self.base = base_selector
        self.filters = []  # List of filters (e.g., ["tag=vip", "x=0"])

    # ✅ Add filters (no manual bracket syntax!)
    def with_tag(self, tag: str) -> "Entity":
        """Add a tag filter → @a[tag=vip]"""
        self.filters.append(f"tag={tag.strip()}")
        return self  # Return self for chaining!

    def at_pos(self, x: int, y: int, z: int) -> "Entity":
        """Add a position filter → @e[x=0,y=64,z=0]"""
        self.filters.append(f"x={x},y={y},z={z}")
        return self  # Return self for chaining!

    def build(self) -> str:
        """Generate the final valid MC selector string (e.g., @a[tag=vip,x=0])"""
        if not self.filters:
            return self.base
        return f"{self.base}[{','.join(self.filters)}]"

# --------------------------
# ✅ SHORTCUT FUNCTIONS (EASY TO USE, JMC STYLE)
# --------------------------
def all_players() -> Entity:
    """Shortcut for @a (all players)"""
    return Entity("@a")

def nearest_player() -> Entity:
    """Shortcut for @p (nearest player)"""
    return Entity("@p")

def self_player() -> Entity:
    """Shortcut for @s (self)"""
    return Entity("@s")

def all_entities() -> Entity:
    """Shortcut for @e (all entities)"""
    return Entity("@e")

def random_player() -> Entity:
    """Shortcut for @r (random player)"""
    return Entity("@r")