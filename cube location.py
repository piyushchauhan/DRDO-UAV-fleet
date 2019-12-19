[12:37 AM, 12/20/2019] IITP Ayush EE: import numpy as np
import math

def  cubeLoc(alpha,beta,head,h,theta_c,theta_p,lat,lon):
    
    x_dash = (alpha*h*math.tan(math.pi*25/180))/640
    y_dash = h*( 1/math.tan((theta_c+theta_p)math.pi/180) - beta(1/math.tan((theta_p+theta_c)*math.pi/180) - 1/math.tan((theta_c+theta_p+15)*math.pi/180))/360)

    #After considering axis of rotation
    x = x_dash*math.cos(head) - y_dash*math.sin(head)
    y = x_dash*math.sin(head) + y_dash*math.cos(head)
    
    c, s = np.cos(head), np.sin(head)
    R = np.array(((c,-s), (s, c)))
    x = R[0][0]*x_dash + R[0][1]*y_dash
    y = R[1][0]*x_dash + R[1][1]*y_dash
    
    #Merging above to GPS coordinates
    lat_final = lat + (x*0.00000898311)
    lon_final = lon + (y*0.00001268282)
    
    print (lat_final)
    print(lon_final)
