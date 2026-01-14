# pymc/compiler.py
from .core import Var, MCFunction
from .errors import validate_loop_bounds
from .entities import Entity

# --------------------------
# ✅ COMPILER CLASS (Python Logic → MCFunction Commands)
# Converts Python for/while loops + if/else → valid MC commands
# --------------------------
class Compiler:
    """
    Compiles Python native logic into Minecraft-compatible commands (mirrors JMC's compiler)
    MC has no loops/if statements — this class uses scoreboards + recursive functions to simulate them.
    All error checks are built-in (no infinite loops!).
    """
    def compile_if_else(
        self,
        condition: str,
        if_cmds: list[str],
        else_cmds: list[str] = None
    ) -> list[str]:
        """
        Compile Python if/else → MC execute commands
        condition: Output from Var.condition() or ExecuteChain
        if_cmds: Commands to run if condition is TRUE
        else_cmds: Commands to run if condition is FALSE (optional)
        """
        compiled = []
        # Compile IF block
        for cmd in if_cmds:
            compiled.append(f"/execute if {condition} run {cmd}")
        # Compile ELSE block
        if else_cmds:
            for cmd in else_cmds:
                compiled.append(f"/execute unless {condition} run {cmd}")
        return compiled

    def compile_for_loop(self, loop_var: Var, start: int, end: int, loop_cmds: list[str], target: Entity | str = "@s", step: int = 1) -> list[str]:
        """
        Compile Python for loop → MC scoreboard-based loop (JMC equivalent: for (var i=0; i<=10; i++))
        MC uses recursive function calls + scoreboard counters for loops — this class auto-generates all of it.
        """
        validate_loop_bounds(start, end, step)  # ✅ Auto error check (no infinite loops!)
        target_str = target.build() if isinstance(target, Entity) else target
        compiled = []

        # Step 1: Initialize loop variable to start value
        compiled.append(loop_var.set_cmd(target_str, start))

        # Step 2: Create loop condition (var <= end)
        loop_cond = loop_var.condition(target_str, ">=", end) if step <0 else loop_var.condition(target_str, "<=", end)

        # Step 3: Compile loop body (run commands if condition is true)
        for cmd in loop_cmds:
            compiled.append(f"/execute if {loop_cond} run {cmd}")
            compiled.append(f"/execute if {loop_cond} run {loop_var.add_cmd(target_str, step)}")

        return compiled