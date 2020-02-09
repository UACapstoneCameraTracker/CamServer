# CamServer

Accessing the usb camera on raspberry pi.

checking pi's ip address:
ifconfig

my: 
inet 192.168.1.71

Method 1: Using service motion, (sudo apt-get install motion ) 
1) sudo service motion restart
2) sudo motion
3) in a browser type: 192.168.1.71:8081 to access video feed
or 192.168.1.71:8080 for managing
4) sudo service motion stop

problem: really low rate or missing frame, long delay

Method 2: Using fswebcam to take screen shot
make sure previous daemon has stopped
1)sudo fswebcam test_image.jpg
or 
1) ./webcamshot.sh 
which is located in /Desktop/PiCameraServer/test
