#!/usr/bin/env python3
"""
Projector Configuration Save/Load System
Allows saving and restoring projector settings
"""

import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from projector_control import ProjectorController


class ProjectorConfig:
    """Manage projector configuration save/load operations"""

    def __init__(self, controller: ProjectorController):
        """
        Initialize config manager

        Args:
            controller: ProjectorController instance
        """
        self.controller = controller

    def capture_config(self) -> Dict[str, Any]:
        """
        Capture all current projector settings

        Returns:
            Dictionary containing all readable settings
        """
        config = {
            'metadata': {
                'captured_at': datetime.now().isoformat(),
                'device_id': self.controller.get_device_id(),
                'mac_address': self.controller.get_mac_address(),
            },
            'power': {},
            'source': {},
            'display': {},
            'image': {},
            'audio': {},
            'geometry': {},
            'system_info': {},
        }

        # Power state
        config['power']['state'] = self.controller.get_power_state()

        # Source
        config['source']['input'] = self.controller.get_input_source()

        # Display settings
        config['display']['mode'] = self.controller.get_display_mode()
        config['display']['projection_mode'] = self.controller.get_projection_mode()
        config['display']['aspect_ratio'] = self.controller.get_aspect_ratio()
        config['display']['digital_zoom'] = self.controller.get_digital_zoom()

        # Image settings
        config['image']['brightness'] = self.controller.get_brightness()
        config['image']['contrast'] = self.controller.get_contrast()
        config['image']['color_temperature'] = self.controller.get_color_temperature()

        # Audio settings
        config['audio']['volume'] = self.controller.get_volume()
        config['audio']['audio_mute'] = self.controller.get_audio_mute_state()
        config['audio']['av_mute'] = self.controller.get_av_mute_state()

        # Geometry/Keystone
        config['geometry']['v_keystone'] = self.controller.get_v_keystone()

        # System info (read-only, for reference)
        config['system_info']['software_versions'] = self.controller.get_software_version()
        config['system_info']['lamp_hours'] = self.controller.get_lamp_hours()
        config['system_info']['system_hours'] = self.controller.get_system_hours()
        config['system_info']['temperature'] = self.controller.get_temperature()
        config['system_info']['fan_speeds'] = self.controller.get_fan_speeds()
        config['system_info']['network_status'] = self.controller.get_network_status()
        config['system_info']['digital_signage'] = self.controller.get_digital_signage_status()

        return config

    def apply_config(self, config: Dict[str, Any], skip_power: bool = True) -> Dict[str, Any]:
        """
        Apply configuration to projector

        Args:
            config: Configuration dictionary (from capture_config or file)
            skip_power: If True, don't change power state (default: True)

        Returns:
            Dictionary with results of each setting attempt
        """
        results = {
            'success': [],
            'failed': [],
            'skipped': []
        }

        # Power (usually skip to avoid accidental shutdown)
        if skip_power:
            results['skipped'].append('power.state')
        else:
            if 'power' in config and 'state' in config['power']:
                power_state = config['power']['state']
                if power_state is True:
                    if self.controller.power_on():
                        results['success'].append('power.state=on')
                    else:
                        results['failed'].append('power.state=on')
                elif power_state is False:
                    if self.controller.power_off():
                        results['success'].append('power.state=off')
                    else:
                        results['failed'].append('power.state=off')

        # Source
        if 'source' in config and 'input' in config['source']:
            source = config['source']['input']
            success = False
            if 'HDMI' in str(source):
                success = self.controller.set_source_hdmi()
            elif 'USB' in str(source):
                success = self.controller.set_source_usb()
            elif 'SD' in str(source):
                success = self.controller.set_source_sd_card()
            elif 'Android' in str(source) or 'Home' in str(source):
                success = self.controller.set_source_android_home()

            if success:
                results['success'].append(f'source.input={source}')
            else:
                results['failed'].append(f'source.input={source}')

        # Display mode
        if 'display' in config:
            display = config['display']

            if 'mode' in display and display['mode']:
                mode = display['mode']
                success = False
                mode_lower = str(mode).lower()

                if 'presentation' in mode_lower or 'pc' in mode_lower:
                    success = self.controller.set_display_mode_presentation()
                elif 'bright' in mode_lower:
                    success = self.controller.set_display_mode_bright()
                elif 'cinema' in mode_lower:
                    success = self.controller.set_display_mode_cinema()
                elif 'srgb' in mode_lower:
                    success = self.controller.set_display_mode_srgb()
                elif '3d' in mode_lower:
                    success = self.controller.set_display_mode_3d()
                elif 'game' in mode_lower:
                    success = self.controller.set_display_mode_game()
                elif 'hdr' in mode_lower:
                    success = self.controller.set_display_mode_hdr()
                elif 'hlg' in mode_lower:
                    success = self.controller.set_display_mode_hlg()
                elif 'ai-pq' in mode_lower or 'aipq' in mode_lower:
                    success = self.controller.set_display_mode_ai_pq()
                elif 'wcg' in mode_lower:
                    success = self.controller.set_display_mode_wcg()
                elif 'photo' in mode_lower or 'vivid' in mode_lower:
                    success = self.controller.set_display_mode_photo()
                elif 'eco' in mode_lower:
                    success = self.controller.set_display_mode_eco()

                if success:
                    results['success'].append(f'display.mode={mode}')
                else:
                    results['failed'].append(f'display.mode={mode}')

            # Projection mode
            if 'projection_mode' in display and display['projection_mode']:
                proj_mode = display['projection_mode']
                success = False

                if 'Front-Desktop' in proj_mode:
                    success = self.controller.set_projection_front_desktop()
                elif 'Rear-Desktop' in proj_mode:
                    success = self.controller.set_projection_rear_desktop()
                elif 'Front-Ceiling' in proj_mode:
                    success = self.controller.set_projection_front_ceiling()
                elif 'Rear-Ceiling' in proj_mode:
                    success = self.controller.set_projection_rear_ceiling()

                if success:
                    results['success'].append(f'display.projection_mode={proj_mode}')
                else:
                    results['failed'].append(f'display.projection_mode={proj_mode}')

            # Aspect ratio
            if 'aspect_ratio' in display and display['aspect_ratio']:
                aspect = display['aspect_ratio']
                success = False

                if '4:3' in aspect:
                    success = self.controller.set_aspect_4_3()
                elif '16:9' in aspect:
                    success = self.controller.set_aspect_16_9()
                elif '16:10' in aspect:
                    success = self.controller.set_aspect_16_10()
                elif 'Auto' in aspect:
                    success = self.controller.set_aspect_auto()

                if success:
                    results['success'].append(f'display.aspect_ratio={aspect}')
                else:
                    results['failed'].append(f'display.aspect_ratio={aspect}')

            # Digital zoom
            if 'digital_zoom' in display and display['digital_zoom']:
                zoom = display['digital_zoom']
                zoom_map = {
                    '50%': 0, '75%': 1, '100%': 2, '125%': 3,
                    '150%': 4, '175%': 5, '200%': 6
                }
                if zoom in zoom_map:
                    if self.controller.set_digital_zoom(zoom_map[zoom]):
                        results['success'].append(f'display.digital_zoom={zoom}')
                    else:
                        results['failed'].append(f'display.digital_zoom={zoom}')

        # Image settings
        if 'image' in config:
            image = config['image']

            if 'brightness' in image and image['brightness'] is not None:
                if self.controller.set_brightness(image['brightness']):
                    results['success'].append(f"image.brightness={image['brightness']}")
                else:
                    results['failed'].append(f"image.brightness={image['brightness']}")

            if 'contrast' in image and image['contrast'] is not None:
                if self.controller.set_contrast(image['contrast']):
                    results['success'].append(f"image.contrast={image['contrast']}")
                else:
                    results['failed'].append(f"image.contrast={image['contrast']}")

            if 'color_temperature' in image and image['color_temperature']:
                color_temp = image['color_temperature']
                success = False

                if 'Standard' in color_temp:
                    success = self.controller.set_color_temp_standard()
                elif 'Cold' in color_temp:
                    success = self.controller.set_color_temp_cold()
                elif 'Warm' in color_temp:
                    success = self.controller.set_color_temp_warm()

                if success:
                    results['success'].append(f'image.color_temperature={color_temp}')
                else:
                    results['failed'].append(f'image.color_temperature={color_temp}')

        # Audio settings
        if 'audio' in config:
            audio = config['audio']

            if 'volume' in audio and audio['volume'] is not None:
                # Can't set volume directly, but we can try to get close
                current = self.controller.get_volume()
                target = audio['volume']
                if current is not None and target is not None:
                    if target > current:
                        for _ in range(target - current):
                            self.controller.volume_up()
                        results['success'].append(f'audio.volume={target}')
                    elif target < current:
                        for _ in range(current - target):
                            self.controller.volume_down()
                        results['success'].append(f'audio.volume={target}')
                    else:
                        results['success'].append(f'audio.volume={target} (unchanged)')

            if 'audio_mute' in audio and audio['audio_mute'] is not None:
                if audio['audio_mute']:
                    if self.controller.audio_mute_on():
                        results['success'].append('audio.audio_mute=on')
                    else:
                        results['failed'].append('audio.audio_mute=on')
                else:
                    if self.controller.audio_mute_off():
                        results['success'].append('audio.audio_mute=off')
                    else:
                        results['failed'].append('audio.audio_mute=off')

            if 'av_mute' in audio and audio['av_mute'] is not None:
                if audio['av_mute']:
                    if self.controller.av_mute_on():
                        results['success'].append('audio.av_mute=on')
                    else:
                        results['failed'].append('audio.av_mute=on')
                else:
                    if self.controller.av_mute_off():
                        results['success'].append('audio.av_mute=off')
                    else:
                        results['failed'].append('audio.av_mute=off')

        return results

    def save_to_file(self, filepath: str, format: str = 'json') -> bool:
        """
        Capture current config and save to file

        Args:
            filepath: Path to save file
            format: 'json' or 'yaml' (default: 'json')

        Returns:
            True if successful
        """
        try:
            config = self.capture_config()

            path = Path(filepath)
            path.parent.mkdir(parents=True, exist_ok=True)

            if format.lower() == 'yaml':
                with open(path, 'w') as f:
                    yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            else:  # json
                with open(path, 'w') as f:
                    json.dump(config, f, indent=2)

            return True

        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def load_from_file(self, filepath: str) -> Optional[Dict[str, Any]]:
        """
        Load config from file

        Args:
            filepath: Path to config file

        Returns:
            Configuration dictionary or None if error
        """
        try:
            path = Path(filepath)

            if path.suffix in ['.yaml', '.yml']:
                with open(path, 'r') as f:
                    return yaml.safe_load(f)
            else:  # assume json
                with open(path, 'r') as f:
                    return json.load(f)

        except Exception as e:
            print(f"Error loading config: {e}")
            return None

    def restore_from_file(self, filepath: str, skip_power: bool = True) -> Dict[str, Any]:
        """
        Load config from file and apply to projector

        Args:
            filepath: Path to config file
            skip_power: If True, don't change power state

        Returns:
            Results dictionary
        """
        config = self.load_from_file(filepath)
        if config is None:
            return {'success': [], 'failed': ['load_file'], 'skipped': []}

        return self.apply_config(config, skip_power=skip_power)


def main():
    """CLI tool for config management"""
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Projector Configuration Management')
    parser.add_argument('--port', default='COM10', help='Serial port (default: COM10)')
    parser.add_argument('action', choices=['save', 'load', 'show'],
                        help='Action: save, load, or show config')
    parser.add_argument('file', nargs='?', help='Config file path')
    parser.add_argument('--format', choices=['json', 'yaml'], default='json',
                        help='File format (default: json)')
    parser.add_argument('--include-power', action='store_true',
                        help='Include power state when loading config')

    args = parser.parse_args()

    if args.action in ['save', 'load'] and not args.file:
        print("Error: file path required for save/load")
        sys.exit(1)

    with ProjectorController(port=args.port) as controller:
        config_manager = ProjectorConfig(controller)

        if args.action == 'save':
            print(f"Capturing configuration from projector...")
            if config_manager.save_to_file(args.file, format=args.format):
                print(f"✓ Configuration saved to {args.file}")
            else:
                print(f"✗ Failed to save configuration")
                sys.exit(1)

        elif args.action == 'load':
            print(f"Loading configuration from {args.file}...")
            results = config_manager.restore_from_file(args.file,
                                                       skip_power=not args.include_power)

            print("\n=== Results ===")
            print(f"✓ Success: {len(results['success'])}")
            for item in results['success']:
                print(f"  - {item}")

            if results['failed']:
                print(f"\n✗ Failed: {len(results['failed'])}")
                for item in results['failed']:
                    print(f"  - {item}")

            if results['skipped']:
                print(f"\n⊝ Skipped: {len(results['skipped'])}")
                for item in results['skipped']:
                    print(f"  - {item}")

        elif args.action == 'show':
            print("Capturing current configuration...\n")
            config = config_manager.capture_config()

            # Print formatted config
            print("=" * 70)
            print("PROJECTOR CONFIGURATION")
            print("=" * 70)

            print(f"\nCaptured: {config['metadata']['captured_at']}")
            print(f"Device ID: {config['metadata']['device_id']}")
            print(f"MAC: {config['metadata']['mac_address']}")

            for section, settings in config.items():
                if section != 'metadata':
                    print(f"\n[{section.upper()}]")
                    for key, value in settings.items():
                        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
