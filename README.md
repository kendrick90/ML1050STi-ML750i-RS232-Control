# Projector RS232 Control Interface

Comprehensive Python control interface for ML1050STi / ML750i projectors via RS232.

## Features

Complete implementation of the DDP RS232 protocol including:

- **Power Control** - On/Off, status query
- **Source Switching** - HDMI, USB-A, SD Card, Android Home
- **Display Modes** - Presentation, Bright, Cinema, sRGB, Photo, Eco, 3D, Game, HDR, HLG, AI-PQ, WCG
- **Image Adjustments** - Brightness, Contrast, Color Temperature, Freeze, Digital Zoom (50%-200%)
- **Audio Control** - Volume, Mute, AV Mute
- **Projection Settings** - Front/Rear, Desktop/Ceiling, Aspect Ratio
- **Keystone** - Auto keystone control, manual adjustment query
- **Remote Functions** - Navigate OSD menus programmatically
- **System Info** - Temperature, fan speeds, lamp hours, versions, network status
- **Advanced** - Digital signage, language, factory reset
- **Config Management** - Save/load complete projector settings to JSON/YAML files

## Files

- **`projector_control.py`** - Main control library (ProjectorController class)
- **`projector_cli.py`** - Interactive CLI interface
- **`projector_config.py`** - Configuration save/load system
- **`projector_status.py`** - Quick status query tool
- **`projector_test.py`** - Connection diagnostic tool
- **`example_usage.py`** - Example scripts demonstrating common operations
- **`Software_DDP_RS-232 Table_20240215.xlsx`** - Official protocol specification

## Requirements

```bash
pip install pyserial pandas openpyxl pyyaml
```

## Quick Start

### 1. Interactive CLI

Launch the interactive menu interface:

```bash
python projector_cli.py
```

Or specify a different COM port:

```bash
python projector_cli.py COM5
```

### 2. Quick Status Check

```bash
python projector_status.py
```

Output example:
```
=== Projector Status ===
Power Status:    On
Lamp Hours:      00007
Input Source:    HDMI 1
Firmware Ver:    C090
Picture Mode:    Presentation (PC)
Temperature:     62°C
```

### 3. Python Library Usage

```python
from projector_control import ProjectorController

# Using context manager (recommended)
with ProjectorController(port='COM10') as proj:
    # Power control
    proj.power_on()
    is_on = proj.get_power_state()

    # Source switching
    proj.set_source_hdmi()
    current_source = proj.get_input_source()

    # Display settings
    proj.set_display_mode_cinema()
    proj.set_brightness(7)
    proj.set_contrast(5)

    # Audio
    proj.volume_up()
    proj.audio_mute_on()

    # System info
    info = proj.get_system_info()
    print(f"Lamp hours: {info['lamp_hours']}")
    print(f"Temperature: {proj.get_temperature()}°C")

# Or manual connection management
proj = ProjectorController(port='COM10')
proj.connect()
proj.power_on()
proj.disconnect()
```

## API Reference

### Power Control

```python
proj.power_on()                    # Turn projector on
proj.power_off()                   # Turn projector off
proj.get_power_state()             # Returns True/False/None
```

### Source Control

```python
proj.set_source_hdmi()             # Switch to HDMI 1
proj.set_source_usb()              # Switch to USB-A
proj.set_source_sd_card()          # Switch to SD Card
proj.set_source_android_home()     # Switch to Android Home
proj.get_input_source()            # Get current source
```

### Display Modes

```python
proj.set_display_mode_presentation()   # PC/Presentation mode
proj.set_display_mode_bright()         # Bright mode
proj.set_display_mode_cinema()         # Cinema mode
proj.set_display_mode_srgb()           # sRGB mode
proj.set_display_mode_photo()          # Photo (Vivid) mode
proj.set_display_mode_eco()            # Eco mode
proj.set_display_mode_3d()             # 3D mode
proj.set_display_mode_game()           # Game mode
proj.set_display_mode_hdr()            # HDR mode
proj.set_display_mode_hlg()            # HLG mode
proj.set_display_mode_ai_pq()          # AI-PQ mode
proj.set_display_mode_wcg()            # WCG (Wide Color Gamut) mode
proj.get_display_mode()                # Get current mode
```

### Image Settings

```python
proj.set_brightness(0-10)          # Set brightness
proj.get_brightness()              # Get brightness
proj.set_contrast(0-10)            # Set contrast
proj.get_contrast()                # Get contrast

proj.set_color_temp_standard()     # Color temp: Standard (D75)
proj.set_color_temp_cold()         # Color temp: Cold (D83)
proj.set_color_temp_warm()         # Color temp: Warm (D65)
proj.get_color_temperature()       # Get color temp

proj.freeze_on()                   # Freeze image
proj.freeze_off()                  # Unfreeze image
```

### Audio Control

```python
proj.volume_up()                   # Increase volume
proj.volume_down()                 # Decrease volume
proj.get_volume()                  # Get volume (0-10)

proj.audio_mute_on()               # Mute audio
proj.audio_mute_off()              # Unmute audio
proj.get_audio_mute_state()        # Get mute state

proj.av_mute_on()                  # Mute video and audio
proj.av_mute_off()                 # Unmute video and audio
proj.get_av_mute_state()           # Get AV mute state
```

### Projection Settings

```python
proj.set_projection_front_desktop()    # Front projection, desktop
proj.set_projection_rear_desktop()     # Rear projection, desktop
proj.set_projection_front_ceiling()    # Front projection, ceiling
proj.set_projection_rear_ceiling()     # Rear projection, ceiling
proj.get_projection_mode()             # Get current mode

proj.set_aspect_4_3()                  # 4:3 aspect ratio
proj.set_aspect_16_9()                 # 16:9 aspect ratio
proj.set_aspect_16_10()                # 16:10 aspect ratio
proj.set_aspect_auto()                 # Auto aspect ratio
proj.get_aspect_ratio()                # Get current ratio

proj.set_auto_keystone_on()            # Enable auto keystone
proj.set_auto_keystone_off()           # Disable auto keystone
proj.get_v_keystone()                  # Get V keystone value (-40 to +40)
```

### Digital Zoom

```python
proj.set_digital_zoom(level)           # Set zoom level (0-6)
proj.set_digital_zoom_50()             # 50% zoom
proj.set_digital_zoom_75()             # 75% zoom
proj.set_digital_zoom_100()            # 100% zoom (normal)
proj.set_digital_zoom_125()            # 125% zoom
proj.set_digital_zoom_150()            # 150% zoom
proj.set_digital_zoom_175()            # 175% zoom
proj.set_digital_zoom_200()            # 200% zoom
proj.get_digital_zoom()                # Get current zoom level
```

### Remote Control Functions

```python
proj.remote_menu()                 # Open OSD menu
proj.remote_up()                   # Navigate up
proj.remote_down()                 # Navigate down
proj.remote_left()                 # Navigate left
proj.remote_right()                # Navigate right
proj.remote_enter()                # Select/Enter
```

### System Information

```python
# Comprehensive system info
info = proj.get_system_info()
# Returns: {'power', 'lamp_hours', 'input_source', 'firmware', 'picture_mode'}

# Software versions
versions = proj.get_software_version()
# Returns: {'DDP', 'MCU', 'Android', 'LAN', 'HDBaseT', ...}

# Hardware status
proj.get_lamp_hours()              # Get light source hours
proj.get_system_hours()            # Get total system hours
proj.get_temperature()             # Get temperature in °C
proj.get_fan_speeds()              # Get all fan speeds (RPM)

# Network info
proj.get_mac_address()             # Get MAC address
proj.get_network_status()          # Get WiFi connection status
proj.get_device_id()               # Get projector ID (00-99)

# Signal info
proj.get_signal_status()           # Check if signal is active
proj.get_resolution()              # Get source resolution
proj.get_refresh_rate()            # Get refresh rate
```

### Advanced Settings

```python
proj.set_digital_signage_on()      # Enable digital signage mode
proj.set_digital_signage_off()     # Disable digital signage mode
proj.get_digital_signage_status()  # Get DS status

proj.set_language(code)            # Set OSD language (1-22)
                                   # 1=English, 2=German, 3=French, etc.

proj.reset_osd_settings()          # Reset OSD to defaults
proj.factory_reset()               # Factory reset (use with caution!)
```

### Configuration Management

Save and restore complete projector settings:

```python
from projector_config import ProjectorConfig

with ProjectorController() as proj:
    config_mgr = ProjectorConfig(proj)

    # Save current config to file
    config_mgr.save_to_file('my_settings.json', format='json')
    config_mgr.save_to_file('my_settings.yaml', format='yaml')

    # Load config from file
    config = config_mgr.load_from_file('my_settings.json')

    # Apply config to projector (skip_power=True by default)
    results = config_mgr.apply_config(config, skip_power=True)

    # Or load and apply in one step
    results = config_mgr.restore_from_file('my_settings.json')

    # Capture current settings
    current_config = config_mgr.capture_config()
```

Command-line tool:

```bash
# Save current config
python projector_config.py save my_config.json

# Save as YAML
python projector_config.py save my_config.yaml --format yaml

# Load and apply config
python projector_config.py load my_config.json

# Include power state when loading
python projector_config.py load my_config.json --include-power

# Show current config
python projector_config.py show
```

## Connection Settings

Default settings for the projector:
- **Port**: COM10 (configurable)
- **Baud Rate**: 9600
- **Data Bits**: 8
- **Parity**: None
- **Stop Bits**: 1
- **Flow Control**: None

The PL2303 USB-to-RS232 adapter works well with this projector.

## Protocol Details

Commands follow the format: `~{ID}{COMMAND}\r`

- **Device ID**: `00` for broadcast (can be 00-99 for specific projectors)
- **Responses**:
  - `P` = Success (for SET commands)
  - `Ok{data}` = Success with data (for GET commands)
  - `F` = Fail

Example:
```
TX: ~00124 1\r   (Query power state)
RX: Ok1\r        (Power is ON)
```

## Troubleshooting

### No response from projector

1. Check projector is powered on (not in standby)
2. Verify COM port number in Device Manager
3. Ensure USB-to-RS232 adapter is properly connected
4. Check cable is not a null-modem cable (should be straight-through)
5. Run diagnostic: `python projector_test.py`

### Wrong COM port

```python
# List available ports
python -m serial.tools.list_ports

# Use specific port
proj = ProjectorController(port='COM5')
```

### PL2303 driver issues

If using a PL2303 adapter and getting errors:
1. Install latest Prolific PL2303 drivers
2. Some clone chips require older drivers
3. Try a different USB port

## Examples

### Example 1: Automated Presentation Setup

```python
from projector_control import ProjectorController
import time

with ProjectorController() as proj:
    print("Setting up for presentation...")

    # Power on and wait
    proj.power_on()
    time.sleep(30)  # Wait for warmup

    # Configure settings
    proj.set_source_hdmi()
    proj.set_display_mode_presentation()
    proj.set_aspect_16_9()
    proj.set_brightness(8)
    proj.set_projection_front_ceiling()

    print("✓ Ready for presentation")
```

### Example 2: Health Monitoring

```python
from projector_control import ProjectorController

with ProjectorController() as proj:
    # Get system health
    temp = proj.get_temperature()
    fans = proj.get_fan_speeds()
    hours = proj.get_lamp_hours()

    # Check for issues
    if temp and temp > 70:
        print(f"⚠️ High temperature: {temp}°C")

    for fan_name, rpm in fans.items():
        if rpm and rpm < 1000:
            print(f"⚠️ {fan_name} running slow: {rpm} RPM")

    print(f"Lamp hours: {hours}")
```

### Example 3: Batch Control Multiple Projectors

```python
from projector_control import ProjectorController

projectors = [
    ProjectorController(port='COM10', device_id='01'),
    ProjectorController(port='COM11', device_id='02'),
]

for i, proj in enumerate(projectors, 1):
    with proj:
        print(f"Configuring projector {i}...")
        proj.power_on()
        proj.set_source_hdmi()
        proj.set_display_mode_cinema()
```

## License

This implementation is based on the official DDP RS232 protocol specification (Software_DDP_RS-232 Table_20240215.xlsx).

## Support

For protocol questions, refer to the official specification document included in this directory.
