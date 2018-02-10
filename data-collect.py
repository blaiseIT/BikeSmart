import Adafruit_ADS1x15, datetime, time, pyrebase

config = {
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "projectId": "",
    "storageBucket": "",
    "messagingSenderId": ""
}
firebase = pyrebase.initialize_app(config)
auth    = firebase.auth()
db      = firebase.database()

adc     = Adafruit_ADS1x15.ADS1115()
GAIN    = 1
left    = 0
right   = 20000
counter = 0
cadence = [0]*5
ppm     = 600
lastMin = 0

print('Reading ADS1x15 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
print('-' * 37)

start = datetime.datetime.now()
while True:
    # Read all the ADC channel values in a list.
    values = [0]*4
    for i in range(4):
        values[i] = adc.read_adc(i, gain=GAIN)
    current = datetime.datetime.now()
    elapsed = current - start
    print int(elapsed.total_seconds() * 1000)
    print('{0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
    
    # Get the cadence
    case = counter%5
    if case == 0:
        cadence[0] = values[0]#latest min val1
        #check if cadence[3] is local min
        if (cadence[0]>cadence[3] and cadence[1]>cadence[3] and cadence[2]>cadence[3] and cadence[4]>cadence[3]):
            ppm = counter - lastMin
            lastMin = counter
    elif case == 1:
        cadence[1] = values[0]
        if (cadence[0]>cadence[4] and cadence[1]>cadence[4] and cadence[2]>cadence[4] and cadence[3]>cadence[4]):
            ppm = counter - lastMin
            lastMin = counter
    elif case == 2:
        cadence[2] = values[0]
        if (cadence[4]>cadence[0] and cadence[1]>cadence[0] and cadence[2]>cadence[0] and cadence[3]>cadence[0]):
            ppm = counter - lastMin
            lastMin = counter
    elif case == 3:
        cadence[3] = values[0]
        if (cadence[4]>cadence[1] and cadence[0]>cadence[1] and cadence[2]>cadence[1] and cadence[3]>cadence[1]):
            ppm = counter - lastMin
            lastMin = counter
    elif case == 4:
        cadence[4] = values[0]
        if (cadence[0]>cadence[2] and cadence[1]>cadence[2] and cadence[3]>cadence[2] and cadence[4]>cadence[2]):
            ppm = counter - lastMin
            lastMin = counter

    left += values[0]#left
    right += values[1] #rich        
    if counter % 10 == 9:
        print (100*left/(left+right))    #this is left power percent
        print (left+right)/4000      #This is muscle %
        #print last_cadence
        data = {"cadence": 600/ppm, "balance": (100*left/(left+right)), "muscle": (left+right)/4000}
        db.child("livetest").set(data)
        left=0
        right=0
	ppm=600
    else:
        time.sleep(0.06)
    counter += 1
