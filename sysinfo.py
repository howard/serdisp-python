from display import DisplayClient
from gatherer import Gatherer
from signal import signal, SIGUSR1
from time import sleep,strftime



def sysinfo(interval=5, host='localhost', port=35367):
    """Takes display name, port and update interval as arguments."""
    g = Gatherer()
    d = DisplayClient(host, port)
    
    def backlight_switch(signum, frame):
        d.backlight()
    
    date = strftime("Date: %a %b %d, %Y   ")
    d.write(1,1,string="%s   %s %s %s" % (g.hostname, g.system, g.system_release, g.machine))
    d.write(1,26,string=date)
    d.write(1,15,string="Uptime: ")
    d.write(1,37,string="Time: ")
    d.write(1,48,string="Load: ")
    
    try:
        while True:
            signal(SIGUSR1, backlight_switch)
            g.refresh()
            if date != strftime("Date: %a %b %d, %Y   "):
                date = strftime("Date: %a %b %d, %Y   ")
                d.write(1,26,string=date)
            d.write(51,15,string="%s   " % ' '.join(g.uptime.split('up')[1].split('user')[0].split()[:-1])[:-1])
            d.write(35,37,string=strftime("%H:%M"))
            d.write(35,48,string=g.uptime.split('average:')[-1].strip())
            sleep(interval)
    except KeyboardInterrupt:
        d.close()

def main():
    sysinfo(10)

if __name__ == "__main__":
    main()