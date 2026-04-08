# Focusbuddy-AI
# Focusbuddy-AI

An IoT-based focus tracking and parental control system that helps users maintain productive study sessions through hardware monitoring and web-based management.

## Description

Focusbuddy-AI combines an ESP32 microcontroller with sensors and a Flask web server to monitor user focus during study sessions. The system detects distractions, enforces timed sessions, and provides parental controls through password-protected phone unlocking. It aims to reduce interruptions and improve productivity by providing real-time feedback and secure access management.

## Key Features

- **Real-time Focus Monitoring**: Uses IR proximity and capacitive touch sensors to detect user presence and potential distractions
- **Audible Alerts**: Buzzer notifications for detected distractions
- **OLED Display**: Visual status updates on the ESP32 device
- **Web Dashboard**: Intuitive interface for timer setup, password management, and session control
- **Parental Controls**: Encrypted password storage with unlock only after session completion
- **Session Timer**: Configurable study durations with automatic completion
- **WiFi Connectivity**: Seamless data transmission between hardware and server

## Technologies Used

### Backend
- **Flask**: Web framework for API and dashboard
- **Flask-CORS**: Cross-origin resource sharing
- **Cryptography (Fernet)**: Password encryption
- **Python**: Core server logic

### Frontend
- **HTML5**: Dashboard structure
- **Vanilla JavaScript**: Client-side interactivity
- **Fetch API**: HTTP communication

### Hardware/Firmware
- **ESP32**: Microcontroller platform
- **WiFi**: Network connectivity
- **I2C/OLED**: Display interface
- **Analog/Capacitive Sensors**: Input detection
- **PWM Audio**: Buzzer control

### Infrastructure
- **Git**: Version control
- **Python Virtual Environment**: Dependency management

## Installation

### Prerequisites
- Python 3.7+
- ESP32 development board
- Arduino IDE or ESP-IDF for firmware upload
- WiFi network access

### Server Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Focusbuddy-AI
   ```

2. **Set up Python virtual environment**:
   ```bash
   cd server
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**:
   ```bash
   python app.py
   ```
   The server will start on `http://localhost:5000`

### Hardware Setup

1. **ESP32 Connections**:
   - IR Sensor OUT → Pin 34
   - Buzzer → Pin 25
   - Capacitive Touch → Pin 13 (T4)
   - OLED Display: I2C (SDA: 21, SCL: 22)

2. **Upload Firmware**:
   - Open `firmware/main esp32.txt` in Arduino IDE
   - Install required libraries: WiFi, HTTPClient, Wire, Adafruit_SSD1306
   - Update WiFi credentials and server IP in the code
   - Upload to ESP32 board

3. **Network Configuration**:
   - Ensure ESP32 and server are on the same WiFi network
   - Update `server_url` in firmware with correct server IP address

## Usage

1. **Access Dashboard**: Open `http://localhost:5000` in a web browser

2. **Set Parental Password**:
   - Enter password in the "Phone Unlock" section
   - Click "Save" to encrypt and store

3. **Start Study Session**:
   - Set desired minutes in the timer input
   - Click "Start Study" to begin
   - Phone becomes locked during session

4. **Monitor Progress**:
   - View real-time status on OLED display
   - Check timer countdown on dashboard
   - Receive alerts for distractions

5. **End Session**:
   - Session completes automatically or manually via "End Study"
   - Password unlocks phone upon completion

## API Endpoints

- `GET /`: Dashboard page
- `POST /upload`: Receive state from ESP32
- `POST /start_session`: Start timed session
- `POST /end_session`: End current session
- `POST /set_password`: Save encrypted password
- `GET /get_password`: Retrieve password (if unlocked)
- `GET /status`: Current session status
- `GET /timer`: Timer information

## Future Improvements

- **Camera Integration**: Add computer vision for advanced distraction detection (facial recognition, eye-tracking, object detection)
- **AI/ML Features**: Emotion recognition, posture analysis, and automated session adjustments
- **Multi-device Support**: Support for multiple ESP32 units or additional sensors
- **Cloud Integration**: Remote monitoring and analytics
- **Mobile App**: Companion app for enhanced control and notifications

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open-source. Please check the license file for details.
