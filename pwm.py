import RPi.GPIO as io
io.setmode(io.BCM)

in1_pin=18
io.setup(in1_pin,io.OUT)

def ste(property, value):
    try:
        f=open("/sys/clss/rpi-pwm/pwm0/" + property, 'w')
        f.write(value)
        f.close()
    except:
        print("Error writing")
        
set(["delayed", "0"])
set(["mode", "pwm"])
set(["frequency", "500"])
set(["active","1"])

def clockwise():
    io.output(in1_pin, True)
    
clockwise()

while True:
    cmd=raw_input("Command:")
    speed=int(cmd[0])*11
    set(["duty", str(speed)])
