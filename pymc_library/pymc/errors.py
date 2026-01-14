# pymc/errors.py
# --------------------------
# ✅ CUSTOM ERROR CLASSES (hierarchical, easy to catch)
# --------------------------
class PyMCError(Exception):
    """Base error for all PyMC library errors (parent class)"""
    pass

class PyMCSyntaxError(PyMCError):
    """Error for invalid MC syntax (e.g., bad selector, invalid item ID)"""
    pass

class PyMCValidationError(PyMCError):
    """Error for invalid logic (e.g., infinite loop, duplicate variable name)"""
    pass

# --------------------------
# ✅ VALIDATION DATABASES (MC vanilla valid values)
# --------------------------
# Add more items/blocks/entities as needed (expand this list easily)
VALID_MC_ITEMS = {"diamond", "iron_sword", "golden_apple", "stick", "stone", "dirt", "grass_block"}
VALID_MC_BLOCKS = {"stone", "dirt", "grass_block", "cobblestone", "oak_planks"}
VALID_MC_SELECTORS = {"@a", "@p", "@s", "@e", "@r"}
VALID_OPERATORS = {"==", "!=", "<", ">", "<=", ">="}

# --------------------------
# ✅ CORE VALIDATION FUNCTIONS (USED EVERYWHERE IN THE LIBRARY)
# --------------------------
def validate_selector(selector: str) -> None:
    """Check if a Minecraft selector is valid (@a/@p/@s/@e/@r)"""
    if selector not in VALID_MC_SELECTORS:
        raise PyMCSyntaxError(
            f"Invalid selector '{selector}'! Valid selectors: {', '.join(VALID_MC_SELECTORS)}"
        )

def validate_item(item: str) -> None:
    """Check if an item ID is valid (auto-adds minecraft: namespace)"""
    clean_item = item.replace("minecraft:", "")
    if clean_item not in VALID_MC_ITEMS:
        raise PyMCSyntaxError(
            f"Invalid item '{item}'! Valid items: {', '.join(VALID_MC_ITEMS)} (add 'minecraft:' if needed)"
        )

def validate_block(block: str) -> None:
    """Check if a block ID is valid"""
    clean_block = block.replace("minecraft:", "")
    if clean_block not in VALID_MC_BLOCKS:
        raise PyMCSyntaxError(
            f"Invalid block '{block}'! Valid blocks: {', '.join(VALID_MC_BLOCKS)}"
        )

def validate_operator(operator: str) -> None:
    """Check if a comparison operator is valid (for if/loop logic)"""
    if operator not in VALID_OPERATORS:
        raise PyMCValidationError(
            f"Invalid operator '{operator}'! Valid operators: {', '.join(VALID_OPERATORS)}"
        )

def validate_loop_bounds(start: int, end: int, step: int) -> None:
    """Prevent infinite loops (critical for MC!)"""
    if step == 0:
        raise PyMCValidationError("Loop step cannot be 0 (infinite loop!)")
    if (step > 0 and start > end) or (step < 0 and start < end):
        raise PyMCValidationError(f"Loop bounds invalid: start={start}, end={end}, step={step} (will never end)")