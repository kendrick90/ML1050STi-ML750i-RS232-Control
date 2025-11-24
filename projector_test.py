#!/usr/bin/env python3
"""
Interactive Projector RS232 Test Tool
"""

import serial
import time
import sys

PORT = 'COM10'
BAUDRATE = 9600

def test_connection():
    """Test connection with various commands"""
    try:
        print(f"Opening {PORT} at {BAUDRATE} baud...")
        ser = serial.Serial(
            port=PORT,
            baudrate=BAUDRATE,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=2,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False
        )

        ser.setRTS(True)
        ser.setDTR(True)
        time.sleep(0.2)

        print(f"Connected! RTS: {ser.rts}, DTR: {ser.dtr}")
        print(f"CTS: {ser.cts}, DSR: {ser.dsr}\n")

        # Test commands
        test_commands = [
            ('Power State', '~00124 1'),
            ('System Info', '~00150 1'),
            ('Software Version', '~00122 1'),
            ('Power On', '~00 1'),  # Simple power on command
        ]

        for name, cmd in test_commands:
            print(f"\n=== Testing: {name} ===")
            ser.reset_input_buffer()
            ser.reset_output_buffer()

            # Send command
            cmd_full = cmd + '\r'
            cmd_bytes = cmd_full.encode('ascii')
            print(f"TX: {repr(cmd_full)}")
            print(f"HEX: {' '.join(f'{b:02x}' for b in cmd_bytes)}")

            ser.write(cmd_bytes)
            ser.flush()

            # Wait and read
            time.sleep(1)
            response = b''
            for _ in range(20):
                if ser.in_waiting > 0:
                    chunk = ser.read(ser.in_waiting)
                    response += chunk
                    print(f"RX: {repr(chunk)} | HEX: {' '.join(f'{b:02x}' for b in chunk)}")
                time.sleep(0.1)

            if not response:
                print("No response")
            else:
                print(f"Total: {repr(response)}")
                print(f"Decoded: {response.decode('ascii', errors='ignore')}")

        print("\n=== Listening for any data (5 seconds) ===")
        start_time = time.time()
        while time.time() - start_time < 5:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                print(f"Received: {repr(data)} | {data.hex(' ')}")
            time.sleep(0.1)

        ser.close()
        print("\nConnection closed.")

    except serial.SerialException as e:
        print(f"Serial error: {e}")
        print("\nPossible issues:")
        print("1. Projector is off or in standby")
        print("2. Wrong COM port")
        print("3. Cable not properly connected")
        print("4. TX/RX wires swapped")
        print("5. Another application is using the port")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 60)
    print("Projector RS232 Connection Test")
    print("=" * 60)
    test_connection()
