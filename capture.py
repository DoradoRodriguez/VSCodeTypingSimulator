import time
import cv2
import numpy as np
import os
import pygame
from vscode_mockup import VSCodeMockup

def record_video(source_file, output_file, duration):
    # Configure video capture
    screen_size = (1280, 720)  # Fixed size for mockup
    
    # Use MJPG with AVI format for better compatibility
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(
        output_file + '.avi',
        fourcc,
        30.0,
        screen_size
    )
    
    if not out.isOpened():
        print("Error: Could not initialize video recording.")
        return
        
    print("Recording started successfully")
    
    try:
        # Read source code
        with open(source_file, 'r', encoding='utf-8') as file:
            code = file.read()
        
        # Initialize mockup
        mockup = VSCodeMockup()
        
        # Simulate typing and record
        mockup.simulate_typing(code, out)
            
    finally:
        out.release()
        cv2.destroyAllWindows()
        pygame.quit()

if __name__ == "__main__":
    # Request file name from user
    source_file = input("Enter the file name to simulate (including .py extension): ")
    output_file = input("Enter the output file name (without extension): ")
    duration = int(input("Enter recording duration in seconds: "))
    
    # Verify file exists
    if not os.path.exists(source_file):
        print(f"Error: File '{source_file}' does not exist.")
        exit(1)
    
    # Get absolute path
    source_file = os.path.abspath(source_file)
    
    print(f"\nStarting recording in 3 seconds...")
    print(f"Source file: {source_file}")
    print(f"Output file: {output_file}.avi")
    print(f"Duration: {duration} seconds")
    print("\nPlease:")
    print("1. Don't move the mouse or use keyboard during recording")
    print("2. Wait for the process to finish")
    
    time.sleep(3)
    record_video(source_file, output_file, duration)
