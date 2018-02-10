import Adafruit_ADS1x15, datetime, time

from firebase import firebase
#firebase = firebase.FirebaseApplication('https://muscle-bike.firebaseio.com/', None)

adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

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
    #res = firebase.put('piData-1',str(z),{'Distance':'nil','Muscle':str(values[0])})
    #res2 = firebase.put('live','muscle-left',values[0])
    current = datetime.datetime.now()
    elapsed = current - start
    print int(elapsed.total_seconds() * 1000)
    print('      {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
    # Pause for half a second.
    time.sleep(0.06)
