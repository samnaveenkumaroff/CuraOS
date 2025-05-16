import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.check_device import get_device

def test_device_check():
    device = get_device()
    assert device is not None
    print(f"[TEST] Device is: {device}")
    
if __name__ == "__main__":
    test_device_check()
