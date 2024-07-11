import numpy as np
import math as mt
import pyrealsense2 as rs
import cv2

k = 29
rad = mt.radians(k)
pxtheta = rad/240
print(pxtheta)
pxk = mt.degrees(pxtheta)
print(pxk)

i=1
cos0 = np.arange(480 ,dtype=float)
cos=np.cos(rad)
cos0[0] = cos
r=rad-pxtheta
while 480>i:    
    r=r-pxtheta
    cos=np.cos(r)
    cos0[i]=cos
    i = i+1


config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 15)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)
 
pipeline = rs.pipeline()
pipeline.start(config)
 
align_to = rs.stream.color
align = rs.align(align_to)

try:
    while True:
        frames = pipeline.wait_for_frames()

        aligned_frames = align.process(frames)

        color_frame = aligned_frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
 
        depth_frame = aligned_frames.get_depth_frame()
        depth_image = np.asanyarray(depth_frame.get_data())        
 
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.02), cv2.COLORMAP_JET)

        distance=np.arange(640,480,dtype=float)
        i = 1
        j = 1
        while i < 481:
                while j < 641:
                        distance[i-1][j-1] = depth_frame.get_distance(j, i)
                        depth_str = str(round(depth_data[i][j], 2)) + "m"
                        cv2.drawMarker(depth_colormap, (j,i), (0,0,255))
                        cv2.putText(depth_colormap, depth_str, (j,i), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), thickness=2)
                        j = j + 1
                i = i + 1
                j = 1
        images = np.hstack((color_image, depth_colormap))
        #
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        #
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
finally:
    #
    pipeline.stop()