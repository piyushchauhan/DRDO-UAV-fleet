import cv2
import numpy as np

cap = cv2.VideoCapture('cubevideo.mp4')

while (cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow("true", frame)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow("HSV image", hsv)

    #gray = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("gray", gray)

    
    #ret,thresh_image = cv2.threshold(gray,180,255,cv2.THRESH_OTSU)
    #cv2.namedWindow("Image after Thresholding",cv2.WINDOW_NORMAL)
    # Creating a Named window to display image
    #cv2.imshow("Image after Thresholding",thresh_image)

    
    lower = np.array([40,100,130])
    higher = np.array([85,170,250])

    lower_green = np.array([20,80,15])
    higher_green = np.array([135,220,105])
    
    mask = cv2.inRange(frame, lower_green, higher_green)
    mask_hsv = cv2.inRange(hsv, lower, higher)

    mask_sum = cv2.addWeighted(mask,0.5,mask_hsv,0.5,0)
    
    res = cv2.bitwise_and(frame, frame, mask = mask_hsv)
    cv2.imshow("res", res)

    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray", gray)

    noise_removal = cv2.bilateralFilter(gray,9,75,75)
    cv2.namedWindow("Noise Removed Image",cv2.WINDOW_NORMAL)
     #Creating a Named window to display image
    cv2.imshow("Noise Removed Image",noise_removal)


    # Applying Canny Edge detection
    canny_image = cv2.Canny(mask_hsv,210,255)
    cv2.namedWindow("Image after applying Canny",cv2.WINDOW_NORMAL)
    # Creating a Named window to display image
    cv2.imshow("Image after applying Canny",canny_image)
    # Display Image
    canny_image = cv2.convertScaleAbs(canny_image)
    
    noise_removal2 = cv2.blur(canny_image,(5,5))
    cv2.namedWindow("Noise Removed Image2",cv2.WINDOW_NORMAL)
     #Creating a Named window to display image
    cv2.imshow("Noise Removed Image2",noise_removal2)
    
    '''
    indices = np.where(canny_image != [0])
    coordinates = zip(indices[0], indices[1])
    
    print('coordinates')
    '''
    

    


    # dilation to strengthen the edges
    kernel = np.ones((3,3), np.uint8)
    # Creating the kernel for dilation
    dilated_image = cv2.dilate(noise_removal2,kernel,iterations=1)
    cv2.namedWindow("Dilation", cv2.WINDOW_NORMAL)
    # Creating a Named window to display image
    cv2.imshow("Dilation", dilated_image)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    erosion = cv2.erode(dilated_image,kernel,iterations = 1)
    cv2.imshow('erosion', erosion)

    
    # Displaying Image
    contours, h = cv2.findContours(dilated_image, 1, 2)
    contours= sorted(contours, key = cv2.contourArea, reverse = True)[:1]
    pt = (180, 3 * frame.shape[0] // 4)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.05*cv2.arcLength(cnt,True),True)
        if  len(approx)==6 or len(approx)==7:
            print ("Cube")
            cv2.drawContours(frame,[cnt],-1,(255,0,0),3)
            cv2.putText(frame,'Cube', pt ,cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, [0,255, 255], 2)
    

    
    cv2.namedWindow("Shape", cv2.WINDOW_NORMAL)
    cv2.imshow('Shape',frame)
        
    corners    = cv2.goodFeaturesToTrack(mask_sum,6,0.06,25)
    corners    = np.float32(corners)
    for    item in    corners:
        x,y    = item[0]
        cv2.circle(erosion,(x,y),10,255,-1)
    cv2.namedWindow("Corners", cv2.WINDOW_NORMAL)
    cv2.imshow("Corners",erosion)
    
    fps = cap.get(5)
    if cv2.waitKey(int(fps)) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
