import cyberpi
import time

# Connect directly to the local Wi-Fi network
cyberpi.wifi.connect("Lumio Students", "As this is a public repository, I will not share the password here, but it will be in the actual code")

while not cyberpi.wifi.is_connected():
    time.sleep(0.5)

cyberpi.inform("Connected & Armed")

while True:
    x = cyberpi.get_acc('x')
    y = cyberpi.get_acc('y')
    z = cyberpi.get_acc('z')
    
    total_g = (x**2 + y**2 + z**2)**0.5
    
    if total_g > 2.5:
        event_type = "roll"
        if total_g > 5.0:
            event_type = "toss"
        if total_g > 7.5:
            event_type = "drop"
            
        current_time = f"{time.localtime()[3]:02d}:{time.localtime()[4]:02d}:{time.localtime()[5]:02d}"
        
        # Trigger a direct web hook to send data to the cloud
        cyberpi.network.request_get(f"https://your-cloud-receiver.com/log?time={current_time}&g={total_g:.2f}&type={event_type}")
        
        time.sleep(0.8)
