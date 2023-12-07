

import time
import network
import uasyncio as asyncio
from machine import Pin, PWM



#i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)

pin_Back= Pin(14, Pin.OUT, value=0) #Motor # gibt steigendes signal aus  
pin_GO= Pin(15, Pin.OUT, value=0)# Motor # # gibt steigendes signal aus  

# Display SDA pin 1
# Display SCL pin 2

#lcd = I2cLcd(i2c, 0x3f, 2, 16)


servo_pin= Pin(0, Pin.OUT, value=0)# Servo 	# Über Periodendauer gesteuert 



# Name und Password eingeben 
#ssid = 'WLAN-L9RBTK'
#password = '5477729214812161'
ssid ='TP-Link_BEA3'
password ='53252126'

check_interval_sec = 0.25

wlan = network.WLAN(network.STA_IF)


# html code für die webseite
html = """<!DOCTYPE html><html>
<head><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
</head>
<body><center><h1>Car Controller</h1></center><br><br>
<form><center>
<center> <button class="button" name="car" value="GO" type="submit">GO</button>
<br><br>
<button class="button" name="car" value="LL" type="submit">SL</button>
<button class="button" name="car" value="L" type="submit">L</button>
<button class="button" name="car" value="STOP" type="submit">STOP</button>
<button class="button" name="car" value="R" type="submit">R</button>
<button class="button" name="car" value="SR" type="submit">SR</button>
<br><br>
<center> <button class="button" name="car" value="BACK" type="submit">BACK</center>
</center></form>
<br><br>
<br><br>
<p>Letzter Befehl war %s<p></body></html>
"""


def control_car(cmd): # Führt dei Befehle aus 
    if cmd == 'stop':
        # Motor aus
        pin_GO.value(0)
        pin_Back.value(0)
        
    if cmd == 'go':
        # langsamme Steigerung, sonst ist geht der Motor kaput
        pin_Back.value(0)
        time.sleep(1)
        i =0
        while i < 1:
              print(i)
              pin_GO.value(i)
              i += 0.02
              time.sleep(0.05)

        pin_GO.value(1)
        
        
    
    if cmd == 'back':
        
         # langsamme Steigerung, sonst ist geht der Motor kaput 
        pin_GO.value(0)
        time.sleep(1)
        j=0
        while j < 1:
              print(j)
              pin_Back.value(j)
              j += 0.02
              time.sleep(0.05)
              

        pin_Back.value(1)
        
       
       
    if cmd == 'richtung_1':
        print("Richtung")
    
        pwm = PWM(Pin(servo_pin))
        pwm.freq(50)
        
        pwm.duty_ns(500000)
        
    if cmd == 'richtung_2':
        print("Richtung")
    
        pwm = PWM(Pin(servo_pin))
        pwm.freq(50)
        
        pwm.duty_ns(1250000)
        
    if cmd == 'richtung_3':
        print("Richtung")
    
        pwm = PWM(Pin(servo_pin))
        pwm.freq(50)
        
        pwm.duty_ns(1750000)
       
        
    if cmd == 'richtung_4':
        print("Richtung")
    
        pwm = PWM(Pin(servo_pin))
        pwm.freq(50)
        
        pwm.duty_ns(2000000)
        
        
    if cmd == 'richtung_5':
        print("Richtung")
    
        pwm = PWM(Pin(servo_pin))
        pwm.freq(50)
        
       
        pwm.duty_ns(1500000)
    
        
async def connect_to_wifi():
    wlan.active(True)
    wlan.config(pm = 0xa11140) 
    wlan.connect(ssid, password)

    # Wait connect or fail
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    # Für connection error
    if wlan.status() != 3:
        
        raise RuntimeError('WiFi connection failed')
    else:
        
        print('connected')
        status = wlan.ifconfig()
        
        #lcd.putstr("ip" + "\n" + "***.***.***.***")
            
        print('ip = ' + status[0])
        

        
        # LCD dysplay 

async def serve_client(reader, writer):
    print("Client connected")
    #lcd.clear()
    request_line = await reader.readline()
    print("Request:", request_line)
    
    while await reader.readline() != b"\r\n":
        pass
    
    # Befehle finden aus request line
    request = str(request_line)
    cmd_go = request.find('car=GO')
    cmd_back = request.find('car=BACK')
    cmd_stop = request.find('car=STOP')
    cmd_sl = request.find('car=SL')
    cmd_l = request.find('car=L')
    cmd_sr = request.find('car=SR')
    cmd_r = request.find('car=R')
    print ('car=GO => ' + str(cmd_go)) # Zeigt ob gefunden (-1 ist nicht gefunden)
    print ('car=BACK => ' + str(cmd_back))
    print ('car=STOP => ' + str(cmd_stop))
    print ('car=SL => ' + str(cmd_sl))
    print ('car=L => ' + str(cmd_l))
    print ('car=SR => ' + str(cmd_sr))
    print ('car=R => ' + str(cmd_r))

    stateis = "" # letzter Befehl
    
    # Führt Befehl aus wenn gefunden (Gefunden hat index 8 in request line)
    if cmd_stop == 8:
        stateis = "Car: STOP"
        print(stateis)
        control_car('richtung_5')
        control_car('stop')
        
    elif cmd_go == 8:
        stateis = "Car: GO"
        print(stateis)
        response = html % stateis
        control_car('richtung_5')
        control_car('go')
        
    elif cmd_back == 8:
        stateis = "Car: BACK"
        print(stateis)
        control_car('richtung_5')
    
        response = html % stateis
        control_car('back')
    elif cmd_sl == 8:
        stateis = "Car: sl"
        print(stateis)
         #18° nach links
        control_car('richtung_1')
    elif cmd_l == 8:
        stateis = "Car: l"
        print(stateis)
        #9° nach links
        control_car('richtung_2')
    elif cmd_sr == 8:
        stateis = "Car: sr"
        print(stateis)
        #9° nach rechts
        control_car('richtung_4')
    elif cmd_r == 8:
        stateis = "Car: r"
        print(stateis)
        #18° nach rechts
        control_car('richtung_3')
    
    response = html % stateis
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)

    await writer.drain()
    await writer.wait_closed()


async def main():
    print('Connecting to WiFi...')
    asyncio.create_task(connect_to_wifi())

    print('Setting up webserver...')
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))

    while True:
        await asyncio.sleep(check_interval_sec)


try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()

