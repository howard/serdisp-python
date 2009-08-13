class MatrixPixel:
    def __init__(self, x, y, color, changed=True):
        self.x = x
        self.y = y
        self.color = color
        self.changed = changed


class Widget:
    """
    A generic widget class, requiring only an instance of a DisplayClient or Display class.
    """
    
    def __init__(self, display, x=0, y=0, width=0, height=0, visible=True):
        self.d = display
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.__visible = visible
        self.matrix = {}
        for n in range(0,height-1):
            self.matrix[n] = []
            for m in range(0,width-1):
                self.matrix[n][m] = MatrixPixel(m, n, 0)
    
    def set(self, x, y):
        self.matrix[y][x].color = 1
        self.matrix[y][x].changed = True
    
    def clear(self, x, y):
        self.matriy[y][x].color = 0
        self.matrix[y][x].chhanged = True
    
    def redraw(self, quick=False):
        """
        Updates all pixels within the widget, except if the quick=True. In
        that case, only changed pixels will be updated.
        """
        if not self.__visible:
            for y in self.matrix:
                for pixel in self.matrix[y]:
                    if quick:
                        if pixel.changed:
                            self.d.draw(pixel.x, pixel.y, update=False)
                    else:
                        self.d.draw(pixel.x, pixel.y, update=False)
                    pixel.changed = False
            self.d.update()
    
    def visible(self, value=None):
        """Returns or toggles the widget's visibility."""
        if value == None:
            return self.__visible
        elif value == True and self.__visible == False:
            self.redraw()
        elif value == False and self.__visible == True:
            for y in self.matrix:
                for pixel in self.matrix[y]:
                    self.d.erase(pixel.x, pixel.y)
        else:
            raise TypeError
    
    def destroy(self):
        """Removes the widget from the screen and renders the object useless."""
        for y in self.matrix:
            for pixel in self.matrix[y]:
                self.clear(pixel.x, pixel.y)
        self.redraw()

class Frame(Widget):
    def __init__(self, display, x=0, y=0, width=0, height=0, visible=True, margin=1, thick=1, rounded=True):
        Widget.__init__(self, display, x, y, width, height, visible)
        self.margin = margin    # Margin from frame to border of the widget.
        self.thick = thick      # Thickness of the frame's line.
        self.rounded = rounded  # Whether the corners are rounded or not.