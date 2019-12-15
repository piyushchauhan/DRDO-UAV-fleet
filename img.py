import datetime
import cv2
import numpy as np
# from dronekit import connect

# vehicle=connect('192.168.43.23:14550',baud=921600,wait_ready=True)

cap = cv2.VideoCapture(0)
# file = open("/home/pi/final.csv","a+")

while (cap.isOpened()):
#     file.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(datetime.datetime.now(),"No Cube","","",\
# vehicle.location.global_relative_frame.lat,vehicle.location.global_relative_frame.lon,vehicle.location.global_relative_frame.alt,\
# vehicle.location.local_frame.north,vehicle.location.local_frame.east,vehicle.location.local_frame.down,\
# vehicle.attitude.pitch,vehicle.attitude.roll,vehicle.attitude.yaw,vehicle.heading))
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([40,100,130])
    higher = np.array([85,170,250])

    lower_green = np.array([40,90,110])
    higher_green = np.array([95,200,250])

    mask = cv2.inRange(frame, lower_green, higher_green)
    mask_hsv = cv2.inRange(hsv, lower, higher)

    mask_sum = cv2.addWeighted(mask,0.5,mask_hsv,0.5,0)

    res = cv2.bitwise_and(frame, frame, mask = mask_hsv)

    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    noise_removal = cv2.bilateralFilter(gray,9,75,75)
    canny_image = cv2.Canny(mask_hsv,210,255)
    canny_image = cv2.convertScaleAbs(canny_image)

    noise_removal2 = cv2.blur(canny_image,(5,5))

    kernel = np.ones((3,3), np.uint8)
    dilated_image = cv2.dilate(noise_removal2,kernel,iterations=1)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    erosion = cv2.erode(dilated_image,kernel,iterations = 1)
    _, contours, h = cv2.findContours(dilated_image, 1, 2)
    contours= sorted(contours, key = cv2.contourArea, reverse = True)[:1]
    pt = (180, 3 * frame.shape[0] // 4)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.05*cv2.arcLength(cnt,True),True)
        M = cv2.moments(cnt)
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        
        if  len(approx)==6 or len(approx)==7:
            print ("Cube",'Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()),(cx,cy))
            cv2.drawContours(frame,[cnt],-1,(255,0,0),3)
            cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)
#             file.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(datetime.datetime.now(),"Cube",cx,cy,\
# vehicle.location.global_relative_frame.lat,vehicle.location.global_relative_frame.lon,vehicle.location.global_relative_frame.alt,\
# vehicle.location.local_frame.north,vehicle.location.local_frame.east,vehicle.location.local_frame.down,\
# vehicle.attitude.pitch,vehicle.attitude.roll,vehicle.attitude.yaw,vehicle.heading))

        else:
            print("NOCUBE")
#             file.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(datetime.datetime.now(),"No Cube","","",\
# vehicle.location.global_relative_frame.lat,vehicle.location.global_relative_frame.lon,vehicle.location.global_relative_frame.alt,\
# vehicle.location.local_frame.north,vehicle.location.local_frame.east,vehicle.location.local_frame.down,\
# vehicle.attitude.pitch,vehicle.attitude.roll,vehicle.attitude.yaw,vehicle.heading))

    fps = cap.get(5)
    if cv2.waitKey(int(fps)) & 0xff == ord('q'):
        break


cap.release()

# file.close()


cv2.destroyAllWindows()
