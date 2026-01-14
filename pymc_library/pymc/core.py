# pymc/core.py
from .errors import PyMCValidationError, validate_operator

# --------------------------
# ✅ JMC's "var x = 0" → PyMC Var CLASS (scoreboard-backed variables)
# --------------------------
class Var:
    """
    Represents a Minecraft scoreboard variable (JMC equivalent: var name = 0)
    Auto-creates unique scoreboard objectives, no duplicate variables allowed.
    All MC variable logic is encapsulated here — no raw /scoreboard commands!
    """
    _registered_vars = set()  # Track all variables to prevent duplicates

    def __init__(self, name: str, default_value: int = 0):
        self.name = name.strip().lower()
        self.default_value = default_value
        self.objective = f"pymc_var_{self.name}"  # Unique scoreboard objective name

        # ✅ Error check: No duplicate variables
        if self.name in Var._registered_vars:
            raise PyMCValidationError(f"Variable '{self.name}' already exists! Use unique names.")
        Var._registered_vars.add(self.name)

    def create_cmd(self) -> str:
        """Generate command to CREATE the scoreboard objective (run once on load)"""
        return f"/scoreboard objectives add {self.objective} dummy [PyMC Var: {self.name}]"

    def set_cmd(self, target: str, value: int) -> str:
        """Generate command to SET the variable's value for a target (@s, @a, etc.)"""
        return f"/scoreboard players set {target} {self.objective} {value}"

    def add_cmd(self, target: str, value: int) -> str:
        """Generate command to ADD to the variable (for loops: counter +=1)"""
        return f"/scoreboard players add {target} {self.objective} {value}"

    def condition(self, target: str, operator: str, value: int) -> str:
        """
        Generate a MC score condition string (for if/else/loop logic)
        Example: var.condition("@s", ">", 5) → "score @s pymc_var_x greaterThan 5"
        """
        validate_operator(operator)  # ✅ Auto error check operator
        mc_op_map = {
            "==": "equals", "!=": "notequals", "<": "lessThan", ">": "greaterThan",
            "<=": "lessThanOrEqual", ">=": "greaterThanOrEqual"
        }
        return f"score {target} {self.objective} {mc_op_map[operator]} {value}"

# --------------------------
# ✅ JMC's "function name() {}" → PyMC MCFunction CLASS (reusable mcfunction)
# --------------------------
class MCFunction:
    """
    Represents a reusable Minecraft function (JMC equivalent: function name() { ... })
    Encapsulates a list of mcfunction commands, has a unique name/namespace.
    Callable via /function namespace:name (auto-generated)
    """
    def __init__(self, name: str, namespace: str = "pymc"):
        self.name = name.strip().lower()
        self.namespace = namespace.strip().lower()
        self.commands = []  # List of compiled mcfunction commands (strings)

    def add(self, cmd: str) -> None:
        """Add a valid mcfunction command to this function (auto-clean whitespace)"""
        clean_cmd = cmd.strip()
        if clean_cmd and not clean_cmd.startswith("#"):
            self.commands.append(clean_cmd)

    def full_name(self) -> str:
        """Return full MC function name (namespace:name) → e.g., pymc:give_loot"""
        return f"{self.namespace}:{self.name}"

    def call_cmd(self) -> str:
        """Generate command to CALL this function → /function namespace:name"""
        return f"/function {self.full_name()}"

# --------------------------
# ✅ Namespace (MC Datapack Standard)
# --------------------------
class Namespace:
    """Simple wrapper for MC datapack namespaces (avoids invalid characters)"""
    def __init__(self, name: str):
        self.name = name.strip().lower().replace(" ", "_")
        if not self.name:
            raise PyMCValidationError("Namespace cannot be empty!")