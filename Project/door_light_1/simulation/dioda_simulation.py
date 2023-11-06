import random
import time


def generate_values():
    while True:
        rnd = random.randint(0, 1)
        if(rnd == 1):
            print("Led is on")
        else:
            print("Led is off")
        time.sleep(1)

