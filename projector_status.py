#!/usr/bin/env python3
"""
Projector RS232 Control Script
Connects to projector on COM10 and queries status
"""

import serial
import time

# Serial port configuration
PORT = 'COM10'
BAUDRATE = 9600
BYTESIZE = serial.EIGHTBITS
PARITY = serial.PARITY_NONE
STOPBITS = serial.STOPBITS_ONE
TIMEOUT = 2
XONXOFF = False
RTSCTS = False
DSRDTR = False

def send_command(ser, command):
    """Send a command to the projector and return response"""
    # Clear any existing data in buffer
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    # Add CR terminator if not present
    if not command.endswith('\r'):
        command += '\r'

    # Send command
    cmd_bytes = command.encode('ascii')
    print(f"Sending: {repr(command)} | Hex: {cmd_bytes.hex(' ')}")
    ser.write(cmd_bytes)
    ser.flush()

    # Wait for response with multiple attempts
    response = b''
    max_attempts = 10
    for i in range(max_attempts):
        time.sleep(0.1)
        waiting = ser.in_waiting
        if waiting > 0:
            response += ser.read(waiting)
            print(f"  Read {waiting} bytes: {repr(response)}")
            # If we got 'Ok' or 'P' or 'F', likely complete
            if b'Ok' in response or b'P' in response or b'F' in response:
                break
        else:
            if response:
                break  # Got some data, no more coming

    print(f"Received: {repr(response)} | Hex: {response.hex(' ') if response else 'empty'}")

    return response.decode('ascii', errors='ignore').strip()

def parse_system_info(response):
    """Parse ~00150 1 response: Okabbbbbccddddee"""
    if not response.startswith('Ok'):
        return None

    data = response[2:]  # Remove 'Ok' prefix

    if len(data) >= 13:
        info = {
            'power_status': 'On' if data[0] == '1' else 'Off',
            'lamp_hours': data[1:6],
            'input_source_code': data[6:8],
            'firmware_version': data[8:12],
            'picture_mode_code': data[12:14] if len(data) >= 14 else 'N/A'
        }

        # Decode input source
        source_map = {
            '07': 'HDMI 1',
            '20': 'Android (USB-A/SD Card/Home)'
        }
        info['input_source'] = source_map.get(data[6:8], f"Unknown ({data[6:8]})")

        # Decode picture mode
        mode_map = {
            '01': 'Presentation (PC)',
            '02': 'Bright',
            '03': 'Cinema',
            '04': 'sRGB',
            '14': 'Photo (Vivid)',
            '28': 'Eco',
            '29': 'iDevice'
        }
        info['picture_mode'] = mode_map.get(data[12:14], f"Unknown ({data[12:14]})")

        return info

    return None

def get_projector_status():
    """Connect to projector and get status"""
    try:
        # Open serial port
        print(f"Opening {PORT} at {BAUDRATE} baud...")
        ser = serial.Serial(
            port=PORT,
            baudrate=BAUDRATE,
            bytesize=BYTESIZE,
            parity=PARITY,
            stopbits=STOPBITS,
            timeout=TIMEOUT,
            xonxoff=XONXOFF,
            rtscts=RTSCTS,
            dsrdtr=DSRDTR
        )

        # Some devices need RTS/DTR signals
        ser.setRTS(True)
        ser.setDTR(True)
        time.sleep(0.2)

        print(f"Connected to {PORT}\n")

        # Query comprehensive system information
        print("=== Querying System Information ===")
        response = send_command(ser, '~00150 1')

        if response:
            info = parse_system_info(response)
            if info:
                print("\n=== Projector Status ===")
                print(f"Power Status:    {info['power_status']}")
                print(f"Lamp Hours:      {info['lamp_hours']}")
                print(f"Input Source:    {info['input_source']}")
                print(f"Firmware Ver:    {info['firmware_version']}")
                print(f"Picture Mode:    {info['picture_mode']}")
            else:
                print("Could not parse response")
        else:
            print("No response received")

        print("\n=== Querying Power State ===")
        response = send_command(ser, '~00124 1')
        if response:
            if response == 'Ok0':
                print("Power: OFF")
            elif response == 'Ok1':
                print("Power: ON")
            else:
                print(f"Response: {response}")

        print("\n=== Querying Input Source ===")
        response = send_command(ser, '~00121 1')
        if response:
            print(f"Input Source Response: {response}")

        print("\n=== Querying Software Version ===")
        response = send_command(ser, '~00122 1')
        if response:
            print(f"Software Version: {response}")

        # Close serial port
        ser.close()
        print("\nConnection closed.")

    except serial.SerialException as e:
        print(f"Serial port error: {e}")
        print("\nTrying with 115200 baud...")

        try:
            ser = serial.Serial(
                port=PORT,
                baudrate=115200,
                bytesize=BYTESIZE,
                parity=PARITY,
                stopbits=STOPBITS,
                timeout=TIMEOUT
            )

            print(f"Connected to {PORT} at 115200 baud\n")

            print("=== Querying System Information ===")
            response = send_command(ser, '~00150 1')
            print(f"Response: {response}")

            ser.close()
            print("\nConnection closed.")

        except Exception as e2:
            print(f"Error with 115200 baud: {e2}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_projector_status()
