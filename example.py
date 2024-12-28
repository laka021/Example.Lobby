# example.py

import time
import sys
import pyfiglet

# ANSI escape codes for colors
BLUE = '\033[94m'
RESET = '\033[0m'

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

def main():
    animated_welcome_message()
    # You can add more functionalities here as needed

if __name__ == "__main__":
    main()
