import time
seconds = input("ddd")
startTime=time.time()
finishTime=startTime+seconds
while(time.time()<finishTime):
    print time.time()
    print "."
    time.sleep(1)
print "damn"
