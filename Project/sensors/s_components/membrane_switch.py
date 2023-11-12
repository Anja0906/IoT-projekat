import time
import RPi.GPIO as GPIO


def detect_motion(code, c1, c2, c3, c4, r1, r2, r3, r4):
    R1 = int(r1)
    R2 = int(r2)
    R3 = int(r3)
    R4 = int(r4)

    C1 = int(c1)
    C2 = int(c2)
    C3 = int(c3)
    C4 = int(c4)

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(R1, GPIO.OUT)
    GPIO.setup(R2, GPIO.OUT)
    GPIO.setup(R3, GPIO.OUT)
    GPIO.setup(R4, GPIO.OUT)

    GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


    def read_line(line, characters):
        GPIO.output(line, GPIO.HIGH)
        if GPIO.input(C1) == 1:
            print(characters[0])
        if GPIO.input(C2) == 1:
            print(characters[1])
        if GPIO.input(C3) == 1:
            print(characters[2])
        if GPIO.input(C4) == 1:
            print(characters[3])
        GPIO.output(line, GPIO.LOW)

        try:
            while True:
                read_line(R1, ["1", "2", "3", "A"])
                read_line(R2, ["4", "5", "6", "B"])
                read_line(R3, ["7", "8", "9", "C"])
                read_line(R4, ["*", "0", "#", "D"])
                time.sleep(0.2)
        except KeyboardInterrupt:
            print("\nApplication stopped!")
