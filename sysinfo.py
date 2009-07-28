from display import DisplayClient
from gatherer import Gatherer
from time import sleep,strftime

def sysinfo(interval=5, host='localhost', port=35367):
    """Takes display name, port and update interval as arguments."""
    g = Gatherer()
    d = DisplayClient(host, port)
    date = strftime("Date: %a %b %d, %Y")
    d.write(1,1,string="%s   %s %s %s" % (g.hostname, g.system, g.system_release, g.machine))
    d.draw_line((4, 12), (d.width-4, 12))
    d.write(1,26,string=date)
    d.write(1,15,string="Uptime: ")
    d.write(1,37,string="Time: ")
    d.write(1,48,string="Load: ")
    try:
        while True:
            g.refresh()
            if date != strftime("Date: %a %b %d, %Y"):
                date = strftime("Date: %a %b %d, %Y")
                d.write(1,26,string=date)
            d.write(51,15,string=g.uptime.split()[2])
            d.write(35,37,string=strftime("%H:%M"))
            d.write(35,48,string=' '.join(g.uptime.split()[8:]))
            sleep(interval)
    except KeyboardInterrupt:
        d.close()

def main():
    sysinfo(15)

if __name__ == "__main__":
    main()