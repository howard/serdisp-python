from display import Display
from gatherer import Gatherer
from time import sleep

def sysinfo(name, port, interval=5):
    """Takes display name, port and update interval as arguments."""
    g = Gatherer()
    d = Display(name, port)
    try:
        while True:
            g.refresh()
            d.write("%s   %s %s %s" % (g.hostname, g.system, g.system_release, g.machine), 1, 1)
            d.draw_line((4, 12), (d.width-4, 12))
            d.write("Uptime: %s" % g.uptime.split()[0], 1, 15)
            sleep(interval)
    except KeyboardInterrupt:
        d.close()

def main():
    sysinfo('ALPHACOOL', 'USB:060C/04EB')

if __name__ == "__main__":
    main()