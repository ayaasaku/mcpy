class MCPyError(Exception):
    """Base error for all PyMC library errors (parent class)"""
    pass

class MCPySyntaxError(MCPyError):
    """Error for invalid MC syntax (e.g., bad selector, invalid item ID)"""
    pass

class MCPyValidationError(MCPyError):
    """Error for invalid logic (e.g., infinite loop, duplicate variable name)"""
    pass

VALID_MC_ITEMS = {"diamond", "iron_sword", "golden_apple", "stick", "stone", "dirt", "grass_block"}
VALID_MC_BLOCKS = {"stone", "dirt", "grass_block", "cobblestone", "oak_planks"}
VALID_MC_SELECTORS = {"@a", "@p", "@s", "@e", "@r"}
VALID_OPERATORS = {"==", "!=", "<", ">", "<=", ">="}