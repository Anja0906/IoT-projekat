import threading
import time
import random


class DHT(object):
    DHTLIB_OK = 0
    DHTLIB_ERROR_CHECKSUM = -1
    DHTLIB_ERROR_TIMEOUT = -2
    DHTLIB_INVALID_VALUE = -999

    DHTLIB_DHT11_WAKEUP = 0.020  # 0.018		#18ms
    DHTLIB_TIMEOUT = 0.0001  # 100us

    humidity = 0
    temperature = 0

    def __init__(self, pin, simulated):
        self.pin = pin
        self.bits = [0, 0, 0, 0, 0]
        self.simulated = simulated

    def readSensor(self, pin, wakeupDelay):
        mask = 0x80
        idx = 0
        self.bits = [0, 0, 0, 0, 0]
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(wakeupDelay)
        GPIO.output(pin, GPIO.HIGH)
        GPIO.setup(pin, GPIO.IN)

        loopCnt = self.DHTLIB_TIMEOUT
        t = time.time()
        while GPIO.input(pin) == GPIO.LOW:
            if (time.time() - t) > loopCnt:
                return self.DHTLIB_ERROR_TIMEOUT
        t = time.time()
        while GPIO.input(pin) == GPIO.HIGH:
            if (time.time() - t) > loopCnt:
                return self.DHTLIB_ERROR_TIMEOUT
        for i in range(0, 40, 1):
            t = time.time()
            while GPIO.input(pin) == GPIO.LOW:
                if (time.time() - t) > loopCnt:
                    return self.DHTLIB_ERROR_TIMEOUT
            t = time.time()
            while GPIO.input(pin) == GPIO.HIGH:
                if (time.time() - t) > loopCnt:
                    return self.DHTLIB_ERROR_TIMEOUT
            if (time.time() - t) > 0.00005:
                self.bits[idx] |= mask
            mask >>= 1
            if mask == 0:
                mask = 0x80
                idx += 1
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        return self.DHTLIB_OK

    def readDHT11(self):
        rv = self.readSensor(self.pin, self.DHTLIB_DHT11_WAKEUP)
        if rv != self.DHTLIB_OK:
            self.humidity = self.DHTLIB_INVALID_VALUE
            self.temperature = self.DHTLIB_INVALID_VALUE
            return rv
        self.humidity = self.bits[0]
        self.temperature = self.bits[2] + self.bits[3] * 0.1
        sumChk = ((self.bits[0] + self.bits[1] + self.bits[2] + self.bits[3]) & 0xFF)
        if self.bits[4] != sumChk:
            return self.DHTLIB_ERROR_CHECKSUM
        return self.DHTLIB_OK

    def parseCheckCode(self, code):
        if code == 0:
            return "DHTLIB_OK"
        elif code == -1:
            return "DHTLIB_ERROR_CHECKSUM"
        elif code == -2:
            return "DHTLIB_ERROR_TIMEOUT"
        elif code == -999:
            return "DHTLIB_INVALID_VALUE"

    def run_dht_loop(self, delay, stop_event):
        import RPi.GPIO as GPIO  # Make sure to import GPIO module
        while True:
            check = self.readDHT11()
            code = self.parseCheckCode(check)
            humidity, temperature = self.humidity, self.temperature
            self.callback(humidity, temperature, code)
            if stop_event.is_set():
                break
            time.sleep(delay)  # Delay between readings

    def dht_callback(self, humidity, temperature, code=None):
        t = time.localtime()
        print("=" * 20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code if code is not None else 'N/A'}")
        print(f"Humidity: {humidity}%")
        print(f"Temperature: {temperature}°C")

    def generate_values(self, initial_temp=25, initial_humidity=20):
        temperature = initial_temp
        humidity = initial_humidity
        while True:
            temperature = temperature + random.randint(-1, 1)
            humidity = humidity + random.randint(-1, 1)
            if humidity < 0:
                humidity = 0
            if humidity > 100:
                humidity = 100
            yield humidity, temperature

    def run_dht_simulator(self, delay, stop_event):
        for h, t in self.generate_values():
            time.sleep(delay)
            self.dht_callback(h, t)
            if stop_event.is_set():
                break

    def run(self, threads):
        stop_event = threading.Event()
        try:
            if self.simulated:
                print("Starting motion simulator")
                dht_thread = threading.Thread(target=self.run_dht_simulator, args=(2, stop_event))
                dht_thread.start()
                threads.append(dht_thread)
            elif not self.simulated:
                print("Starting motion loop")
                motion_thread = threading.Thread(target=self.run_dht_loop, args=(2, stop_event))
                motion_thread.start()
                threads.append(motion_thread)
            else:
                print("Self.simulated is none")
        except KeyboardInterrupt:
            for t in threads:
                stop_event.set()
