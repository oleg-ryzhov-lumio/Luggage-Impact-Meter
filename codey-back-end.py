import codey
import time

# --- Configuration & Thresholds ---
# Adjust this threshold to define what counts as a "significant impact" (in Gs)
SIGNIFICANT_THRESHOLD = 2.0

# Multi-list to store the filtered telemetry data
# Format per entry: [timestamp, intensity, impact_type]
final_impact_log = []

# State flag to control the recording window
is_recording = False

def get_current_timestamp():
    """
    Generates a mock local time string based on system uptime.
    Note: Codey Rocky lacks an internal real-time clock (RTC) battery,
    so baseline synchronization usually relies on the live computer connection.
    """
    current_seconds = int(time.time())
    hours = (current_seconds // 3600) % 24
    minutes = (current_seconds // 60) % 60
    seconds = current_seconds % 60
    return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

def classify_impact_type():
    """
    Classifies the movement profile based on which axis registered the primary force
    or if a sudden state change matches structural movement profiles.
    """
    # Check integrated orientation/motion states
    if codey.is_shaking():
        return "toss"
    
    x = abs(codey.get_acceleration('x'))
    y = abs(codey.get_acceleration('y'))
    z = abs(codey.get_acceleration('z'))
    
    # Determine the primary vector profile
    if z > x and z > y:
        return "drop"
    elif x > y:
        return "roll"
    else:
        return "toss"

# --- Main App Loop ---
codey.display.show("READY")

while True:
    # Start recording when A is pressed
    if codey.is_button_pressed('A') and not is_recording:
        is_recording = True
        codey.display.show("REC")
        codey.sound.play('happy')
        time.sleep(0.3) # Debounce button press

    # Stop recording when B is pressed
    if codey.is_button_pressed('B') and is_recording:
        is_recording = False
        codey.display.show("STOP")
        codey.sound.play('sad')
        print("--- Recording Stopped ---")
        print("Final Organized Data Multi-List:")
        print(final_impact_log)
        break # Exit loop to finalize script

    # Record acceleration and filter out insignificant impacts
    if is_recording:
        # Calculate overall total G-force acceleration magnitude
        acc_x = codey.get_acceleration('x')
        acc_y = codey.get_acceleration('y')
        acc_z = codey.get_accelerat('z')
        
        # Calculate raw peak scalar force magnitude
        total_intensity = (acc_x**2 + acc_y**2 + acc_z**2)**0.5
        
        # Filter: Only record if it crosses your 'significant' threshold criteria
        if total_intensity >= SIGNIFICANT_THRESHOLD:
            timestamp = get_current_timestamp()
            impact_type = classify_impact_type()
            
            # Construct entry package
            log_entry = [timestamp, round(total_intensity, 2), impact_type]
            final_impact_log.append(log_entry)

            
            # Flash the screen matrix briefly to confirm capture without halting execution
            codey.display.show("!!!")
            time.sleep(0.4)
            codey.display.show("REC")
            
    # Minimal polling delay to keep the processor responsive without choking memory cycles
    time.sleep(0.05)
