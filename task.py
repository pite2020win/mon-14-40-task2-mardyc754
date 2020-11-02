import random, time

def tilt_correction():
  while True:
    rate_of_correction = random.randint(10,100)/10
    tilt = random.randint(-10,10)
    print(f"Current orientation: {tilt} degrees")
    print("Tilt correction:")  
    time.sleep(0.5)
    tilt -= random.gauss(0, 2*rate_of_correction)
    print(f"Plane tilt: {tilt} degrees")
    time.sleep(1)

tilt_correction()
