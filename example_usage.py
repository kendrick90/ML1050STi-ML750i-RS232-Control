#!/usr/bin/env python3
"""
Example Usage Scripts for Projector Control
Demonstrates common operations and workflows
"""

from projector_control import ProjectorController
import time


def example_quick_status():
    """Example: Quick status check"""
    print("=" * 60)
    print("EXAMPLE 1: Quick Status Check")
    print("=" * 60)

    with ProjectorController(port='COM10') as proj:
        # Get basic info
        power = proj.get_power_state()
        source = proj.get_input_source()
        mode = proj.get_display_mode()
        volume = proj.get_volume()

        print(f"\nPower: {'ON' if power else 'OFF'}")
        print(f"Source: {source}")
        print(f"Display Mode: {mode}")
        print(f"Volume: {volume}/10")

        # Get system health
        temp = proj.get_temperature()
        hours = proj.get_lamp_hours()

        print(f"\nTemperature: {temp}°C")
        print(f"Runtime: {hours} hours")


def example_presentation_setup():
    """Example: Automated presentation setup"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Presentation Setup")
    print("=" * 60)

    with ProjectorController(port='COM10') as proj:
        print("\nConfiguring projector for presentation...")

        # Check if already on
        if not proj.get_power_state():
            print("  - Powering on projector...")
            proj.power_on()
            print("  - Waiting for warmup (30 seconds)...")
            time.sleep(30)
        else:
            print("  - Already powered on")

        # Configure settings
        print("  - Setting source to HDMI...")
        proj.set_source_hdmi()

        print("  - Setting display mode to Presentation...")
        proj.set_display_mode_presentation()

        print("  - Setting aspect ratio to 16:9...")
        proj.set_aspect_16_9()

        print("  - Setting brightness to 8...")
        proj.set_brightness(8)

        print("  - Setting contrast to 5...")
        proj.set_contrast(5)

        print("\n✓ Presentation setup complete!")


def example_movie_mode():
    """Example: Switch to cinema/movie mode"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Movie Mode Setup")
    print("=" * 60)

    with ProjectorController(port='COM10') as proj:
        print("\nConfiguring projector for movie viewing...")

        print("  - Setting display mode to Cinema...")
        proj.set_display_mode_cinema()

        print("  - Setting color temperature to Warm...")
        proj.set_color_temp_warm()

        print("  - Setting aspect ratio to Auto...")
        proj.set_aspect_auto()

        print("  - Setting brightness to 5...")
        proj.set_brightness(5)

        print("  - Setting contrast to 6...")
        proj.set_contrast(6)

        print("\n✓ Movie mode configured!")


def example_health_monitoring():
    """Example: System health check"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: System Health Monitoring")
    print("=" * 60)

    with ProjectorController(port='COM10') as proj:
        print("\nChecking projector health...\n")

        # Temperature check
        temp = proj.get_temperature()
        if temp:
            print(f"Temperature: {temp}°C", end="")
            if temp > 70:
                print(" ⚠️ HIGH!")
            elif temp > 60:
                print(" (warm)")
            else:
                print(" (normal)")

        # Fan speeds
        fans = proj.get_fan_speeds()
        print("\nFan Speeds:")
        for fan_name, rpm in fans.items():
            if rpm:
                status = "⚠️ LOW!" if rpm < 1000 else "✓"
                print(f"  {fan_name}: {rpm} RPM {status}")
            else:
                print(f"  {fan_name}: Unknown")

        # Usage hours
        lamp_hours = proj.get_lamp_hours()
        system_hours = proj.get_system_hours()
        print(f"\nUsage Statistics:")
        print(f"  Lamp Hours: {lamp_hours}")
        print(f"  System Hours: {system_hours}")

        # Signal status
        signal = proj.get_signal_status()
        resolution = proj.get_resolution()
        refresh = proj.get_refresh_rate()

        print(f"\nSignal Status:")
        print(f"  Active: {'Yes ✓' if signal else 'No ✗' if signal is False else 'Unknown'}")
        if resolution:
            print(f"  Resolution: {resolution}")
        if refresh:
            print(f"  Refresh Rate: {refresh}")


def example_power_cycle():
    """Example: Safe power cycle"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Power Cycle")
    print("=" * 60)

    with ProjectorController(port='COM10') as proj:
        # Check current state
        is_on = proj.get_power_state()
        print(f"\nCurrent power state: {'ON' if is_on else 'OFF'}")

        if is_on:
            print("\nPowering off...")
            if proj.power_off():
                print("✓ Power off command sent")
                print("  (Projector will cool down before shutting off)")
        else:
            print("\nPowering on...")
            if proj.power_on():
                print("✓ Power on command sent")
                print("  (Projector will warm up for ~30 seconds)")


def example_source_cycling():
    """Example: Cycle through sources"""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Source Testing")
    print("=" * 60)

    with ProjectorController(port='COM10') as proj:
        sources = [
            ("HDMI", proj.set_source_hdmi),
            ("USB-A", proj.set_source_usb),
            ("Android Home", proj.set_source_android_home),
        ]

        print("\nTesting each input source...\n")

        for source_name, set_func in sources:
            print(f"Switching to {source_name}...", end=" ")
            if set_func():
                print("✓")
                time.sleep(2)  # Give time to switch

                # Check signal
                signal = proj.get_signal_status()
                if signal:
                    res = proj.get_resolution()
                    print(f"  Signal detected: {res if res else 'Unknown resolution'}")
                else:
                    print("  No signal detected")
            else:
                print("✗ Failed")


def example_comprehensive_info():
    """Example: Get all available information"""
    print("\n" + "=" * 60)
    print("EXAMPLE 7: Comprehensive Information Dump")
    print("=" * 60)

    with ProjectorController(port='COM10') as proj:
        print("\nRetrieving all projector information...\n")

        # System info
        info = proj.get_system_info()
        print("=== SYSTEM INFO ===")
        for key, val in info.items():
            print(f"  {key}: {val}")

        # Software versions
        versions = proj.get_software_version()
        print("\n=== SOFTWARE VERSIONS ===")
        for key, val in versions.items():
            print(f"  {key}: {val}")

        # Network
        print("\n=== NETWORK ===")
        print(f"  MAC Address: {proj.get_mac_address()}")
        print(f"  WiFi Status: {proj.get_network_status()}")
        print(f"  Device ID: {proj.get_device_id()}")

        # Display settings
        print("\n=== DISPLAY SETTINGS ===")
        print(f"  Display Mode: {proj.get_display_mode()}")
        print(f"  Projection Mode: {proj.get_projection_mode()}")
        print(f"  Aspect Ratio: {proj.get_aspect_ratio()}")
        print(f"  Brightness: {proj.get_brightness()}")
        print(f"  Contrast: {proj.get_contrast()}")
        print(f"  Color Temperature: {proj.get_color_temperature()}")

        # Audio
        print("\n=== AUDIO ===")
        print(f"  Volume: {proj.get_volume()}")
        print(f"  Audio Mute: {proj.get_audio_mute_state()}")
        print(f"  AV Mute: {proj.get_av_mute_state()}")

        # Hardware status
        print("\n=== HARDWARE STATUS ===")
        print(f"  Temperature: {proj.get_temperature()}°C")

        fans = proj.get_fan_speeds()
        for fan_name, rpm in fans.items():
            print(f"  {fan_name}: {rpm} RPM" if rpm else f"  {fan_name}: Unknown")


def main():
    """Run all examples"""
    print("\n" + "╔" + "=" * 58 + "╗")
    print("║  PROJECTOR CONTROL - EXAMPLE USAGE DEMONSTRATIONS       ║")
    print("╚" + "=" * 58 + "╝")

    examples = [
        ("Quick Status Check", example_quick_status),
        ("Presentation Setup", example_presentation_setup),
        ("Movie Mode Setup", example_movie_mode),
        ("Health Monitoring", example_health_monitoring),
        ("Power Cycle", example_power_cycle),
        ("Source Testing", example_source_cycling),
        ("Comprehensive Info", example_comprehensive_info),
    ]

    print("\nAvailable Examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  [{i}] {name}")
    print(f"  [A] Run All")
    print(f"  [Q] Quit")

    choice = input("\nSelect example to run: ").strip().upper()

    if choice == 'Q':
        return

    if choice == 'A':
        for name, func in examples:
            try:
                func()
                time.sleep(1)
            except Exception as e:
                print(f"\n✗ Error in {name}: {e}")
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(examples):
                examples[idx][1]()
            else:
                print("Invalid choice")
        except ValueError:
            print("Invalid choice")
        except Exception as e:
            print(f"\n✗ Error: {e}")

    print("\n" + "=" * 60)
    print("Example complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
