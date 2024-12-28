# lobby.py

import time
import sys
import pyfiglet

BLUE = '\033[94m'
RESET = '\033[0m'

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
   
if __name__ == "__main__":
    main()
