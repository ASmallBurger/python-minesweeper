from ui import run_app
import sys


if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
if __name__ == "__main__":
    run_app()