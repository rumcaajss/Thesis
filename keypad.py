import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

MATRIX = [[1,2,3,'A'],
          [4,5,6,'B'],
          [7,8,9,'C'],
          ['*',0,'*', 'D']]
ROW = [17,27,22,10]
COL = [25,8,7,1]
print MATRIX[2]
for j in range(4):
    GPIO.setup(COL[j], GPIO.OUT)
    GPIO.output(COL[j],1)
for i in range(4):
    GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)
try:
    while(True):
        for j in range(4):
            GPIO.output(COL[j],0)
            for i in range(4):
                if GPIO.input(ROW[i])==0:
                    if (MATRIX[i][j]=='A'):
                        print('siema')
                    elif(MATRIX[i][j]=='B'):
                        print('BENG!')
                    else:
                        print('lel')
                    time.sleep(0.2)
                    while(GPIO.input(ROW[i])==0):
                        pass
            GPIO.output(COL[j],1)
except KeyboardInterrupt:
    GPIO.cleanup()
