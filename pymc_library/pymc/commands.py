# pymc/commands.py
from .errors import validate_item, validate_block
from .entities import Entity
from .core import Var, MCFunction

# --------------------------
# ✅ HELPER: Add minecraft: namespace to MC IDs (auto-fix)
# --------------------------
def _add_namespace(id_str: str) -> str:
    return id_str if id_str.startswith("minecraft:") else f"minecraft:{id_str}"

# --------------------------
# ✅ CORE MC COMMANDS (WRAPPED, NO RAW SYNTAX)
# All return valid MC command strings (ready to add to MCFunction)
# --------------------------
def give(target: Entity | str, item: str, count: int = 1) -> str:
    """Give an item to a target (Entity or selector string)"""
    validate_item(item)
    target_str = target.build() if isinstance(target, Entity) else target
    item_id = _add_namespace(item)
    return f"/give {target_str} {item_id} {count}"

def tp(target: Entity | str, x: int, y: int, z: int) -> str:
    """Teleport a target to coordinates"""
    target_str = target.build() if isinstance(target, Entity) else target
    return f"/tp {target_str} {x} {y} {z}"

def setblock(x: int, y: int, z: int, block: str) -> str:
    """Set a block at coordinates"""
    validate_block(block)
    block_id = _add_namespace(block)
    return f"/setblock {x} {y} {z} {block_id}"

def say(message: str) -> str:
    """Send a chat message"""
    return f"/say {message}"

def summon(entity: str, x: int, y: int, z: int) -> str:
    """Summon an entity at coordinates"""
    entity_id = _add_namespace(entity)
    return f"/summon {entity_id} {x} {y} {z}"

# --------------------------
# ✅ 🔥 FLAGSHIP FEATURE: FLUENT EXECUTE COMMAND CHAINING (JMC EXACT COPY)
# JMC: execute.as(@a).ifBlock(0,64,0,stone).run(give(@p, diamond))
# PyMC: ExecuteChain().as_target(all_players()).if_block(0,64,0,"stone").run(give(nearest_player(), "diamond"))
# --------------------------
class ExecuteChain:
    """
    Fluent, chainable execute command builder (mirrors JMC's execute chain EXACTLY)
    All methods return self → chain forever: .as_target().if_block().if_score().run()
    Generates valid MC execute commands with zero manual syntax.
    """
    def __init__(self):
        self.chain_parts = []  # Store chain segments (e.g., ["as @a", "if block 0 64 0 stone"])

    # ✅ Chain Step 1: Set target (JMC: .as(@a))
    def as_target(self, target: Entity | str) -> "ExecuteChain":
        target_str = target.build() if isinstance(target, Entity) else target
        self.chain_parts.append(f"as {target_str}")
        return self

    # ✅ Chain Step 2: If block condition (JMC: .ifBlock(x,y,z,block))
    def if_block(self, x: int, y: int, z: int, block: str) -> "ExecuteChain":
        validate_block(block)
        block_id = _add_namespace(block)
        self.chain_parts.append(f"if block {x} {y} {z} {block_id}")
        return self

    # ✅ Chain Step 3: If score condition (JMC: .ifScore(var, op, val))
    def if_score(self, var: Var, target: Entity | str, operator: str, value: int) -> "ExecuteChain":
        target_str = target.build() if isinstance(target, Entity) else target
        cond = var.condition(target_str, operator, value)
        self.chain_parts.append(f"if {cond}")
        return self

    # ✅ Chain Step 4: Run a command/function (JMC: .run(cmd)) → FINAL STEP
    def run(self, cmd: str) -> str:
        """Build the final execute command and return it (end of chain)"""
        chain_str = " ".join(self.chain_parts)
        return f"/execute {chain_str} run {cmd.strip()}"