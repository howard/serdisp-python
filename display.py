#!/usr/bin/env python

from ctypes import *
import characters as chrs
#import SocketServer


class Display:
    def __init__(self, driver, port, options="", lib_path="/usr/local/lib/libserdisp.so.1"):
        self.lib = CDLL(lib_path)
        self.driver = driver
        # The following is ugly and C-ish
        self.disp_conn = self.lib.SDCONN_open(port)
        self.disp = self.lib.serdisp_init(self.disp_conn, self.driver, options) # display descriptor
        self.width = self.lib.serdisp_getwidth(self.disp)
        self.height = self.lib.serdisp_getheight(self.disp)
        self.colors = self.lib.serdisp_getcolours(self.disp)
        self.color_depth = self.lib.serdisp_getdepth(self.disp)
        #self.pixel_aspect_ratio = self.lib.serdisp_getaspect(self.disp)
    
    def close(self):
        self.lib.serdisp_quit(self.disp)
        #self.lib.serdisp_close(self.disp)
        #self.lib.SDCONN_close(self.disp_conn)
    
    def reset(self, full=False):
        if full:
            self.lib.serdisp_fullreset(self.disp)
        else:
            self.lib.serdisp_reset(self.disp)
    
    def clear_buffer(self):
        self.lib.serdisp_clearbuffer(self.disp)
    
    def backlight(self, state=2):
        """Puts the backlight in the given state. Use 0, 1, or 2 for toggle (default)."""
        if not state in (0, 1, 2):
            raise "Invalid bacaklight state: it must be either 0, 1 or 2 for toggle."
        else:
            self.lib.serdisp_setoption(self.disp, 'BACKLIGHT', state)
    
    def invert(self):
        """Inverts the colors."""
        self.lib.serdisp_setoption(self.disp, 'INVERT', 2)
    
    def rotate(self, n):
        """Rotates the display by n degrees."""
        self.lib.serdisp_setoption(self.disp, 'ROTATE', n)
    
    def see(self, x, y):
        """Inspects the color of a pixel at the position (x/y)."""
        return self.lib.serdisp_getcolour(self.disp, x, y)
    
    def draw(self, x, y, color=0xFF000000, update=True):
        """
        Changegs a pixel's color to the third argument. Default is 0xFF000000.
        The last argument decides whether the display is updated after setting
        the pixel or not. Default is True.
        """
        self.lib.serdisp_setcolour(self.disp, x, y, color)
        if update:
            self.update()
    
    def draw_pattern(self, x_offset, y_offset, pattern, update=True):
        """
        Draws a b/w pattern, which has to be defined like this:
        --++--++
        ++--++--
        ...wereas - is white and + is black. It's important that each line has the
        same length.
        """
        lines = pattern.split('\n')
        width = len(lines[0])
        height = len(lines)
        for y in range(0, height):
            for x in range(0, width):
                try:
                    px = lines[y][x]
                    if px == '+':
                        color = 0xFF000000
                    else:
                        color = 0xFFFFFFFF
                    self.draw(x_offset+x, y_offset+y, color, False)
                except IndexError:
                    pass    # Ignore this one silently.
        if update:
            self.update()
    
    def erase(self, x, y, update=True):
        self.draw(x, y, 0xFFFFFFFF, update)
    
    def write(self, x=0, y=0, string=""):
        """
        Writes a string on screen, starting at a given position. Currently,
        only b/w text is available, and the font size is bound to be 10px.
        """
        special_chrs = {
            ' ':getattr(chrs, 'SPACE'),
            '_':getattr(chrs, 'UNDERSCORE'),
            '-':getattr(chrs, 'DASH'),
            '.':getattr(chrs, 'DOT'),
            ',':getattr(chrs, 'COMMA'),
            '!':getattr(chrs, 'EXCL_MARK'),
            '?':getattr(chrs, 'QUES_MARK'),
            '#':getattr(chrs, 'HASH')
        }
        x_offset = x
        y_offset = y
        for c in string:
            if c == '\n':
                x_offset = x
                y_offset += 10
            else:
                try:
                    if c in special_chrs.keys():
                        char = special_chrs[c]
                    else:
                        char = getattr(chrs, c)
                    self.draw_pattern(x_offset, y_offset, char, False)
                    char_width = len(char.split('\n')[0])
                    if x_offset > self.width+10:
                        x_offset = x
                        y_offset += 10
                    else:
                        x_offset += char_width
                except AttributeError:
                    raise "Sorry, this character is not available at this time."
        self.update()
    
    def image(self, path):
        """Draws an image on sceen."""
        pass
    
    def clear(self):
        """Clears whole display."""
        self.lib.serdisp_clear(self.disp)
    
    def update(self):
        self.lib.serdisp_update(self.disp)
    
    def rewrite(self):
        self.lib.serdisp_rewrite(self.disp)
    
    def blink(self, method, n=1, t=1):
        """
        Blinks display content in the way given in method, n times in
        intervals of t seconds. Methods: backlight, reverse.
        """
        if not method in ('backlight', 'reverse'):
            raise "Invalid blink method: it must be either 'backlight' or 'reverse'."
        else:
            self.lib.serdisp_blink(self.disp, method.upper(), n, t)
    
    def test(self):
        self.write(0, 0, "AaBbCcDd _-.,!?#")


"""class DisplayServerHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        while True:
            self.data = self.rfile.readline().strip().split()
            command = self.data[0].lower()
            params = self.data[1:]
            d = self.request.display
            if command == 'quit':
                break
            try:
                {
                'p': lambda: d.draw(params[0], params[1]),
                'clear': lambda: d.clear()
                }[command]()
                self.wfile.write("OK")
            except KeyError, TypeError:
                self.wfile.write("FAIL")
        


class DisplayServer(SocketServer.TCPServer):
    def __init__(self, display, (host, port), handler):
        SocketServer.TCPServer.__init__(self, (host, port), handler)
        self.display = display


def start_display_server(display, host='localhost', port=35367):
    server = DisplayServer(display, (host, port), DisplayServerHandler)
    server.serve_forever()
    return server"""
    

def main():
    display = Display('ALPHACOOL', 'USB:060C/04EB')
    #server = start_display_server(display)

if __name__ == '__main__':
    main()