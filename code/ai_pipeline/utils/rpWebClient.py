import cv2
import requests
import base64
import numpy as np

class RPClient():
    def __init__(self, ip="192.168.8.122"):
        self.ip = ip

    def getImage(self):
        response = requests.get(f"http://{self.ip}:40324/image", timeout = None )
        data = response.json()

        if data[ "error" ] == "None":
            img_bytes = base64.b64decode(data['img'])
            img_np = np.frombuffer(img_bytes, dtype=np.uint8)
            img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
            
            img = cv2.rotate( img, cv2.ROTATE_90_CLOCKWISE )
            img = cv2.rotate( img, cv2.ROTATE_90_CLOCKWISE )
            img = cv2.rotate( img, cv2.ROTATE_90_CLOCKWISE )

            config_response = requests.get(f"http://{self.ip}:40324/config")
            config_data = config_response.json()

            return { "img": img, "config": config_data, "error": "None" }
        else:
            return { "img": None, "config": None, "error": data[ "error" ] }

if __name__ == "__main__":
    r = RPClient()

    import time

    start = time.time()
    c = r.getImage()
    end = time.time()
    print( end - start )
