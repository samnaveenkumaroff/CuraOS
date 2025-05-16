# src/utils/check_device.py

import torch

def get_device():
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print(f"[INFO] GPU Available: {torch.cuda.get_device_name(0)}")
    else:
        device = torch.device("cpu")
        print("[INFO] No GPU found. Using CPU.")
    return device

if __name__ == "__main__":
    device = get_device()
