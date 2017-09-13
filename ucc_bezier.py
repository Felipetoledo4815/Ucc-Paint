#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk, GooCanvas

from ucc_marker import CG_Marker

class CG_Bezier():
    def __init__(self, layer, x, y, width = 2.0, color = 0xff0000ff):
        self.string = "data"

        self.xi = x
        self.yi = y
        self.xf = x
        self.yf = y
        self.cx = x
        self.cy = y

        self.conversor()

        self.bezier = GooCanvas.CanvasPath (
                    parent = layer,
                    data = self.string,
                    stroke_color_rgba = color,
                    line_width = width)

        self.markers = [CG_Marker(layer, x, y, self.handler1),
                        CG_Marker(layer, x, y, self.handler2),
                        CG_Marker(layer, x, y, self.handler3)]


    def handler1(self, x, y):
        """ Este handler es asignado al marcador de la esquina superior izq.
            Movera la figura entera
        """
        dx = x - self.xi
        dy = y - self.yi

        self.xi = x
        self.yi = y
        self.xf = self.xf + dx
        self.yf = self.yf + dy
        self.cx = self.cx + dx
        self.cy = self.cy + dy

        self.markers[1].goto_x_y(self.cx, self.cy, False)
        self.markers[2].goto_x_y(self.xf, self.yf, False)

        self.conversor()
        self.bezier.set_property("data", self.string)


    def handler2(self, x, y):
        """ Este handler es asignado al marcador de control."""
        self.cx = x
        self.cy = y

        self.conversor()
        self.bezier.set_property("data", self.string)


    def handler3(self, x, y):
        """ Este handler es asignado al marcador de la esquina inferior derecha.
            Cambiara el tamano de la figura
        """
        self.xf = x
        self.yf = y

        self.conversor()
        self.bezier.set_property("data", self.string)


    def conversor(self):            #"M20,100 C50,50 50,50 100,100"
        self.string = "M%d,%d C%d,%d %d,%d %d,%d"%(self.xi, self.yi,
                                                   self.cx, self.cy,
                                                   self.cx, self.cy,
                                                   self.xf, self.yf)


class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.set_size_request(400, 400)

        canvas = GooCanvas.Canvas()
        cvroot = canvas.get_root_item()

        r = CG_Bezier(cvroot, 100, 100)

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
