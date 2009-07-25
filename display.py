#!/usr/bin/env python

from ctypes import *


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
    
    def draw(self, x, y, color=0xFF000000):
        """Changegs a pixel's color to the third argument. Default is 0xFF000000."""
        self.lib.serdisp_setcolour(self.disp, x, y, color)
        self.update()
    
    def erase(self, x, y):
        self.lib.serdisp_setcolour(self.disp, x, y, 0xFFFFFFFF)
        self.update()
    
    def write(self, string):
        """Writes a string on screen."""
        pass
    
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
        for x in range(20, 40):
            for y in range(20, 40):
                self.draw(x, y)
    

def main():
    d = Display('ALPHACOOL', 'USB:060C/04EB')
    d.test()

if __name__ == '__main__':
    main()