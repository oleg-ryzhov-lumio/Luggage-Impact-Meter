import cyberpi
import time

# 1. Connect Codey directly to your local Wi-Fi network
cyberpi.wifi.connect("Your_WiFi_Name", "Your_WiFi_Password")

while not cyberpi.wifi.is_connected():
    time.sleep(0.5)

cyberpi.inform("Connected & Armed")

# Your unique Google Apps Script Web App URL (We get this in the steps below)
google_script_url = "YOUR_GOOGLE_APPS_SCRIPT_URL_HERE"

while True:
    x = cyberpi.get_acc('x')
    y = cyberpi.get_acc('y')
    z = cyberpi.get_acc('z')
    
    total_g = (x**2 + y**2 + z**2)**0.5
    
    # Threshold filtering
    if total_g > 2.5:
        event_type = "roll"
        if total_g > 5.0:
            event_type = "toss"
        if total_g > 7.5:
            event_type = "drop"
            
        current_time = f"{time.localtime()[3]:02d}:{time.localtime()[4]:02d}:{time.localtime()[5]:02d}"
        
        # 2. Fire the data directly to your Google Sheet over the internet
        request_url = f"{google_script_url}?time={current_time}&g={total_g:.2f}&type={event_type}"
        cyberpi.network.request_get(request_url)
        
        time.sleep(0.8)
