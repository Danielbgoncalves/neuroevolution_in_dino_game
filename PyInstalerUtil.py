import sys
import os

def resource_path(relative_path):
    """Retorna o caminho absoluto, compatível com PyInstaller."""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)