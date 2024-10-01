# Air-quality-detector

## Overview
The Air Quality Detector is a real-time environmental monitoring system built using a Raspberry Pi and various sensors to track air quality parameters, including gas presence, temperature, humidity, and CO2 concentration. The system collects and analyzes data in real-time and visualizes it on the ThingSpeak platform, allowing users to monitor environmental conditions remotely. Alerts via LEDs and buzzers are triggered when significant changes are detected, making it a reliable tool for both real-time monitoring and remote analysis.

## Objectives and Goals
- Real-Time Data Collection: Continuously collect data on gas levels, temperature, humidity, and CO2 concentration using integrated sensors.
- Data Visualization: Visualize collected data intuitively on ThingSpeak, ensuring accessibility and clarity.
- User Alerts and Notifications: Integrate visual and audible alerts (LEDs and buzzers) to notify users of significant changes in real-time.
- System Robustness: Ensure the system operates reliably with thorough testing and resolution of any issues.
- User-Friendly Interface: Provide clear and descriptive visualizations with proper labels and legends for easy interpretation.
- Scalability and Future Integration: Design the system to be expandable for future sensor integration and enhanced monitoring capabilities.

## Features
- Multi-sensor integration: Gas sensor, DHT11 (temperature and humidity), and CO2 sensor (MH-Z19B)
- Real-time monitoring and data processing
- Air quality categorization based on CO2 levels
- Visual indicators using LED lights (Green: Excellent, Blue: Good, Red: Unhealthy)
- Audible alerts for high temperature conditions
- Data logging and visualization using ThingSpeak for remote monitoring and analysis
- Multi-threaded design for efficient sensor reading and data transmission

## Hardware Requirements
- Raspberry Pi (any model with GPIO pins)
- Gas sensor (connected via GPIO 12)
- DHT11 temperature and humidity sensor (connected via GPIO 16)
- CO2 sensor (MH-Z19B, connected via UART)
- LEDs (Green: GPIO 17, Blue: GPIO 27, Red: GPIO 22)
- Buzzer (connected via GPIO 21)

## Installation
1. Clone this repository:
   
        git clone https://github.com/yourusername/air-quality-detector.git
   
3. Install required Python packages:
python3 -m pip install RPi.GPIO adafruit-circuitpython-dht gpiozero pyserial requests
4. Set up your ThingSpeak account and replace the `THINGSPEAK_API_KEY` in the `airqualitydetector.py` script with your API key.

## Usage
Ensure all sensors and LEDs are connected to the correct GPIO pins as per the Hardware Requirements section.
Run the script with Python 3:

      python3 airqualitydetector.py

The system will start monitoring air quality parameters and:
- Display readings in the console
- Update LED indicators based on air quality
- Trigger the buzzer for high temperature alerts
- Send data to ThingSpeak every 30 seconds

## Implementation Details
### Connections
- Gas Sensor: Connected via GPIO pin 12
- DHT11: Connected via GPIO pin 16
- CO2 Sensor (MH-Z19B): Connected via UART

### Data Reading
- Gas Sensor: Digital input for gas detection (0: No gas, 1: Gas present)
- DHT11: Temperature (Celsius) and humidity (percentage) readings
- CO2 Sensor: CO2 concentration levels (measured in ppm)

### Code Overview
- Python scripts initialize the sensors and perform continuous data reading.
- Sensor data is processed in real-time, triggering visual and audible alerts when thresholds are exceeded.
- Periodic data transmission to ThingSpeak for remote monitoring and analysis.

## ThingSpeak Integration
### Data Transmission
- Data is uploaded to ThingSpeak periodically using HTTP POST requests through the ThingSpeak API.
- Sensor data for gas levels, temperature, humidity, and CO2 concentration is mapped to specific fields in ThingSpeak.

## API Configuration
- API Key: 0RH3YYBQLXAGHXHY (Channel is public)
- Data is transmitted to the following fields:
- Temperature
- Humidity
- Gas presence
- CO2 levels

## Data Interpretation
- Gas Sensor: Detects presence of gases (0: No gas, 1: Gas present)
- Temperature: Measured in Celsius
- Humidity: Measured as a percentage
- CO2 Levels:
  - ≤1000 ppm: Excellent (Green LED)
  - 1001-1800 ppm: Good (Blue LED)
  - 1800 ppm: Unhealthy (Red LED)

## Summary of Results
- Performance: Testing revealed the system operates reliably and accurately in real-world conditions, providing robust insights into environmental data.
- Data Insights: Comprehensive data collection from multiple sensors has given detailed insights into air quality, allowing for informed decision-making.

## User Experience Improvements
- Feedback Integration: User feedback led to enhancements in usability, including more intuitive features and improved interface design.
- User Engagement: Streamlined navigation and clearer data visualization have significantly improved user satisfaction and engagement.

## License
This project is licensed under the MIT License.

## From the Author

- *LinkedIn*: [Udayy Singh Pawar](https://www.linkedin.com/in/udayy-singh-pawar/)
- *GitHub*: [barrackmobamba69](https://github.com/barrackmobamba69)

### Contributors
- *LinkedIn*: [Sakshi Ojha](https://www.linkedin.com/in/sakshi-ojha-36b5b1224/)
- *LinkedIn*: [Pankaj Bhusal](https://www.linkedin.com/in/pankaj-bhusal/)

Feel free to reach out if you have any questions or suggestions!
