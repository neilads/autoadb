import cv2
import numpy as np
import subprocess
import os
from PIL import Image
from io import BytesIO

def capture_screen():
    try:
        subprocess.run(
            "adb shell screencap -p /sdcard/screen.png && adb pull /sdcard/screen.png ./screen.png && adb shell rm /sdcard/screen.png",
            shell=True, check=True, capture_output=True
        )
        with open("screen.png", "rb") as f:
            img_bytes = f.read()
        os.remove("screen.png")
        image = cv2.cvtColor(np.array(Image.open(BytesIO(img_bytes))), cv2.COLOR_RGB2BGR)
        return image
    except Exception:
        return None
