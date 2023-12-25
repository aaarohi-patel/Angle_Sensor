# Import the MPU6050 class from the MPU6050.py file
from mpu6050 import mpu6050
#from machine import Pin, I2C
from time import sleep
 
#i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
# Create a new instance of the MPU6050 class

# pin connection information
# SCL connect to the pin# 5
# SDA connect to the pin# 3
# connet pin 1 to VCC
# connet pin 6 to ground

#sensor = MPU6050(i2c)
sensor = mpu6050(0x68)
 
while True:
    accel_data = sensor.get_accel_data()
    gyro_data = sensor.get_gyro_data()
    temp = sensor.get_temp()
 
    #print("Accelerometer data")
    #print("x: " + str(round(accel_data['x'],2)))
    #print("y: " + str(round(accel_data['y'],2)))
    #print("z: " + str(round(accel_data['z'],2)))
 
    print("Gyroscope data")
    print("x: " + str(round(gyro_data['x'],2)))
    print("y: " + str(round(gyro_data['y'],2)))
    print("z: " + str(round(gyro_data['z'],2)))
 
    print("Temp: " + str(round(temp,2)) + " C")
    sleep(1.5)
 