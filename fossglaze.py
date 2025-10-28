import re
import time
import sys
import subprocess
import argparse
import os
from pathlib import Path
from pypresence import Presence, ActivityType
from pypresence.exceptions import InvalidID, DiscordNotFound

VERSION = "v1.0" 

# change this only after you fork the repo, pleaseeeeeeeeeeee :C
CLIENT_ID = '1432701582541193236' 

LOGO_MAP = {
    'default': 'tux_logo',
    'arch': 'arch_logo',
    'omarchy': 'omarchy',
    'debian': 'debian_logo',
    'fedora': 'fedora_logo',
    'ubuntu': 'ubuntu_logo',
    'manjaro': 'manjaro_logo',
    'gentoo': 'gentoo_logo',
    'opensuse-tumbleweed': 'opensuse_logo',
    'opensuse-leap': 'opensuse_logo',
    'endeavouros': 'endeavouros_logo',
    'nixos': 'nixos_logo',
    'void': 'void_logo',
}

SETUP_TILING_INSTRUCTIONS = """
[FOSSGlaze Setup: Automatic startup for saucy DE's and WM's]

Why wouldn't you want to use this? It's a laziest way to start FOSSGlaze.
Add these lines to your config file to automatically start FOSSGlaze at login:

  For i3 or Sway (e.g., ~/.config/i3/config):
    exec --no-startup-id /usr/bin/fossglaze

  For Hyprland (e.g., ~/.config/hypr/hyprland.conf):
    exec-once = /usr/bin/fossglaze

After adding the line, save the file and reload your WM (optional, ain't
forcing you to do shi)
"""

SYSTEMD_SERVICE_CONTENT = """[Unit]
Description=FOSSGlaze Discord RPC
After=graphical-session.target
PartOf=graphical-session.target

[Service]
ExecStart=/usr/bin/fossglaze
Restart=always
RestartSec=10

[Install]
WantedBy=graphical-session.target
"""

def get_auto_distro_details():
    try:
        result = subprocess.run(
            ['omarchy-version'], 
            capture_output=True, 
            text=True, 
            check=False
        )
        version_output = result.stdout.strip()
        
        if result.returncode == 0 and version_output:
            pretty_name = "Omarchy"
            state_msg = f"Version {version_output}"
            logo_key = LOGO_MAP.get('omarchy', LOGO_MAP['default'])
            return pretty_name, state_msg, logo_key
            
    except FileNotFoundError:
        pass    
    except Exception as e:
        print_error(f"Could not run 'omarchy-version': {e}")
        pass    
    
    os_info = {}
    try:
        with open("/etc/os-release", "r") as f:
            for line in f:
                line = line.strip()
                if '=' in line:
                    key, value = line.split('=', 1)
                    os_info[key] = value.strip().strip('"')

    except FileNotFoundError:
        print_error("Could not find /etc/os-release.")
        return "A FOSS Distro", "i use linux just in case", LOGO_MAP['default']
    except Exception as e:
        print_error(f"An error occurred while reading /etc/os-release: {e}")
        return "A FOSS Distro", "i use linux just in case", LOGO_MAP['default']

    pretty_name = os_info.get('PRETTY_NAME', 'A FOSS Distro')
    distro_id = os_info.get('ID', 'default')
    id_like = os_info.get('ID_LIKE', '').split() 

    is_arch_based = (distro_id == 'arch' or 'arch' in id_like)

    if is_arch_based:
        state_msg = "i use arch btw"
        if distro_id == 'arch':
            pretty_name = "Arch Linux"
    else:
        state_msg = "i use linux just in case"

    if distro_id in LOGO_MAP:
        logo_key = LOGO_MAP[distro_id]
    else:
        found_like = False
        for parent_id in id_like:
            if parent_id in LOGO_MAP:
                logo_key = LOGO_MAP[parent_id]
                found_like = True
                break
        if not found_like:
            logo_key = LOGO_MAP['default']

    return pretty_name, state_msg, logo_key

def print_error(msg):
    print(f"FOSSGlaze Error: {msg}", file=sys.stderr)

def setup_systemd():
    print("[FOSSGlaze Setup: systemd User Service (secure :3)]")
    print("")
    print("This will probably create a service file in your home directory to run")
    print("FOSSGlaze automatically when you log in.")
    
    try:
        choice = input("Install FOSSGlaze as a systemd user service? (y/n): ").strip().lower()
    except KeyboardInterrupt:
        print("\nSetup cancelled - why would you do this.")
        return

    if choice != 'y':
        print("Setup cancelled - why would you do this.")
        return

    try:
        service_dir = Path.home() / ".config/systemd/user"
        service_path = service_dir / "fossglaze.service"

        print(f"Creating directory: {service_dir}")
        service_dir.mkdir(parents=True, exist_ok=True)

        print(f"Writing service file to: {service_path}")
        service_path.write_text(SYSTEMD_SERVICE_CONTENT)

        print("Reloading systemd user daemon...")
        subprocess.run(["systemctl", "--user", "daemon-reload"], check=True)
        
        print("Enabling and starting the service...")
        subprocess.run(["systemctl", "--user", "enable", "--now", "fossglaze.service"], check=True)
        
        print("\n[SUCCESS!]")
        print("FOSSGlaze is now installed and running automatically on login.")
        print("To check its status, run:")
        print("  systemctl --user status fossglaze.service")

    except subprocess.CalledProcessError as e:
        print_error(f"A systemctl command failed: {e}")
        print("Please try running the commands in the instructions manually.")
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        print("Setup failed. Please report this bug in FOSSGlaze's GitHub repo. Probably gonna fix it soon...")


def main():
    parser = argparse.ArgumentParser(
        description="FOSSGlaze: A Discord RPC for your Linux Distro.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f"FOSSGlaze {VERSION}",
        help="Show the application's version and exit (i'm not gonna lie, this is kinda useless)"
    )
    parser.add_argument(
        '--list-distros',
        action='store_true',
        help="List all supported distro IDs for the --distro flag and exit"
    )
    parser.add_argument(
        '--setup',
        choices=['tiling', 'systemd'],
        help="Run the interactive setup for auto-starting FOSSGlaze"
    )

    parser.add_argument(
        '--distro',
        type=str,
        help='Force a specific distro ID (e.g., "arch", "fedora"). Bypasses all auto-detection and gaslights everyone.'
    )
    
    args = parser.parse_args()
    
    if args.list_distros:
        print("Supported Distro IDs (for --distro flag and LOGO_MAP):")
        for key in LOGO_MAP:
            print(f"  - {key}")
        sys.exit(0)

    if args.setup:
        if args.setup == 'tiling':
            print(SETUP_TILING_INSTRUCTIONS)
        elif args.setup == 'systemd':
            setup_systemd()
        sys.exit(0)

    if CLIENT_ID == 'PASTE_YOUR_ONE_AND_ONLY_CLIENT_ID_HERE':
        print_error("This app is not configured by the developer.")
        print_error("Please contact the package maintainer.")
        sys.exit(1)

    RPC = None
    connected = False
    start_time = int(time.time())
    
    try:
        if args.distro:
            print(f"FOSSGlaze: User forced distro: '{args.distro}'")
            forced_id = args.distro.lower()
            
            if forced_id in LOGO_MAP:
                logo_key = LOGO_MAP[forced_id]
            else:
                print_error(f"Forced distro ID '{forced_id}' not in LOGO_MAP. Using default logo.")
                logo_key = LOGO_MAP['default']
            
            if forced_id == 'arch':
                distro_name = "Arch Linux"
            else:
                distro_name = forced_id.capitalize()

            if forced_id == 'arch':
                state_msg = "i use arch btw"
            else:
                state_msg = "i use linux just in case"

        else:
            print("FOSSGlaze: Starting. Auto-detecting distro...")
            distro_name, state_msg, logo_key = get_auto_distro_details()

        print(f"FOSSGlaze: Distro set to: {distro_name}.")
        print(f"FOSSGlaze: Status will be: '{state_msg}'")
        print(f"FOSSGlaze: Using logo asset '{logo_key}'.")

    except Exception as e:
        print_error(f"Failed to initialize: {e}")
        sys.exit(1)

    while True:
        try:
            if not RPC:
                RPC = Presence(CLIENT_ID)
            
            RPC.connect()
            connected = True
            print("FOSSGlaze: Successfully connected to Discord.")

            presence_data = {
                "activity_type": ActivityType.WATCHING,
                "name": distro_name,
                "details": state_msg,                 
                "large_image": logo_key,
                "large_text": distro_name,
                "start": start_time
            }
            
            RPC.update(**presence_data)
            print("FOSSGlaze: Status is now live!")
            
            while True:
                time.sleep(300) 

        except InvalidID:
            print_error("Invalid Client ID configured. Please contact the maintainer.")
            break 
        except (ConnectionRefusedError, DiscordNotFound):
            print_error("Could not connect to Discord.")
            print_error("Is your Discord desktop client open? (Try Discord Canary)")
            print("FOSSGlaze: Retrying in 60 seconds...")
            connected = False 
            if RPC:
                try:
                    RPC.close()
                except Exception:
                    pass 
                RPC = None
            time.sleep(60)
        except KeyboardInterrupt:
            print("\nFOSSGlaze: Exiting...")
            if connected and RPC:
                RPC.close()
            break
        except Exception as e:
            print_error(f"An unexpected error occurred: {e}")
            if connected and RPC:
                RPC.close()
            connected = False
            RPC = None
            print("FOSSGlaze: Retrying in 60 seconds...")
            time.sleep(60)

if __name__ == "__main__":
    main()

