"""ANSI color utilities for terminal output."""


class Colors:
    """ANSI color codes for terminal formatting."""
    
    # Color codes
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    MAGENTA = '\033[0;35m'
    CYAN = '\033[0;36m'
    WHITE = '\033[0;37m'
    
    # Additional color variants (from oak-insights)
    HEADER = '\033[95m'
    
    # Formatting
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    
    # Reset
    RESET = '\033[0m'
    END = '\033[0m'  # Alias for RESET (compatibility)
    
    @classmethod
    def disable(cls):
        """Disable all colors (for --no-color flag)."""
        for attr in dir(cls):
            if not attr.startswith('_') and attr.isupper():
                setattr(cls, attr, '')
