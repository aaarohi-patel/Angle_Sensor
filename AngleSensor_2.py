import RPi.GPIO as GPIO
import pickle
# Import the MPU6050 class from the MPU6050.py file
from mpu6050 import mpu6050
#from machine import Pin, I2C
from time import sleep

# AccelGyro pin connection information
# AccelGyro SCL connect to the pin# 5
# AccelGyro SDA connect to the pin# 3
# AccelGyro connet pin 1 to VCC
# AccelGyro connet pin 6 to ground

sensor = mpu6050(0x68)
accelDataList = []
calibAccelDataList = []
gyroDataList = []

def get_values(n_samples=100):
    result = []
    for _ in range(n_samples):
        sleep(0.01)
        accelData = sensor.get_accel_data()
        gyroData = sensor.get_gyro_data()
        tempData = sensor.get_temp()
        result.append({ 'AccelX' :round(accelData['x'],2), 'AccelY':round(accelData['y'],2), 'AccelZ':round(accelData['z'],2),
                      'GyroX' :round(gyroData['x'],2), 'GyroY':round(gyroData['y'],2), 'GyroZ':round(gyroData['z'],2),
                       'Temp':round(tempData,2)
                      })
        
    return result


def calibrate(threshold=50, n_samples=100):
    """
    Get calibration date for the sensor, by repeatedly measuring
    while the sensor is stable. The resulting calibration
    dictionary contains offsets for this sensor in its
    current position.
    """
    while True:
        v1 = get_values(n_samples=1)[0]
        v2 = get_values(n_samples=1)[0]
        # Check all consecutive measurements are within
        # the threshold. We use abs() so all calculated
        # differences are positive.
        if all(abs(v1[k] - v2[k]) < threshold for k in v1.keys()):
            return v1  # Calibrated.


def get_smoothed_values(n_samples=10, calibration=None):
    """
    Get smoothed values from the sensor by sampling
    the sensor `n_samples` times and returning the mean.

    If passed a `calibration` dictionary, subtract these
    values from the final sensor value before returning.
    """
    result = {}
    for _ in range(n_samples):
        valueList = get_values(n_samples=1)
        #accelDataList.append(valueList)
        data = valueList[0]

        for k in data.keys():
            # Add on value / n_samples to produce an average
            # over n_samples, with default of 0 for first loop.
            result[k] = result.get(k, 0) + (data[k] / n_samples)

    
    if calibration:
        # Remove calibration adjustment.
        for k in calibration.keys():
            result[k] -= calibration[k]

    return result


def map(value, inMin, inMax, outMin, outMax):
    return int( outMin + (outMax-outMin) * ((value-inMin)/(inMax-inMin))) 


def cleanBoard():
    print("Cleaning up!")
    # Release resources - clean up the board setting
    GPIO.cleanup()
    
def GetAccelerator():
    accel_data = sensor.get_accel_data()
    print("Accelerometer data")
    print("x: " + str(round(accel_data['x'],2)))
    print("y: " + str(round(accel_data['y'],2)))
    print("z: " + str(round(accel_data['z'],2)))
    accelDataList.append([round(accel_data['x'],2),round(accel_data['y'],2),round(accel_data['z'],2)])
    
    if len(accelDataList) > 2:
        print(accelDataList[-2])
        print(accelDataList[-1])
        diffX = accelDataList[-2][0] - accelDataList[-1][0]
        if abs(diffX) > 5:
             if diffX < 0:
                print("Person tilted backward by :"+ str(abs(diffX))) 
             else:
                print("Person tilted forward by :"+ str(abs(diffX)))
            
    
    
def GetGyro():
    gyro_data = sensor.get_gyro_data()
    print("Gyroscope data")
    print("x: " + str(round(gyro_data['x'],2)))
    print("y: " + str(round(gyro_data['y'],2)))
    print("z: " + str(round(gyro_data['z'],2)))
    gyroDataList.append([round(gyro_data['x'],2), round(gyro_data['y'],2), round(gyro_data['z'],2)])
    
    #print(map(round(gyro_data['x'],2), -17000, 17000, 0, 255))
    
    if len(gyroDataList) > 2:
        #print(gyroDataList[-2])
        #print(gyroDataList[-1])
        diffX = gyroDataList[-2][0] - gyroDataList[-1][0]
        if abs(diffX) > 5:
             if diffX < 0:
                print("?? :"+ str(abs(diffX))) 
             else:
                print("??lll :"+ str(abs(diffX)))
    

def GetTemp():
    temp = sensor.get_temp()
    print("Temp: " + str(round(temp,2)) + " C")
       

def TestGyroAccelerator():
    sensor.set_accel_range(sensor.ACCEL_RANGE_16G)
    sensor.set_gyro_range(sensor.GYRO_RANGE_2000DEG)
    print("Accel Range:"+str(sensor.read_accel_range(raw = False)))
    print("Gyro Range:"+str(sensor.read_gyro_range(raw = False)))
    try:  
        while True:
        #for i in range(5):
            calibrateData= calibrate()
            data = get_smoothed_values(n_samples=100, calibration=None)
            print('\t'.join('{0}:{1:>10.1f}'.format(k, data[k]) for k in sorted(data.keys())),  end='\r')
            #calibAccelDataList.append(data)
    except KeyboardInterrupt:
        None        
        
    '''
    while True:
        GetAccelerator()
        #GetGyro()
        sleep(1.5)
    '''

# main part
if __name__ == "__main__":
    accelDataList.clear()
    calibAccelDataList.clear()
    TestGyroAccelerator()
    '''
    with open("AccelData.txt","w") as outfile:
        outfile.write("\n".join(str(item) for item in accelDataList))
        outfile.write("\n calibrated data \n")
        outfile.write("\n".join(str(item) for item in calibAccelDataList))
    #cleanBoard()
    '''
       
    
