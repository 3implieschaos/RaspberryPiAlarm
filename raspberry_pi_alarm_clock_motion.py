#from multiprocessing import Process
import os
import glob
import time
import RPi.GPIO as io
from time import gmtime, sleep, strftime
from datetime import datetime
from subprocess import *

os.system('killall mpg321')

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
  


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
 #       timenow = str(datetime.now())             # .isoformat()
#        min = datetime.now().minute
        return temp_f #c, temp_f, timenow, min


io.setmode(io.BCM)

pir_pin=23

io.setup(pir_pin, io.IN)

motioncount=1

cmd2 = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"

def run_cmd(cmd):
        p = Popen(cmd, shell=True, stdout=PIPE)
        output = p.communicate()[0]
        return output

flag=0
ipaddr = run_cmd(cmd2)
if(ipaddr == ''):
	flag=1	


if(read_temp()<70):
	os.system("amixer --quiet set 'PCM',0 100%")
else:
	os.system("amixer --quiet set 'PCM',0 85%")

str1="Good morning Tim, it is time to wake up! The temperature is %0.1f "%read_temp()+" and it is time "+strftime("%H:%M", time.localtime())
if(flag==0):
	cmd='aplay /home/pi/alarm.wav; /home/pi/speech.sh '+str1+'; aplay /home/pi/alarm.wav'
else:
	cmd='aplay /home/pi/alarm.wav; echo '+str1+' | festival --tts; aplay /home/pi/alarm.wav'

while motioncount<=3:
	os.system(cmd)
	if io.input(pir_pin):
           stro = "'Proof "+str(motioncount)+" of three obtained.'"
	   cm2 = "echo "+stro+" | festival --tts"
	   os.system(cm2)
           motioncount=motioncount+1
	sleep(1)
        if io.input(pir_pin):
           stro = "'Proof "+str(motioncount)+" of three obtained.'"
           cm2 = "echo "+stro+" | festival --tts"
           os.system(cm2)
           motioncount=motioncount+1
        sleep(1)
        if io.input(pir_pin):
           stro = "'Proof "+str(motioncount)+" of three obtained.'"
           cm2 = "echo "+stro+" | festival --tts"
           os.system(cm2)
           motioncount=motioncount+1
        sleep(1)

if(flag==0):
	os.system("/home/pi/speech.sh Have a great day!")
else:	
	os.system("echo 'Have a great day' | festival --tts")

