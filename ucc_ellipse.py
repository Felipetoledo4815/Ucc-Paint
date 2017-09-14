import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk, GooCanvas

from ucc_marker import CG_Marker


class CG_Ellipse():
    """ Creacion de una elipse
    """
    def __init__(self, layer, x, y, rx = 1, ry = 1, stroke_color = 0x000000ff, line_width = 1.0,
                                    fill_color = 0x0000ffc0):
        self.cx = x
        self.cy = y
        self.px = x
        self.py = y

        self.ellipse = GooCanvas.CanvasEllipse(
                    parent = layer,
                    center_x = x,
                    center_y = y,
                    radius_x = rx,
                    radius_y = ry,
                    stroke_color_rgba = stroke_color,
                    line_width = line_width,
                    fill_color_rgba = fill_color)

        self.markers = [CG_Marker(layer, x, y, self.handler1),
                        CG_Marker(layer, x, y, self.handler2)]


    def handler1(self, x, y):
        """ Este handler es asignado al marcador de la esquina superior izq.
            Movera la figura entera
        """
        dx = x - self.cx
        dy = y - self.cy

        self.cx = x
        self.cy = y
        self.px = self.px + dx
        self.py = self.py + dy

        self.ellipse.set_property("center_x", x)
        self.ellipse.set_property("center_y", y)
        self.markers[1].goto_x_y(self.px,
                                 self.py, False)


    def handler2(self, x, y):
        """ Este handler es asignado al marcador de la esquina inferior derecha.
            Cambiara el tamano de la figura
        """
        dx = x - self.cx
        dy = y - self.cy

        self.px = self.cx + dx
        self.py = self.cy + dy

        if dx > 0:
            self.ellipse.set_property("radius_x", dx)
        if dy > 0:
            self.ellipse.set_property("radius_y", dy)


class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.set_size_request(400, 400)

        canvas = GooCanvas.Canvas()
        cvroot = canvas.get_root_item()

        r = CG_Ellipse(cvroot, 100, 100, 1, 1)

        self.add(canvas)
        self.show_all()

    def run(self):
        Gtk.main()


def main(args):
    mainwdw = MainWindow()
    mainwdw.run()

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
