#!/usr/bin/env python3
"""
Interactive CLI Interface for Projector Control
"""

import sys
from pathlib import Path
from projector_control import ProjectorController
from projector_config import ProjectorConfig


class ProjectorCLI:
    """Interactive command-line interface for projector control"""

    def __init__(self, port='COM10'):
        self.proj = ProjectorController(port=port)
        self.running = False

    def print_header(self):
        """Print CLI header"""
        print("\n" + "=" * 70)
        print("  PROJECTOR CONTROL INTERFACE")
        print("=" * 70)

    def print_menu(self):
        """Print main menu"""
        print("\n" + "-" * 70)
        print("MAIN MENU")
        print("-" * 70)
        print("  [1] Power Control          [2] Source Control")
        print("  [3] Display Settings       [4] Image Settings")
        print("  [5] Audio Control          [6] Remote Functions")
        print("  [7] System Information     [8] Advanced Settings")
        print("  [9] Quick Status           [C] Config Save/Load")
        print("  [0] Exit")
        print("-" * 70)

    def power_menu(self):
        """Power control submenu"""
        while True:
            print("\n--- POWER CONTROL ---")
            print("  [1] Power On")
            print("  [2] Power Off")
            print("  [3] Check Power State")
            print("  [0] Back")

            choice = input("\nChoice: ").strip()

            if choice == '1':
                print("Turning projector ON...")
                if self.proj.power_on():
                    print("✓ Projector is turning on")
                else:
                    print("✗ Failed to send power on command")

            elif choice == '2':
                confirm = input("Really power off? (yes/no): ").strip().lower()
                if confirm in ['yes', 'y']:
                    print("Turning projector OFF...")
                    if self.proj.power_off():
                        print("✓ Projector is turning off")
                    else:
                        print("✗ Failed to send power off command")

            elif choice == '3':
                state = self.proj.get_power_state()
                if state is True:
                    print("Power State: ON")
                elif state is False:
                    print("Power State: OFF")
                else:
                    print("✗ Could not read power state")

            elif choice == '0':
                break

    def source_menu(self):
        """Source control submenu"""
        while True:
            print("\n--- SOURCE CONTROL ---")
            current = self.proj.get_input_source()
            print(f"  Current Source: {current if current else 'Unknown'}")
            print()
            print("  [1] HDMI 1")
            print("  [2] USB-A (Flash Drive)")
            print("  [3] SD Card")
            print("  [4] Android Home")
            print("  [0] Back")

            choice = input("\nChoice: ").strip()

            if choice == '1':
                print("Switching to HDMI 1...")
                if self.proj.set_source_hdmi():
                    print("✓ Switched to HDMI 1")
                else:
                    print("✗ Failed")

            elif choice == '2':
                print("Switching to USB-A...")
                if self.proj.set_source_usb():
                    print("✓ Switched to USB-A")
                else:
                    print("✗ Failed")

            elif choice == '3':
                print("Switching to SD Card...")
                if self.proj.set_source_sd_card():
                    print("✓ Switched to SD Card")
                else:
                    print("✗ Failed")

            elif choice == '4':
                print("Switching to Android Home...")
                if self.proj.set_source_android_home():
                    print("✓ Switched to Android Home")
                else:
                    print("✗ Failed")

            elif choice == '0':
                break

    def display_menu(self):
        """Display settings submenu"""
        while True:
            print("\n--- DISPLAY SETTINGS ---")
            current = self.proj.get_display_mode()
            zoom = self.proj.get_digital_zoom()
            print(f"  Current Mode: {current if current else 'Unknown'}")
            print(f"  Digital Zoom: {zoom if zoom else 'Unknown'}")
            print()
            print("  [1] Presentation (PC)      [2] Bright         [3] Cinema")
            print("  [4] sRGB                   [5] Photo (Vivid)  [6] Eco")
            print("  [7] 3D                     [8] Game           [9] HDR")
            print("  [A] HLG                    [B] AI-PQ          [C] WCG")
            print("  [D] Projection Mode        [E] Aspect Ratio   [F] Digital Zoom")
            print("  [0] Back")

            choice = input("\nChoice: ").strip()

            if choice == '1':
                if self.proj.set_display_mode_presentation():
                    print("✓ Set to Presentation mode")
                else:
                    print("✗ Failed")

            elif choice == '2':
                if self.proj.set_display_mode_bright():
                    print("✓ Set to Bright mode")
                else:
                    print("✗ Failed")

            elif choice == '3':
                if self.proj.set_display_mode_cinema():
                    print("✓ Set to Cinema mode")
                else:
                    print("✗ Failed")

            elif choice == '4':
                if self.proj.set_display_mode_srgb():
                    print("✓ Set to sRGB mode")
                else:
                    print("✗ Failed")

            elif choice == '5':
                if self.proj.set_display_mode_photo():
                    print("✓ Set to Photo mode")
                else:
                    print("✗ Failed")

            elif choice == '6':
                if self.proj.set_display_mode_eco():
                    print("✓ Set to Eco mode")
                else:
                    print("✗ Failed")

            elif choice == '7':
                if self.proj.set_display_mode_3d():
                    print("✓ Set to 3D mode")
                else:
                    print("✗ Failed")

            elif choice == '8':
                if self.proj.set_display_mode_game():
                    print("✓ Set to Game mode")
                else:
                    print("✗ Failed")

            elif choice == '9':
                if self.proj.set_display_mode_hdr():
                    print("✓ Set to HDR mode")
                else:
                    print("✗ Failed")

            elif choice.upper() == 'A':
                if self.proj.set_display_mode_hlg():
                    print("✓ Set to HLG mode")
                else:
                    print("✗ Failed")

            elif choice.upper() == 'B':
                if self.proj.set_display_mode_ai_pq():
                    print("✓ Set to AI-PQ mode")
                else:
                    print("✗ Failed")

            elif choice.upper() == 'C':
                if self.proj.set_display_mode_wcg():
                    print("✓ Set to WCG mode")
                else:
                    print("✗ Failed")

            elif choice.upper() == 'D':
                self.projection_mode_submenu()

            elif choice.upper() == 'E':
                self.aspect_ratio_submenu()

            elif choice.upper() == 'F':
                self.digital_zoom_submenu()

            elif choice == '0':
                break

    def projection_mode_submenu(self):
        """Projection mode submenu"""
        print("\n--- PROJECTION MODE ---")
        current = self.proj.get_projection_mode()
        print(f"  Current: {current if current else 'Unknown'}")
        print()
        print("  [1] Front-Desktop")
        print("  [2] Rear-Desktop")
        print("  [3] Front-Ceiling")
        print("  [4] Rear-Ceiling")

        choice = input("\nChoice: ").strip()

        if choice == '1':
            if self.proj.set_projection_front_desktop():
                print("✓ Set to Front-Desktop")
        elif choice == '2':
            if self.proj.set_projection_rear_desktop():
                print("✓ Set to Rear-Desktop")
        elif choice == '3':
            if self.proj.set_projection_front_ceiling():
                print("✓ Set to Front-Ceiling")
        elif choice == '4':
            if self.proj.set_projection_rear_ceiling():
                print("✓ Set to Rear-Ceiling")

    def aspect_ratio_submenu(self):
        """Aspect ratio submenu"""
        print("\n--- ASPECT RATIO ---")
        current = self.proj.get_aspect_ratio()
        print(f"  Current: {current if current else 'Unknown'}")
        print()
        print("  [1] 4:3")
        print("  [2] 16:9")
        print("  [3] 16:10")
        print("  [4] Auto")

        choice = input("\nChoice: ").strip()

        if choice == '1':
            if self.proj.set_aspect_4_3():
                print("✓ Set to 4:3")
        elif choice == '2':
            if self.proj.set_aspect_16_9():
                print("✓ Set to 16:9")
        elif choice == '3':
            if self.proj.set_aspect_16_10():
                print("✓ Set to 16:10")
        elif choice == '4':
            if self.proj.set_aspect_auto():
                print("✓ Set to Auto")

    def image_menu(self):
        """Image settings submenu"""
        while True:
            print("\n--- IMAGE SETTINGS ---")
            brightness = self.proj.get_brightness()
            contrast = self.proj.get_contrast()
            color_temp = self.proj.get_color_temperature()

            print(f"  Brightness: {brightness if brightness is not None else 'Unknown'}")
            print(f"  Contrast: {contrast if contrast is not None else 'Unknown'}")
            print(f"  Color Temp: {color_temp if color_temp else 'Unknown'}")
            print()
            print("  [1] Set Brightness         [2] Set Contrast")
            print("  [3] Color Temperature      [4] Freeze On/Off")
            print("  [5] Auto Keystone          [0] Back")

            choice = input("\nChoice: ").strip()

            if choice == '1':
                try:
                    val = int(input("Enter brightness (0-10): "))
                    if self.proj.set_brightness(val):
                        print(f"✓ Brightness set to {val}")
                    else:
                        print("✗ Failed (must be 0-10)")
                except ValueError:
                    print("✗ Invalid input")

            elif choice == '2':
                try:
                    val = int(input("Enter contrast (0-10): "))
                    if self.proj.set_contrast(val):
                        print(f"✓ Contrast set to {val}")
                    else:
                        print("✗ Failed (must be 0-10)")
                except ValueError:
                    print("✗ Invalid input")

            elif choice == '3':
                print("\n  [1] Standard  [2] Cold  [3] Warm")
                temp_choice = input("Choice: ").strip()
                if temp_choice == '1':
                    if self.proj.set_color_temp_standard():
                        print("✓ Set to Standard")
                elif temp_choice == '2':
                    if self.proj.set_color_temp_cold():
                        print("✓ Set to Cold")
                elif temp_choice == '3':
                    if self.proj.set_color_temp_warm():
                        print("✓ Set to Warm")

            elif choice == '4':
                print("\n  [1] Freeze On  [2] Freeze Off")
                freeze_choice = input("Choice: ").strip()
                if freeze_choice == '1':
                    if self.proj.freeze_on():
                        print("✓ Freeze enabled")
                elif freeze_choice == '2':
                    if self.proj.freeze_off():
                        print("✓ Freeze disabled")

            elif choice == '5':
                print("\n  [1] Auto Keystone On  [2] Auto Keystone Off")
                ks_choice = input("Choice: ").strip()
                if ks_choice == '1':
                    if self.proj.set_auto_keystone_on():
                        print("✓ Auto keystone enabled")
                elif ks_choice == '2':
                    if self.proj.set_auto_keystone_off():
                        print("✓ Auto keystone disabled")

            elif choice == '0':
                break

    def audio_menu(self):
        """Audio control submenu"""
        while True:
            print("\n--- AUDIO CONTROL ---")
            volume = self.proj.get_volume()
            audio_mute = self.proj.get_audio_mute_state()
            av_mute = self.proj.get_av_mute_state()

            print(f"  Volume: {volume if volume is not None else 'Unknown'}")
            print(f"  Audio Mute: {'ON' if audio_mute else 'OFF' if audio_mute is False else 'Unknown'}")
            print(f"  AV Mute: {'ON' if av_mute else 'OFF' if av_mute is False else 'Unknown'}")
            print()
            print("  [1] Volume Up              [2] Volume Down")
            print("  [3] Audio Mute On          [4] Audio Mute Off")
            print("  [5] AV Mute On             [6] AV Mute Off")
            print("  [0] Back")

            choice = input("\nChoice: ").strip()

            if choice == '1':
                if self.proj.volume_up():
                    print("✓ Volume increased")
            elif choice == '2':
                if self.proj.volume_down():
                    print("✓ Volume decreased")
            elif choice == '3':
                if self.proj.audio_mute_on():
                    print("✓ Audio mute ON")
            elif choice == '4':
                if self.proj.audio_mute_off():
                    print("✓ Audio mute OFF")
            elif choice == '5':
                if self.proj.av_mute_on():
                    print("✓ AV mute ON")
            elif choice == '6':
                if self.proj.av_mute_off():
                    print("✓ AV mute OFF")
            elif choice == '0':
                break

    def remote_menu(self):
        """Remote control functions submenu"""
        while True:
            print("\n--- REMOTE FUNCTIONS ---")
            print("  [1] Menu")
            print("  [2] Up        [3] Down")
            print("  [4] Left      [5] Right")
            print("  [6] Enter")
            print("  [0] Back")

            choice = input("\nChoice: ").strip()

            if choice == '1':
                self.proj.remote_menu()
                print("✓ Menu button pressed")
            elif choice == '2':
                self.proj.remote_up()
                print("✓ Up")
            elif choice == '3':
                self.proj.remote_down()
                print("✓ Down")
            elif choice == '4':
                self.proj.remote_left()
                print("✓ Left")
            elif choice == '5':
                self.proj.remote_right()
                print("✓ Right")
            elif choice == '6':
                self.proj.remote_enter()
                print("✓ Enter")
            elif choice == '0':
                break

    def system_info_menu(self):
        """System information submenu"""
        print("\n" + "=" * 70)
        print("SYSTEM INFORMATION")
        print("=" * 70)

        # Get comprehensive info
        info = self.proj.get_system_info()
        versions = self.proj.get_software_version()
        mac = self.proj.get_mac_address()
        device_id = self.proj.get_device_id()
        temp = self.proj.get_temperature()
        fans = self.proj.get_fan_speeds()
        network = self.proj.get_network_status()
        signal = self.proj.get_signal_status()
        resolution = self.proj.get_resolution()
        refresh = self.proj.get_refresh_rate()
        system_hours = self.proj.get_system_hours()

        print("\nGeneral:")
        print(f"  Power: {info.get('power', 'Unknown')}")
        print(f"  Input Source: {info.get('input_source', 'Unknown')}")
        print(f"  Picture Mode: {info.get('picture_mode', 'Unknown')}")
        print(f"  Lamp Hours: {info.get('lamp_hours', 'Unknown')}")
        print(f"  System Hours: {system_hours if system_hours else 'Unknown'}")

        print("\nSoftware:")
        for key, val in versions.items():
            print(f"  {key}: {val}")

        print("\nNetwork:")
        print(f"  MAC Address: {mac if mac else 'Unknown'}")
        print(f"  WiFi Status: {'Connected' if network else 'Disconnected' if network is False else 'Unknown'}")
        print(f"  Device ID: {device_id if device_id else 'Unknown'}")

        print("\nSignal:")
        print(f"  Signal Active: {'Yes' if signal else 'No' if signal is False else 'Unknown'}")
        print(f"  Resolution: {resolution if resolution else 'Unknown'}")
        print(f"  Refresh Rate: {refresh if refresh else 'Unknown'}")

        print("\nSystem Status:")
        print(f"  Temperature: {temp}°C" if temp else "  Temperature: Unknown")
        print("\n  Fan Speeds:")
        for fan_name, rpm in fans.items():
            print(f"    {fan_name}: {rpm} RPM" if rpm else f"    {fan_name}: Unknown")

        print("\n" + "=" * 70)
        input("\nPress Enter to continue...")

    def advanced_menu(self):
        """Advanced settings submenu"""
        while True:
            print("\n--- ADVANCED SETTINGS ---")
            ds_status = self.proj.get_digital_signage_status()
            print(f"  Digital Signage: {'ON' if ds_status else 'OFF' if ds_status is False else 'Unknown'}")
            print()
            print("  [1] Digital Signage On     [2] Digital Signage Off")
            print("  [3] Set Language           [4] Reset OSD Settings")
            print("  [5] Factory Reset          [0] Back")

            choice = input("\nChoice: ").strip()

            if choice == '1':
                if self.proj.set_digital_signage_on():
                    print("✓ Digital signage enabled")
            elif choice == '2':
                if self.proj.set_digital_signage_off():
                    print("✓ Digital signage disabled")
            elif choice == '3':
                print("\nLanguages: 1=English, 2=German, 3=French, 4=Italian,")
                print("           5=Spanish, 6=Portuguese, 7=Polish, 8=Dutch,")
                print("           9=Swedish, 17=Russian, 20=Arabic, 22=Turkish")
                try:
                    lang = int(input("Enter language code: "))
                    if self.proj.set_language(lang):
                        print("✓ Language changed")
                except ValueError:
                    print("✗ Invalid input")
            elif choice == '4':
                confirm = input("Reset OSD settings? (yes/no): ").strip().lower()
                if confirm in ['yes', 'y']:
                    if self.proj.reset_osd_settings():
                        print("✓ OSD settings reset")
            elif choice == '5':
                confirm = input("FACTORY RESET - Are you SURE? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    if self.proj.factory_reset():
                        print("✓ Factory reset initiated")
            elif choice == '0':
                break

    def digital_zoom_submenu(self):
        """Digital zoom submenu"""
        print("\n--- DIGITAL ZOOM ---")
        current = self.proj.get_digital_zoom()
        print(f"  Current: {current if current else 'Unknown'}")
        print()
        print("  [1] 50%    [2] 75%    [3] 100%")
        print("  [4] 125%   [5] 150%   [6] 175%   [7] 200%")

        choice = input("\nChoice: ").strip()

        zoom_map = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6}
        zoom_labels = {0: '50%', 1: '75%', 2: '100%', 3: '125%', 4: '150%', 5: '175%', 6: '200%'}

        if choice in zoom_map:
            level = zoom_map[choice]
            if self.proj.set_digital_zoom(level):
                print(f"✓ Digital zoom set to {zoom_labels[level]}")
            else:
                print("✗ Failed")

    def config_menu(self):
        """Config save/load submenu"""
        while True:
            print("\n--- CONFIG MANAGEMENT ---")
            print("  [1] Save Config to JSON")
            print("  [2] Save Config to YAML")
            print("  [3] Load Config from File")
            print("  [4] Show Current Config")
            print("  [0] Back")

            choice = input("\nChoice: ").strip()

            if choice == '1':
                filename = input("Enter filename (e.g., my_config.json): ").strip()
                if not filename:
                    print("✗ Filename required")
                    continue

                config_mgr = ProjectorConfig(self.proj)
                if config_mgr.save_to_file(filename, format='json'):
                    print(f"✓ Config saved to {filename}")
                else:
                    print("✗ Failed to save config")

            elif choice == '2':
                filename = input("Enter filename (e.g., my_config.yaml): ").strip()
                if not filename:
                    print("✗ Filename required")
                    continue

                config_mgr = ProjectorConfig(self.proj)
                if config_mgr.save_to_file(filename, format='yaml'):
                    print(f"✓ Config saved to {filename}")
                else:
                    print("✗ Failed to save config")

            elif choice == '3':
                filename = input("Enter filename to load: ").strip()
                if not filename:
                    print("✗ Filename required")
                    continue

                if not Path(filename).exists():
                    print(f"✗ File not found: {filename}")
                    continue

                include_power = input("Include power state? (yes/no): ").strip().lower()
                skip_power = include_power not in ['yes', 'y']

                config_mgr = ProjectorConfig(self.proj)
                results = config_mgr.restore_from_file(filename, skip_power=skip_power)

                print("\n=== Results ===")
                print(f"✓ Success: {len(results['success'])}")
                for item in results['success'][:5]:  # Show first 5
                    print(f"  - {item}")
                if len(results['success']) > 5:
                    print(f"  ... and {len(results['success']) - 5} more")

                if results['failed']:
                    print(f"\n✗ Failed: {len(results['failed'])}")
                    for item in results['failed']:
                        print(f"  - {item}")

                if results['skipped']:
                    print(f"\n⊝ Skipped: {len(results['skipped'])}")

                input("\nPress Enter to continue...")

            elif choice == '4':
                config_mgr = ProjectorConfig(self.proj)
                config = config_mgr.capture_config()

                print("\n" + "=" * 70)
                print("CURRENT CONFIGURATION")
                print("=" * 70)

                for section, settings in config.items():
                    if section != 'metadata':
                        print(f"\n[{section.upper()}]")
                        for key, value in settings.items():
                            print(f"  {key}: {value}")

                print("=" * 70)
                input("\nPress Enter to continue...")

            elif choice == '0':
                break

    def quick_status(self):
        """Display quick status summary"""
        print("\n" + "=" * 70)
        print("QUICK STATUS")
        print("=" * 70)

        info = self.proj.get_system_info()
        volume = self.proj.get_volume()
        temp = self.proj.get_temperature()

        print(f"\n  Power: {info.get('power', 'Unknown')}")
        print(f"  Source: {info.get('input_source', 'Unknown')}")
        print(f"  Picture Mode: {info.get('picture_mode', 'Unknown')}")
        print(f"  Volume: {volume if volume is not None else 'Unknown'}")
        print(f"  Temperature: {temp}°C" if temp else "  Temperature: Unknown")
        print(f"  Runtime: {info.get('lamp_hours', 'Unknown')} hours")

        print("=" * 70)
        input("\nPress Enter to continue...")

    def run(self):
        """Run the interactive CLI"""
        self.print_header()

        # Try to connect
        print("\nConnecting to projector...")
        if not self.proj.connect():
            print("✗ Failed to connect to projector")
            print("  Check that COM10 is correct and projector is connected")
            return

        print("✓ Connected successfully")

        self.running = True

        try:
            while self.running:
                self.print_menu()
                choice = input("\nChoice: ").strip()

                if choice == '1':
                    self.power_menu()
                elif choice == '2':
                    self.source_menu()
                elif choice == '3':
                    self.display_menu()
                elif choice == '4':
                    self.image_menu()
                elif choice == '5':
                    self.audio_menu()
                elif choice == '6':
                    self.remote_menu()
                elif choice == '7':
                    self.system_info_menu()
                elif choice == '8':
                    self.advanced_menu()
                elif choice == '9':
                    self.quick_status()
                elif choice.upper() == 'C':
                    self.config_menu()
                elif choice == '0':
                    print("\nExiting...")
                    self.running = False
                else:
                    print("✗ Invalid choice")

        except KeyboardInterrupt:
            print("\n\nInterrupted by user")

        finally:
            self.proj.disconnect()
            print("✓ Disconnected")


if __name__ == "__main__":
    # Check for port argument
    port = sys.argv[1] if len(sys.argv) > 1 else 'COM10'

    cli = ProjectorCLI(port=port)
    cli.run()
