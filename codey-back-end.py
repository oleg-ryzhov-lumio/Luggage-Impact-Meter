import cyberpi
import time

cyberpi.inform("System Armed")

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
        
        payload = f"{current_time},{total_g:.2f},{event_type}\n"
        cyberpi.cloud_message.send(payload)
        
        time.sleep(0.8)
