# [DeepX project] [coded by Bogdan Shklyar] [copyright (c) Covijn Ltd, 2017]
###################################
# for cancel programm press CTRL-C#
###################################
import picamera
import time
import io
from time import strftime
from sense_hat import SenseHat
import json

#loading SenseHat
sense = SenseHat()
sense.set_imu_config(True, True, True)

def loop():    
    #some values
    record_time = 5 * 60 #(5 min)change number of seconds that camera will be recording
    device_ID = "nd001"
    camera_ID = "nc001"
    camera_TP = "IP"
    curr_time = strftime ("%Y_%m_%d_%H:%M:%S")

    #starting record
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480) #camera resolution
        camera.framerate = 25 #camera framerate 
        time_start = strftime ("%Y_%m_%d_%H:%M:%S" + ".h264") 
        time_start_2 = strftime ("%H:%M:%S")
        #data dict for json
        data = {
            "date      ": strftime ("%Y-%m-%d"),
            "deviceID  ": device_ID,
            "cameraID  ": camera_ID,
            "cameraTP  ": camera_TP,
            "time_begin": time_start_2,
            "time_end  ": time_start_2
        }
        #creating json file
        file_name = 'pos:{0}_dev:{1}_cam:{2}.json'.format(strftime ("%Y_%m_%d_%H:%M:"), device_ID, camera_ID)
        
        with io.open(str(file_name), mode='a', encoding='utf-8')  as file:
            camera.start_recording(str(time_start))
            camera.start_preview() #coment this if you dn`t want look preview
             
        #open json file and wtite sensors data into it
        with open(str(file_name), mode='a')  as file:
            gps = io.open('gps.txt', 'r')#fake data for gps
            
            for i in range(record_time): #writing data in loop every second(changeable) as much as camera recording

                orientation = sense.get_orientation()
                d = ("{pitch}".format(**orientation), "{roll}".format(**orientation), "{yaw}".format(**orientation))

                gps_lat = gps.read(10)
                gps_lon = gps.read(10)
                
                curr_time = strftime ("%H:%M:%S")
                #sensors dict for json
                d_f_sens = {
                        "time" : curr_time,
                        "pitch" : d[0],
                        "roll" : d[1],
                        "yaw" : d[2]
                        }
                print (d_f_sens)
                file.write(json.dumps(d_f_sens, indent = 4, sort_keys=True))
                time.sleep(1) #cange for set the delay time data recording (1 sec by default)
            #stoping record   
            camera.stop_recording()
            print("recorded")
            time_end = strftime ("%H:%M:%S")
            data = {
            "date      ": strftime ("%Y-%m-%d"),
            "deviceID  ": device_ID,
            "cameraID  ": camera_ID,
            "cameraTP  ": camera_TP,
            "time_begin": time_start_2,
            "time_end  ": time_end 
                }
            #write header data to json
            file.write(json.dumps(data, indent = 2, sort_keys=True))
            file.close()
    loop()
#loop
circles = 1
if circles > 0:
    loop()

