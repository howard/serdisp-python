import socket

class DisplayClient:
    def __init__(self, host='localhost', port=35367):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.width = int(self.send('width'))
        self.height = int(self.send('height'))
        self.colors = int(self.send('colors'))
        self.coolor_depth = int(self.send('color_depth'))
    
    def send(self, request):
        self.socket.send("%s\r\n" % request)
        response = self.socket.recv(1024).split('\n')
        return '\n'.join(response[:-2])
    
    def close(self):
        self.socket.send('clear')
        self.backlight(0)
        self.socket.close()
    
    def backlight(self, state=2):
        """Puts the backlight in the given state. Use 0, 1, or 2 for toggle (default)."""
        if not state in (0, 1, 2):
            raise "Invalid bacaklight state: it must be either 0, 1 or 2 for toggle."
        else:
            self.send('backlight %d' % state)

    def invert(self):
        """Inverts the colors."""
        self.send('invert')

    def rotate(self, n=180):
        """Rotates the display by n degrees."""
        self.send('rotate %d' % n)

    def see(self, x, y):
        """Inspects the color of a pixel at the position (x/y)."""
        return self.send('see %d %d' % (x, y))

    def draw(self, x, y, color=0xFF000000, update=True):
        """
        Changegs a pixel's color to the third argument. Default is 0xFF000000.
        The last argument decides whether the display is updated after setting
        the pixel or not. Default is True.
        """
        command = 'draw %d %d 0x%X %s' % (x, y, color, update)
        self.send(command)

    def draw_pattern(self, x_offset, y_offset, pattern="", update=True):
        """
        Draws a b/w pattern, which has to be defined like this:
        --++--++
        ++--++--
        ...wereas - is white and + is black. It's important that each line has the
        same length.
        """
        lines = pattern.split('\n')
        for line in lines:
            self.send('draw_pattern %d %d %s %s' % (x_offset, y_offset, line, False))
        if update:
            self.update()

    def erase(self, x, y, update=True):
        """Erases a given pixel."""
        self.send('erase %d %d %s' % (x, y, update))

    def write(self, x=0, y=0, update=True, string=""):
        """
        Writes a string on screen, starting at a given position. Currently,
        only b/w text is available, and the font size is bound to be 10px.
        """
        self.send('write %d %d %s %s' % (x, y, update, string))

    def image(self, path):
        """Draws an image on sceen."""
        pass

    def clear(self):
        """Clears whole display."""
        self.send('clear')

    def update(self):
        self.send('update')

    def rewrite(self):
        self.send('rewrite')

    def blink(self, method, n=1, t=1):
        """
        Blinks display content in the way given in method, n times in
        intervals of t seconds. Methods: backlight, reverse.
        """
        if not method in ('backlight', 'reverse'):
            raise "Invalid blink method: it must be either 'backlight' or 'reverse'."
        else:
            self.send('blink %s %d %d' % (method, n, t))

    def test(self):
        self.send('test')