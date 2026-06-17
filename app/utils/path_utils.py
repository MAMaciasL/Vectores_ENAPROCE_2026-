import os
import sys

def resource_path(rel_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.abspath(os.path.join(base_path, "..", ".."))

    return os.path.join(base_path, rel_path)