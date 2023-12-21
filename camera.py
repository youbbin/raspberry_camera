import time
import requests
from picamera2 import Picamera2
import os

server_url = 'http://192.168.0.2:8888/ceiling/image/upload'

fixed_exposure_value = 100

camera = Picamera2()
controls = {"ExposureTime": 2000}
preview_config = camera.create_preview_configuration(main={"size":(2000,1000)}, controls=controls)
capture_config = camera.create_still_configuration()
camera.configure(preview_config)
camera.start()
time.sleep(2)

try:
    while True:
        current_time = time.strftime("%Y%m%d_%H%M%S")
        folder_name = time.strftime("%Y%m%d")
        folder_path = f"/home/raspberrypi/test_folder/{folder_name}"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)


        file_extension = "jpg"
        file_name = f"{current_time}.{file_extension}"
        image_path = os.path.join(folder_path, file_name)
        metadata = camera.capture_file(image_path)
        print(metadata)

        # metadata = camera.switch_mode_and_capture_file(capture_config,image_path)
        with open(image_path, 'rb') as image_file:
            files = {'file': open(image_path, 'rb')}
            response = requests.post(server_url, files=files)
            print("image send")
            print(response)
            if response.status_code == 200:
                os.remove(image_path)
            else :
                print("error!")
            time.sleep(60)

except KeyboardInterrupt:
    camera.close()
    print(" KeyboardInterrupt")

