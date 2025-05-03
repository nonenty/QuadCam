from camera import ShowcaseCamera
import json
import base64

if __name__ == '__main__':
    with open('definitions2.json','r') as f:
        data=json.load(f)
        cam = ShowcaseCamera(data)
        cam.plus_one()
        pass