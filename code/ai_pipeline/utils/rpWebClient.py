import cv2
import requests
import base64
import numpy as np

class RPClient():
    def __init__(self, ip="192.168.8.111"):
        self.ip = ip

    def getImage(self):
        response = requests.get(f"http://{self.ip}:5000/image", timeout = None )
        data = response.json()
        img_bytes = base64.b64decode(data['img'])
        img_np = np.frombuffer(img_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        config_response = requests.get(f"http://{self.ip}:5000/config")
        config_data = config_response.json()

        return img, config_data

if __name__ == "__main__":
    r = RPClient()
    i, c = r.getImage()
    print(c)

    import matplotlib.pyplot as plt

    plt.imshow(cv2.cvtColor(i, cv2.COLOR_BGR2RGB))
    plt.show()