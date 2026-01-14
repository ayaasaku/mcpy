# example_usage.py
# ✅ How to use your PyMC library (write your Minecraft logic here!)
# All imports are clean and simple (no deep paths)
from main import (
    Var, MCFunction, Compiler, Datapack,
    ExecuteChain, give, setblock, say,
    all_players, nearest_player, self_player
)

# --------------------------
# 1. Initialize Library Tools
# --------------------------
compiler = Compiler()
datapack = Datapack("my_first_pymc_datapack")
load_func = MCFunction("load")  # Runs once when datapack loads
main_func = MCFunction("main")  # Your main logic

# --------------------------
# 2. Create Variables (JMC: var loop_counter = 0)
# --------------------------
loop_counter = Var("loop_counter", 0)
load_func.add(loop_counter.create_cmd())  # Create scoreboard on load

# --------------------------
# 3. Command Chaining (YOUR #1 REQUEST!) → JMC STYLE
# --------------------------
# JMC: execute.as(@a).ifBlock(0,64,0,stone).run(give(@p, diamond))
chain_cmd = ExecuteChain()\
    .as_target(all_players())\
    .if_block(0,64,0,"stone")\
    .run(give(nearest_player(), "diamond", 1))
main_func.add(chain_cmd)

# --------------------------
# 4. Python For Loop → Compiled to MC Loop
# --------------------------
# Place 10 stone blocks (x=0-9, y=64, z=0)
loop_cmds = [setblock(x,64,0,"stone") for x in range(10)]
compiled_loop = compiler.compile_for_loop(
    loop_var=loop_counter,
    start=0,
    end=9,
    target=self_player(),
    loop_cmds=loop_cmds
)
main_func.add("\n".join(compiled_loop))

# --------------------------
# 5. If/Else Logic
# --------------------------
cond = loop_counter.condition(self_player().build(), ">", 5)
if_cmds = [give(self_player(), "golden_apple", 2)]
else_cmds = [give(self_player(), "stick", 1)]
compiled_if = compiler.compile_if_else(cond, if_cmds, else_cmds)
main_func.add("\n".join(compiled_if))

# --------------------------
# 6. Generate the Datapack
# --------------------------
datapack.write_pack_meta()
datapack.write_function(load_func)
datapack.write_function(main_func)
datapack.write_load_tag(load_func)

print("\n🎉 SUCCESS! Datapack generated in 'generated_datapacks/my_first_pymc_datapack'")
print("👉 Drop the folder into your Minecraft world's 'datapacks' folder and run /reload")
print("👉 Run your logic with: /function pymc:main")