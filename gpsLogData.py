import datetime

import cv2
import numpy as np

from cubeDetect import process, videoProcess
from dronekit import connect


'''
Get the following in the channel
- Timestamp
- GPS Global position of Drone(Lat,Long,Alt)
- GPS Local position of Drone (North,East,Down)
- Heading
- Pitch
- Number of Cubes detected
- Coordinates of the detected cube
'''


def videoProcess(feed=0):
    cap = cv2.VideoCapture(feed)
    while (cap.isOpened()):
        ret, frame = cap.read()
        numCubes, cubeCenters = process(frame)
        fps = cap.get(cv2.CAP_PROP_FPS)
        if cv2.waitKey(int(fps)) & 0xff == ord('q'):
            break
        file.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(datetime.datetime.now(), "", vehicle.location.global_relative_frame.lat,
                                                                      vehicle.location.global_relative_frame.lon, vehicle.location.global_relative_frame.alt,
                                                                      vehicle.location.local_frame.north, vehicle.location.local_frame.east, vehicle.location.local_frame.down,
                                                                      vehicle.attitude.pitch, vehicle.attitude.roll, vehicle.attitude.yaw, vehicle.heading, numCubes, cubeCenters))
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    vehicle = connect('192.168.43.23:14550', baud=921600, wait_ready=True)
    file = open("/home/pi/final.csv", "a+")
    videoProcess()
    file.close()
