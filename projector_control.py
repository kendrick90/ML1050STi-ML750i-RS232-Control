#!/usr/bin/env python3
"""
Comprehensive Projector Control Interface
Based on ML1050STi / ML750i RS232 Protocol
"""

import serial
import time
from typing import Optional, Dict, Any


class ProjectorController:
    """Complete control interface for DDP projector via RS232"""

    def __init__(self, port='COM10', baudrate=9600, device_id='00'):
        """
        Initialize projector controller

        Args:
            port: Serial port name (e.g., 'COM10')
            baudrate: Baud rate (default 9600)
            device_id: Projector device ID (00-99, default '00' for broadcast)
        """
        self.port = port
        self.baudrate = baudrate
        self.device_id = device_id
        self.ser = None

    def connect(self):
        """Open serial connection to projector"""
        if self.ser and self.ser.is_open:
            return True

        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=2,
                xonxoff=False,
                rtscts=False,
                dsrdtr=False
            )

            self.ser.setRTS(True)
            self.ser.setDTR(True)
            time.sleep(0.2)
            return True

        except serial.SerialException as e:
            print(f"Connection error: {e}")
            return False

    def disconnect(self):
        """Close serial connection"""
        if self.ser and self.ser.is_open:
            self.ser.close()

    def _send_command(self, command: str) -> str:
        """
        Send command to projector and return response

        Args:
            command: Command string without CR terminator

        Returns:
            Response string from projector
        """
        if not self.ser or not self.ser.is_open:
            if not self.connect():
                return ""

        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        # Add CR terminator
        cmd_full = f"~{self.device_id}{command}\r"
        self.ser.write(cmd_full.encode('ascii'))
        self.ser.flush()

        # Read response
        response = b''
        for _ in range(10):
            time.sleep(0.1)
            if self.ser.in_waiting > 0:
                response += self.ser.read(self.ser.in_waiting)
                if b'Ok' in response or b'P' in response or b'F' in response:
                    break

        return response.decode('ascii', errors='ignore').strip()

    def _check_success(self, response: str) -> bool:
        """Check if command was successful"""
        return response == 'P' or response.startswith('Ok')

    # ========== POWER CONTROL ==========

    def power_on(self) -> bool:
        """Turn projector on"""
        response = self._send_command('00 1')
        return self._check_success(response)

    def power_off(self) -> bool:
        """Turn projector off"""
        response = self._send_command('00 0')
        return self._check_success(response)

    def get_power_state(self) -> Optional[bool]:
        """Get power state. Returns True if on, False if off"""
        response = self._send_command('124 1')
        if response == 'Ok0':
            return False
        elif response == 'Ok1':
            return True
        return None

    # ========== MUTE CONTROL ==========

    def av_mute_on(self) -> bool:
        """Turn on AV mute (video and audio)"""
        response = self._send_command('02 1')
        return self._check_success(response)

    def av_mute_off(self) -> bool:
        """Turn off AV mute"""
        response = self._send_command('02 0')
        return self._check_success(response)

    def get_av_mute_state(self) -> Optional[bool]:
        """Get AV mute state"""
        response = self._send_command('355 1')
        if response == 'Ok0':
            return False
        elif response == 'Ok1':
            return True
        return None

    def audio_mute_on(self) -> bool:
        """Turn on audio mute"""
        response = self._send_command('03 1')
        return self._check_success(response)

    def audio_mute_off(self) -> bool:
        """Turn off audio mute"""
        response = self._send_command('03 0')
        return self._check_success(response)

    def get_audio_mute_state(self) -> Optional[bool]:
        """Get audio mute state"""
        response = self._send_command('356 1')
        if response == 'Ok0':
            return False
        elif response == 'Ok1':
            return True
        return None

    # ========== FREEZE CONTROL ==========

    def freeze_on(self) -> bool:
        """Freeze the image"""
        response = self._send_command('04 1')
        return self._check_success(response)

    def freeze_off(self) -> bool:
        """Unfreeze the image"""
        response = self._send_command('04 0')
        return self._check_success(response)

    # ========== SOURCE CONTROL ==========

    def set_source_hdmi(self) -> bool:
        """Switch to HDMI input"""
        response = self._send_command('12 1')
        return self._check_success(response)

    def set_source_usb(self) -> bool:
        """Switch to USB-A (Flash Drive)"""
        response = self._send_command('12 17')
        return self._check_success(response)

    def set_source_sd_card(self) -> bool:
        """Switch to SD Card"""
        response = self._send_command('12 31')
        return self._check_success(response)

    def set_source_android_home(self) -> bool:
        """Switch to Android Home page (Smart TV)"""
        response = self._send_command('12 24')
        return self._check_success(response)

    def get_input_source(self) -> Optional[str]:
        """Get current input source"""
        response = self._send_command('121 1')
        if response.startswith('Ok'):
            code = response[2:]
            source_map = {
                '7': 'HDMI 1',
                '20': 'Android Home (USB-A/SD Card)'
            }
            return source_map.get(code, f"Unknown ({code})")
        return None

    # ========== PROJECTION MODE ==========

    def set_projection_front_desktop(self) -> bool:
        """Set projection mode: Front-Desktop"""
        response = self._send_command('71 1')
        return self._check_success(response)

    def set_projection_rear_desktop(self) -> bool:
        """Set projection mode: Rear-Desktop"""
        response = self._send_command('71 2')
        return self._check_success(response)

    def set_projection_front_ceiling(self) -> bool:
        """Set projection mode: Front-Ceiling"""
        response = self._send_command('71 3')
        return self._check_success(response)

    def set_projection_rear_ceiling(self) -> bool:
        """Set projection mode: Rear-Ceiling"""
        response = self._send_command('71 4')
        return self._check_success(response)

    def get_projection_mode(self) -> Optional[str]:
        """Get projection mode"""
        response = self._send_command('129 1')
        if response.startswith('Ok'):
            mode_map = {
                '0': 'Front-Desktop',
                '1': 'Rear-Desktop',
                '2': 'Front-Ceiling',
                '3': 'Rear-Ceiling'
            }
            return mode_map.get(response[2], 'Unknown')
        return None

    # ========== DISPLAY MODE (PICTURE MODE) ==========

    def set_display_mode_presentation(self) -> bool:
        """Set display mode: Presentation (PC)"""
        response = self._send_command('20 1')
        return self._check_success(response)

    def set_display_mode_bright(self) -> bool:
        """Set display mode: Bright"""
        response = self._send_command('20 2')
        return self._check_success(response)

    def set_display_mode_cinema(self) -> bool:
        """Set display mode: Cinema"""
        response = self._send_command('20 3')
        return self._check_success(response)

    def set_display_mode_srgb(self) -> bool:
        """Set display mode: sRGB"""
        response = self._send_command('20 4')
        return self._check_success(response)

    def set_display_mode_photo(self) -> bool:
        """Set display mode: Photo (Vivid)"""
        response = self._send_command('20 16')
        return self._check_success(response)

    def set_display_mode_eco(self) -> bool:
        """Set display mode: Eco"""
        response = self._send_command('20 44')
        return self._check_success(response)

    def set_display_mode_3d(self) -> bool:
        """Set display mode: 3D"""
        response = self._send_command('20 9')
        return self._check_success(response)

    def set_display_mode_game(self) -> bool:
        """Set display mode: Game"""
        response = self._send_command('20 12')
        return self._check_success(response)

    def set_display_mode_hdr(self) -> bool:
        """Set display mode: HDR"""
        response = self._send_command('20 21')
        return self._check_success(response)

    def set_display_mode_hlg(self) -> bool:
        """Set display mode: HLG"""
        response = self._send_command('20 25')
        return self._check_success(response)

    def set_display_mode_ai_pq(self) -> bool:
        """Set display mode: AI-PQ"""
        response = self._send_command('20 41')
        return self._check_success(response)

    def set_display_mode_wcg(self) -> bool:
        """Set display mode: WCG (Wide Color Gamut)"""
        response = self._send_command('20 42')
        return self._check_success(response)

    def get_display_mode(self) -> Optional[str]:
        """Get current display mode"""
        response = self._send_command('123 1')
        if response.startswith('Ok'):
            mode_map = {
                '1': 'Presentation (PC)',
                '2': 'Bright',
                '3': 'Cinema',
                '4': 'sRGB',
                '9': '3D',
                '12': 'Game',
                '14': 'Photo (Vivid)',
                '21': 'HDR',
                '25': 'HLG',
                '41': 'AI-PQ',
                '42': 'WCG',
                '43': 'Eco'
            }
            code = response[2:]
            return mode_map.get(code, f"Unknown ({code})")
        return None

    # ========== IMAGE SETTINGS ==========

    def set_brightness(self, value: int) -> bool:
        """Set brightness (0-10)"""
        if not 0 <= value <= 10:
            return False
        response = self._send_command(f'21 {value}')
        return self._check_success(response)

    def get_brightness(self) -> Optional[int]:
        """Get brightness value (0-10)"""
        response = self._send_command('125 1')
        if response.startswith('Ok'):
            try:
                return int(response[2:])
            except:
                pass
        return None

    def set_contrast(self, value: int) -> bool:
        """Set contrast (0-10)"""
        if not 0 <= value <= 10:
            return False
        response = self._send_command(f'22 {value}')
        return self._check_success(response)

    def get_contrast(self) -> Optional[int]:
        """Get contrast value (0-10)"""
        response = self._send_command('126 1')
        if response.startswith('Ok'):
            try:
                return int(response[2:])
            except:
                pass
        return None

    # ========== COLOR TEMPERATURE ==========

    def set_color_temp_standard(self) -> bool:
        """Set color temperature: Standard (D75)"""
        response = self._send_command('36 1')
        return self._check_success(response)

    def set_color_temp_cold(self) -> bool:
        """Set color temperature: Cold (D83)"""
        response = self._send_command('36 3')
        return self._check_success(response)

    def set_color_temp_warm(self) -> bool:
        """Set color temperature: Warm (D65)"""
        response = self._send_command('36 4')
        return self._check_success(response)

    def get_color_temperature(self) -> Optional[str]:
        """Get color temperature setting"""
        response = self._send_command('128 1')
        if response.startswith('Ok'):
            temp_map = {
                '2': 'Standard (D75)',
                '3': 'Warm (D65)',
                '5': 'Cold (D83)'
            }
            return temp_map.get(response[2], 'Unknown')
        return None

    # ========== ASPECT RATIO ==========

    def set_aspect_4_3(self) -> bool:
        """Set aspect ratio: 4:3"""
        response = self._send_command('60 1')
        return self._check_success(response)

    def set_aspect_16_9(self) -> bool:
        """Set aspect ratio: 16:9"""
        response = self._send_command('60 2')
        return self._check_success(response)

    def set_aspect_16_10(self) -> bool:
        """Set aspect ratio: 16:10"""
        response = self._send_command('60 3')
        return self._check_success(response)

    def set_aspect_auto(self) -> bool:
        """Set aspect ratio: Auto"""
        response = self._send_command('60 7')
        return self._check_success(response)

    def get_aspect_ratio(self) -> Optional[str]:
        """Get aspect ratio setting"""
        response = self._send_command('127 1')
        if response.startswith('Ok'):
            ratio_map = {
                '1': '4:3',
                '2': '16:9',
                '3': '16:10',
                '7': 'Auto'
            }
            return ratio_map.get(response[2:], 'Unknown')
        return None

    # ========== KEYSTONE ==========

    def set_auto_keystone_on(self) -> bool:
        """Enable auto keystone"""
        response = self._send_command('69 1')
        return self._check_success(response)

    def set_auto_keystone_off(self) -> bool:
        """Disable auto keystone"""
        response = self._send_command('69 0')
        return self._check_success(response)

    def get_v_keystone(self) -> Optional[int]:
        """Get vertical keystone value (-40 to +40)"""
        response = self._send_command('543 3')
        if response.startswith('Ok'):
            try:
                return int(response[2:])
            except:
                pass
        return None

    # ========== DIGITAL ZOOM ==========

    def set_digital_zoom(self, level: int) -> bool:
        """
        Set digital zoom level (0-6)
        0=50%, 1=75%, 2=100%, 3=125%, 4=150%, 5=175%, 6=200%
        """
        if not 0 <= level <= 6:
            return False
        response = self._send_command(f'62 {level}')
        return self._check_success(response)

    def set_digital_zoom_50(self) -> bool:
        """Set digital zoom to 50%"""
        return self.set_digital_zoom(0)

    def set_digital_zoom_75(self) -> bool:
        """Set digital zoom to 75%"""
        return self.set_digital_zoom(1)

    def set_digital_zoom_100(self) -> bool:
        """Set digital zoom to 100% (normal)"""
        return self.set_digital_zoom(2)

    def set_digital_zoom_125(self) -> bool:
        """Set digital zoom to 125%"""
        return self.set_digital_zoom(3)

    def set_digital_zoom_150(self) -> bool:
        """Set digital zoom to 150%"""
        return self.set_digital_zoom(4)

    def set_digital_zoom_175(self) -> bool:
        """Set digital zoom to 175%"""
        return self.set_digital_zoom(5)

    def set_digital_zoom_200(self) -> bool:
        """Set digital zoom to 200%"""
        return self.set_digital_zoom(6)

    def get_digital_zoom(self) -> Optional[str]:
        """Get digital zoom level"""
        response = self._send_command('543 9')
        if response.startswith('Ok'):
            zoom_map = {
                '0': '50%',
                '1': '75%',
                '2': '100%',
                '3': '125%',
                '4': '150%',
                '5': '175%',
                '6': '200%'
            }
            return zoom_map.get(response[2], 'Unknown')
        return None

    # ========== VOLUME ==========

    def volume_up(self) -> bool:
        """Increase volume"""
        response = self._send_command('140 18')
        return self._check_success(response)

    def volume_down(self) -> bool:
        """Decrease volume"""
        response = self._send_command('140 17')
        return self._check_success(response)

    def get_volume(self) -> Optional[int]:
        """Get volume level (0-10)"""
        response = self._send_command('120 1')
        if response.startswith('Ok'):
            try:
                return int(response[2:])
            except:
                pass
        return None

    # ========== LANGUAGE ==========

    def set_language(self, lang_code: int) -> bool:
        """
        Set OSD language
        1=English, 2=German, 3=French, 4=Italian, 5=Spanish, 6=Portuguese,
        7=Polish, 8=Dutch, 9=Swedish, 17=Russian, 20=Arabic, 22=Turkish
        """
        response = self._send_command(f'70 {lang_code}')
        return self._check_success(response)

    # ========== REMOTE CONTROL FUNCTIONS ==========

    def remote_menu(self) -> bool:
        """Display OSD main menu"""
        response = self._send_command('140 20')
        return self._check_success(response)

    def remote_up(self) -> bool:
        """OSD menu - Up"""
        response = self._send_command('140 10')
        return self._check_success(response)

    def remote_down(self) -> bool:
        """OSD menu - Down"""
        response = self._send_command('140 14')
        return self._check_success(response)

    def remote_left(self) -> bool:
        """OSD menu - Left"""
        response = self._send_command('140 11')
        return self._check_success(response)

    def remote_right(self) -> bool:
        """OSD menu - Right"""
        response = self._send_command('140 13')
        return self._check_success(response)

    def remote_enter(self) -> bool:
        """OSD menu - Enter"""
        response = self._send_command('140 12')
        return self._check_success(response)

    # ========== SYSTEM INFORMATION ==========

    def get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information"""
        response = self._send_command('150 1')

        info = {}
        if response.startswith('Ok') and len(response) >= 15:
            data = response[2:]

            # Parse: Okabbbbbccddddee
            info['power'] = 'On' if data[0] == '1' else 'Off'
            info['lamp_hours'] = int(data[1:6])

            source_code = data[6:8]
            source_map = {
                '07': 'HDMI 1',
                '20': 'Android Home (USB-A/SD Card)'
            }
            info['input_source'] = source_map.get(source_code, f"Unknown ({source_code})")

            info['firmware'] = data[8:12]

            if len(data) >= 14:
                mode_code = data[12:14]
                mode_map = {
                    '01': 'Presentation (PC)',
                    '02': 'Bright',
                    '03': 'Cinema',
                    '04': 'sRGB',
                    '14': 'Photo (Vivid)',
                    '28': 'Eco'
                }
                info['picture_mode'] = mode_map.get(mode_code, f"Unknown ({mode_code})")

        return info

    def get_software_version(self) -> Dict[str, str]:
        """Get detailed software version information (all versions)"""
        response = self._send_command('122 1')

        versions = {}
        if response.startswith('Ok'):
            # Parse: OkAaaMbbLccHddSeeXff or OkCaaMbbRcc format
            data = response[2:]

            # Try to parse the format
            if 'C' in data and 'M' in data:
                parts = data.replace('R', 'R ').replace('M', ' M').replace('L', ' L').replace('H', ' H').replace('S', ' S').replace('X', ' X').split()
                for part in parts:
                    if part.startswith('C'):
                        versions['DDP'] = part[1:]
                    elif part.startswith('M'):
                        versions['MCU'] = part[1:]
                    elif part.startswith('R'):
                        versions['Android'] = part[1:]
                    elif part.startswith('L'):
                        versions['LAN'] = part[1:]
                    elif part.startswith('H'):
                        versions['HDBaseT'] = part[1:]
                    elif part.startswith('S'):
                        versions['System'] = part[1:]

        return versions

    def get_ddp_software_version(self) -> Optional[str]:
        """Get DDP software version only"""
        response = self._send_command('357 3')
        if response.startswith('Ok'):
            return response[2:]
        return None

    def get_android_software_version(self) -> Optional[str]:
        """Get Android software version only"""
        response = self._send_command('357 4')
        if response.startswith('Ok'):
            return response[2:]
        return None

    def get_lamp_hours(self) -> Optional[int]:
        """Get light source hours of usage"""
        response = self._send_command('108 1')
        if response.startswith('Ok'):
            try:
                return int(response[2:])
            except:
                pass
        return None

    def get_system_hours(self) -> Optional[int]:
        """Get total system hours of usage"""
        response = self._send_command('150 21')
        if response.startswith('Ok'):
            try:
                return int(response[2:])
            except:
                pass
        return None

    def get_temperature(self) -> Optional[int]:
        """Get system temperature"""
        response = self._send_command('352 1')
        if response.startswith('Ok'):
            try:
                return int(response[2:])
            except:
                pass
        return None

    def get_fan_speeds(self) -> Dict[str, Optional[int]]:
        """Get all fan speeds in RPM"""
        fans = {}

        for fan_num, fan_name in [(0, 'System Fan 1'), (1, 'System Fan 2'), (2, 'Optical Fan')]:
            response = self._send_command(f'351 {fan_num}')
            if response.startswith('Ok'):
                try:
                    fans[fan_name] = int(response[2:])
                except:
                    fans[fan_name] = None
            else:
                fans[fan_name] = None

        return fans

    def get_mac_address(self) -> Optional[str]:
        """Get network MAC address"""
        response = self._send_command('555 2')
        if response.startswith('Ok'):
            return response[2:]
        return None

    def get_device_id(self) -> Optional[str]:
        """Get projector device ID (00-99)"""
        response = self._send_command('558 1')
        if response.startswith('Ok'):
            return response[2:]
        return None

    def get_network_status(self) -> Optional[bool]:
        """Get WiFi connection status. Returns True if connected"""
        response = self._send_command('451 1')
        if response == 'Ok0':
            return False
        elif response == 'Ok1':
            return True
        return None

    def get_signal_status(self) -> Optional[bool]:
        """Get signal status of current input. Returns True if signal active"""
        response = self._send_command('150 23')
        if response == 'Ok0':
            return False
        elif response == 'Ok1':
            return True
        return None

    def get_resolution(self) -> Optional[str]:
        """Get source resolution"""
        response = self._send_command('150 4')
        if response.startswith('Ok'):
            return response[2:]
        return None

    def get_refresh_rate(self) -> Optional[str]:
        """Get refresh rate"""
        response = self._send_command('150 19')
        if response.startswith('Ok'):
            return response[2:]
        return None

    # ========== DIGITAL SIGNAGE ==========

    def set_digital_signage_on(self) -> bool:
        """Enable digital signage mode"""
        response = self._send_command('569 2')
        return self._check_success(response)

    def set_digital_signage_off(self) -> bool:
        """Disable digital signage mode"""
        response = self._send_command('569 1')
        return self._check_success(response)

    def get_digital_signage_status(self) -> Optional[bool]:
        """Get digital signage status"""
        response = self._send_command('568 1')
        if response == 'Ok0':
            return False
        elif response == 'Ok1':
            return True
        return None

    # ========== RESET FUNCTIONS ==========

    def factory_reset(self) -> bool:
        """Perform factory reset (WARNING: Resets all settings)"""
        response = self._send_command('112 1')
        return self._check_success(response)

    def reset_osd_settings(self) -> bool:
        """Reset OSD settings to default"""
        response = self._send_command('546 1')
        return self._check_success(response)

    # ========== CONTEXT MANAGER SUPPORT ==========

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()


if __name__ == "__main__":
    # Example usage
    with ProjectorController(port='COM10') as proj:
        print("=== Projector Control Test ===\n")

        # Get system info
        info = proj.get_system_info()
        print("System Information:")
        for key, value in info.items():
            print(f"  {key}: {value}")

        print(f"\nPower State: {proj.get_power_state()}")
        print(f"Input Source: {proj.get_input_source()}")
        print(f"Display Mode: {proj.get_display_mode()}")
        print(f"Volume: {proj.get_volume()}")
        print(f"Temperature: {proj.get_temperature()}°C")
