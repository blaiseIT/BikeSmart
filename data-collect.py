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
auth = firebase.auth()
db = firebase.database()

adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1
left = 0
right = 20000
counter = 0

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
    print('      {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
    # Pause for half a second.

    left += values[0]#left
    right += values[1] #rich        
    if counter % 10 == 9:
        print (100*left/(left+right))    #this is left power percent
        print (left+right)/4000      #This is muscle %
        #print last_cadence
        data = {"cadence": counter, "balance": (100*left/(left+right)), "muscle": (left+right)/4000}
    db.child("livetest").set(data)
        left=0
        right=0
    else:
        time.sleep(0.06)
    counter += 1
