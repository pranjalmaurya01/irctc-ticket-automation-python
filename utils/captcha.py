import base64
import os
import subprocess
import sys

CAPTCHA_FILE_NAME = 'tmp-captcha.png'


def solve_captcha(captcha_src_base64: str, method='GOCR') -> str:
    base64_img = captcha_src_base64.split(',')[1]
    img_data = base64.b64decode(base64_img)
    with open(CAPTCHA_FILE_NAME, 'wb') as f:
        f.write(img_data)

    try:
        result = subprocess.run(['gocr', CAPTCHA_FILE_NAME],
                                capture_output=True, text=True, check=True)
        captcha_txt = result.stdout.strip()
        os.remove(CAPTCHA_FILE_NAME)
        return captcha_txt
    except Exception as e:
        print("GOCR not found on system please install to continue", e)
        sys.exit()
