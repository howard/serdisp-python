#!/usr/bin/env python

from libdisplay import *
import SocketServer

class DisplayServerHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        while True:
            self.data = self.rfile.readline().strip().split()
            command = self.data[0].lower()
            params = self.data[1:]
            d = self.server.display
            if command == 'quit':
                break
            try:
                # When talking to the Display object via socket, all possible
                # arguments must be given. Client-side modules can make this
                # more convenient by offering defaults again.
                output = {
                'driver': lambda: d.driver,
                'width': lambda: d.width,
                'height': lambda: d.height,
                'colors': lambda: d.colors,
                'color_depth': lambda: d.color_depth,
                'backlight': lambda: d.backlight(int(params[0])),
                'invert': lambda: d.invert(),
                'rotate': lambda: d.rotate(int(params[0])),
                'reset': lambda: d.reset(bool(params[0])),
                'see': lambda: d.see(int(params[0]), int(params[1])),
                'draw': lambda: d.draw(int(params[0]), int(params[1]), int(params[2]), bool(params[3])),
                'draw_pattern': lambda: d.draw_pattern(int(params[0]), int(params[1]), params[2], bool(params[3])),
                'erase': lambda: d.erase(int(params[0]), int(params[1]), int(params[2])),
                'write': lambda: d.write(int(params[0]), int(params[1]), bool(params[2]), (' '.join(params[3:]))),
                'clear': lambda: d.clear(),
                'test': lambda: d.test(),
                'update': lambda: d.update(),
                'rewrite': lambda: d.rewrite(),
                'blink': lambda: d.blink(params[0], int(params[1]), int(params[2]))
                }[command]()
                self.wfile.write("%s\nOK\n" % output)
            except IndexError, TypeError:
                self.wfile.write("FAIL\n")
        


class DisplayServer(SocketServer.TCPServer):
    def __init__(self, display, host='localhost', port=35367, handler=DisplayServerHandler):
        SocketServer.TCPServer.__init__(self, (host, port), handler)
        self.display = display


def main():
    display = Display('ALPHACOOL', 'USB:060C/04EB')
    server = DisplayServer(display)
    server.serve_forever()

if __name__ == '__main__':
    main()