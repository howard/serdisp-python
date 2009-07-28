#!/usr/bin/env python

from ctypes import *
import characters as chrs
import subprocess


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
    
    def draw_line(self, (start_x, start_y), (end_x, end_y), kind='solid', color='0xFF000000', update=True):
        """
        Draws a horizontal or vertical line on screen.
        Arguments: (start_x, start_y), (end_x, end_y), kind='solid', color='0xFF000000', update=True
        Available kinds: solid, dotted, dashed
        """
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                if kind == 'solid':
                    self.draw(x, y, color, False)
                elif kind == 'dotted':
                    if not (x-start_x % 2 or y-start_y % 2):
                        self.draw(x, y, color, False)
                elif kind == 'dashed':
                    if not (x-start_x % 4 or y-start_y % 4):
                        self.draw(x, y, color, False)
                else:
                    raise "Invalid line type: It must be either solid, dotted, or dashed."
        self.update()
    
    def draw_pattern(self, x_offset, y_offset, pattern="", update=True):
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
        """Erases a given pixel."""
        self.draw(x, y, 0xFFFFFFFF, update)
    
    def write(self, x=0, y=0, update=True, string=""):
        """
        Writes a string on screen, starting at a given position. Currently,
        only b/w text is available, and the font size is bound to be 10px.
        """
        def get_p(what):
            """Gets a pattern specified in the first argument from the characters file."""
            try:
                return getattr(chrs, what)
            except AttributeError:
                return getattr(chrs, 'NONE')
        
        special_chrs = {
            ' ':get_p('SPACE'),
            '_':get_p('UNDERSCORE'),
            '-':get_p('DASH'),
            '.':get_p('DOT'),
            ':':get_p('COLON'),
            ',':get_p('COMMA'),
            ';':get_p('SEMICOLON'),
            '!':get_p('EXCL_MARK'),
            '?':get_p('QUES_MARK'),
            '&':get_p('AMPERSAND'),
            '#':get_p('HASH'),
            '"':get_p('QUOT_MARK'),
            '$':get_p('DOLLAR'),
            '%':get_p('PERCENT'),
            '\'':get_p('APOSTROPHE'),
            '(':get_p('PARENTHESIS1'),
            ')':get_p('PARENTHESIS2'),
            '*':get_p('ASTERISK'),
            '+':get_p('PLUS'),
            '/':get_p('SLASH'),
            '\\':get_p('BACKSLASH'),
            '<':get_p('SMALLER'),
            '>':get_p('BIGGER'),
            '=':get_p('EQUAL'),
            '[':get_p('SQUAR_BRACKET1'),
            ']':get_p('SQUAR_BRACKET2'),
            '@':get_p('AT'),
            '^':get_p('CARRET'),
            '`':get_p('GRAVE'),
            '|':get_p('PIPE'),
            '~':get_p('TILDE'),
            '{':get_p('CURL_BRACKET1'),
            '}':get_p('CURL_BRACKET2'),
            '0':get_p('ZERO'),
            '1':get_p('ONE'),
            '2':get_p('TWO'),
            '3':get_p('THREE'),
            '4':get_p('FOUR'),
            '5':get_p('FIVE'),
            '6':get_p('SIX'),
            '7':get_p('SEVEN'),
            '8':get_p('EIGHT'),
            '9':get_p('NINE')
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
                    if x_offset > self.width-15:
                        x_offset = x
                        y_offset += 10
                    else:
                        x_offset += char_width
                except AttributeError:
                    raise "Sorry, this character is not available at this time."
        if update:
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
        self.write(0,0,True," AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPp\nQqRrSsTtUuVvWwXxYyZz0123456789\n\
_-.:,;!?&#\"$%'()*+/\\<>=[]@^`|~{}")
        self.draw_pattern(self.width/2-73, self.height/2-23, chrs.AGF_HUGE)


def get_output(command, stdout = True, stderr = False):
    """
    Runs a program specified in the first argument and returns its output
    as a string. Code borrowed from P1tr.
    """
    if (stdout or stderr) and not (stdout and stderr):
        pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        if stdout:
        	return pipe.stdout.read()
        else:
        	return pipe.stderr.read()
    elif stdout and stderr:
    	return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT).stdout().read()
    else:
        try:
            return bool(subprocess.Popen(command))
        except OSError:
            return "Output unavailable."

