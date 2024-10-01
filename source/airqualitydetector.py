import time
import board
import adafruit_dht # this library is used for Dht11 sensor
import RPi.GPIO as GPIO
import serial # used for co2 sensor
import requests 
from gpiozero import LED
from threading import Thread

# ThingSpeak API configuration
THINGSPEAK_API_KEY = '0RH3YYBQLXAGHXHY'
THINGSPEAK_URL = 'https://api.thingspeak.com/update'

# GPIO setup
GPIO.setmode(GPIO.BCM)  # Set GPIO pin numbering mode
DO_PIN = 12
GPIO.setup(DO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Configure gas sensor pin
dht_sensor = adafruit_dht.DHT11(board.D16)  # Configure DHT11 sensor for temperature and humidity
BUZZER_PIN = 21
GPIO.setup(BUZZER_PIN, GPIO.OUT)  # Configure buzzer pin
green_led = LED(17)  # Configure green LED pin
blue_led = LED(27)  # Configure blue LED pin
red_led = LED(22)  # Configure red LED pin

# Dictionary to store sensor data
sensor_data = {
    "gas_state": 0,
    "temperature": 0.0,
    "humidity": 0.0,
    "co2": 0,
    "air_quality": "Unknown",
    "health_implications": "Unknown"
}

def buzz(pitch, duration):
    """Function to control the buzzer"""
    period = 1.0 / pitch  # Calculate period of the sound wave
    delay = period / 2  # Calculate delay for half period
    cycles = int(duration * pitch)  # Calculate number of cycles
    for i in range(cycles):
        GPIO.output(BUZZER_PIN, True)  # Turn on buzzer
        time.sleep(delay)  # Wait for half period
        GPIO.output(BUZZER_PIN, False)  # Turn off buzzer
        time.sleep(delay)  # Wait for half period

def categorize_co2_level(co2):
    """Function to categorize CO2 levels"""
    if co2 <= 1000:
        return "Excellent", "Optimal air quality; no adverse health effects."
    elif co2 <= 1800:
        return "Good", "Generally comfortable; minor effects possible for some."
    else:
        return "Unhealthy", "Discomfort and potential health risks."

def control_leds(air_quality):
    """Function to control LEDs based on air quality"""
    green_led.off()
    blue_led.off()
    red_led.off()
    if air_quality == "Excellent":
        green_led.on()
    elif air_quality == "Good":
        blue_led.on()
    else:
        red_led.on()

def send_to_thingspeak():
    """Thread function to send data to ThingSpeak"""
    while True:
        response = requests.post(THINGSPEAK_URL, data={
            'api_key': THINGSPEAK_API_KEY,
            'field1': sensor_data['gas_state'],
            'field2': sensor_data['temperature'],
            'field3': sensor_data['humidity'],
            'field4': sensor_data['co2']
        })
        if response.status_code != 200:
            print("Failed to send data to ThingSpeak")
        time.sleep(30)

def read_gas_sensor():
    """Thread function to read gas sensor data"""
    while True:
        gas_present = GPIO.input(DO_PIN)  # Read gas sensor input
        sensor_data['gas_state'] = 0 if gas_present == GPIO.HIGH else 1  # 0 = no gas, 1 = gas present
        print(f"Gas sensor state: {'Gas present' if sensor_data['gas_state'] else 'No gas'}")
        time.sleep(30)

def read_dht_sensor():
    """Thread function to read DHT11 sensor data"""
    while True:
        try:
            temperature_c = dht_sensor.temperature  # Read temperature
            humidity = dht_sensor.humidity  # Read humidity
            sensor_data['temperature'] = temperature_c  # Update temperature in sensor_data
            sensor_data['humidity'] = humidity  # Update humidity in sensor_data
            print(f"Temperature: {temperature_c:.1f}C")
            print(f"Humidity: {humidity:.1f}%")
            if temperature_c > 25:
                buzz(1000, 5.0)  # Buzz if temperature is above 25C
            else:
                GPIO.output(BUZZER_PIN, GPIO.LOW)  # Turn off buzzer
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dht_sensor.exit()
            raise error
        time.sleep(30)

def read_co2_sensor():
    """Thread function to read CO2 sensor data"""
    ser = serial.Serial('/dev/serial0', 9600, timeout=1)  # Configure serial port for CO2 sensor
    while True:
        ser.flush()  # Flush the serial port
        ser.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")  # Send command to read CO2 level
        time.sleep(1)
        if ser.in_waiting > 0:
            response = ser.read(9)  # Read response from CO2 sensor
            if len(response) == 9 and response[0] == 0xff and response[1] == 0x86:
                co2 = response[2] * 256 + response[3]  # Calculate CO2 level
                air_quality, health_implications = categorize_co2_level(co2)  # Categorize CO2 level
                sensor_data['co2'] = co2  # Update CO2 level in sensor_data
                sensor_data['air_quality'] = air_quality  # Update air quality in sensor_data
                sensor_data['health_implications'] = health_implications  # Update health implications in sensor_data
                control_leds(air_quality)  # Control LEDs based on air quality
                print(f"CO2: {co2} ppm")
                print(f"Air Quality: {air_quality}")
                print(f"Health Implications: {health_implications}")
                print("-" * 80)  # Separator line
        time.sleep(30)

if __name__ == "__main__":
    try:
        # Create and start threads for each sensor and ThingSpeak
        gas_thread = Thread(target=read_gas_sensor)
        dht_thread = Thread(target=read_dht_sensor)
        co2_thread = Thread(target=read_co2_sensor)
        thingspeak_thread = Thread(target=send_to_thingspeak)

        gas_thread.start()
        dht_thread.start()
        co2_thread.start()
        thingspeak_thread.start()

        # Join threads to the main thread
        gas_thread.join()
        dht_thread.join()
        co2_thread.join()
        thingspeak_thread.join()
    except KeyboardInterrupt:
        print("Script stopped by user")
    finally:
        GPIO.cleanup()  # Clean up GPIO settings

