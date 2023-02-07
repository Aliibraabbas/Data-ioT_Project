import network
import socket
from machine import Pin
from machine import Pin, ADC 
from machine import Pin, PWM 
import time

adc = ADC(Pin(26, mode=Pin.IN))

led = PWM(Pin(13,mode=Pin.OUT)) 
led.freq(1_000) 
led.duty_u16(13000)

led2 = PWM(Pin(9,mode=Pin.OUT)) 
led2.freq(1_000) 
led2.duty_u16(13000)

led3 = PWM(Pin(5,mode=Pin.OUT)) 
led3.freq(1_000) 
led3.duty_u16(13000)


# led = Pin(13, Pin.OUT)
# led2 = Pin(9, Pin.OUT)
# led3 = Pin(5, Pin.OUT)
ledState = 'LED State Unknown'
led2State = 'LED State Unknown'
led3State = 'LED State Unknown'

button = Pin(17, Pin.IN, Pin.PULL_UP)

ssid = 'A.B'
password = 'Aliabbas000007'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

html = """<!DOCTYPE html><html>
<head><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
            <style>
                html {
                    font-family: Helvetica;
                    display: inline-block;
                    margin: 0px auto;
                    text-align: center;
                }
                h1 {
                    color: #0F3376;
                    padding: 2vh;
                }

                p{
                    display: inline-block ;
                    font-weight: bold;
                    font-size: 12px;
                }
                .Button {           
                    border-radius: 31px;           
                    display: inline-block;
                    cursor: pointer;
                    color: #ffffff;
                    font-family: Arial;
                    font-size: 17px;
                    font-weight: bold;
                    font-style: italic;
                    padding: 17px 19px;
                    text-decoration: none;           
                }
                .ButtonR {
                    background-color: #ec4949;            
                    border: 6px solid #991f1f;           
                    text-shadow: 0px 2px 2px #471e1e;
                }
                .ButtonR:hover {
                    background-color: #f51616;
                }

                .Button:active {
                    position: relative;
                    top: 1px;
                }
                .ButtonG {
                    background-color: #49ec56;            
                    border: 6px solid #23991f;          
                    text-shadow: 0px 2px 2px #1e4723;
                }
                .ButtonG:hover {
                    background-color: #29f516;
                }  
                .ButtonB {
                    background-color: #4974ec;           
                    border: 6px solid #1f3599;         
                    text-shadow: 0px 2px 2px #1e2447;
                }
                .ButtonB:hover {
                    background-color: #165df5;
                }
                .buttonRed{
                    background-color: #ec4949;            
                    border: 1px solid #991f1f; 
                    border-radius: 15px; 
                     padding: 10px 12px;
                }
            
            </style>
</head>
<body><center><h1>Control Panel</h1></center><br><br>
<form><center>
<center> <button class="ButtonB Button" name="led" value="on" type="submit">Blue light ON</button>
<br><br>
<center> <button class="buttonRed" name="led" value="off" type="submit">Blue light OFF</button>
<br><br>
<center> <button class="ButtonR Button" name="led2" value="on" type="submit">Red light ON</button>
<br><br>
<center> <button class="buttonRed" name="led2" value="off" type="submit">Red light OFF</button>
<br><br>
<center> <button class="ButtonG Button" name="led3" value="on" type="submit">Green light ON</button>
<br><br>
<center> <button class="buttonRed" name="led3" value="off" type="submit">Green light OFF</button>
</form>
<br><br>
<br><br>
<p>%s<p>
</body>
</html>
"""



max_wait = 10

while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)


if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )


# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)



while True:

    try:          

        val = adc.read_u16()
        val = val * (3.3/65535)
        print(round(val, 2), "V")
        time.sleep_ms(100) 


        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print("request:")
        print(request)
        request = str(request)
        led_on = request.find('led=on')
        led_off = request.find('led=off')
        led2_on = request.find('led2=on')
        led2_off = request.find('led2=off')
        led3_on = request.find('led3=on')
        led3_off = request.find('led3=off')
        
        print( 'led on = ' + str(led_on))
        print( 'led off = ' + str(led_off))
        print( 'led2 on = ' + str(led2_on))
        print( 'led2 off = ' + str(led2_off))
        print( 'led3 on = ' + str(led3_on))
        print( 'led3 off = ' + str(led3_off))
        
        if led_on == 8:
            print("led on")
            led.duty_u16(13000)
        
        if led2_on == 8:
            print("led on")
            led2.duty_u16(13000)

        
        if led3_on == 8:
            print("led on")
            led3.duty_u16(13000)
        
        if led_off == 8:
            print("led off")
            led.duty_u16(0)

        if led2_off == 8:
            print("led2 off")
            led2.duty_u16(0)

        if led3_off == 8:
            print("led3 off")
            led3.duty_u16(0)
        
        ledState = "Blue light is OFF" if led.duty_u16() == 0 else "Blue light is ON" 
        led2State = "Red light is OFF" if led.duty_u16() == 0 else "Red light is ON" 
        led3State = "Green light is OFF" if led.duty_u16() == 0 else "Green light is ON" 

        
        
        stateis = ledState + " and " + led2State  + "and" + led3State
        response = html % stateis
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    
 
        
    except OSError as e:
        cl.close()
        print('connection closed')