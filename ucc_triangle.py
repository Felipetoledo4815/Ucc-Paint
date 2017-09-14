#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk, GooCanvas
from ucc_marker import CG_Marker



class CG_Triangle():
    def __init__(self, layer, x, y, line_color = 0x000000ff, width = 1.0,
                                    fill_color = 0x0000ffc0):

        # self.pts = GooCanvas.CanvasPoints.new(3)
        # self.pts.set_point(0, x, y)
        # self.pts.set_point(1, x, y)
        # self.pts.set_point(2, x, y)

        self.xi = x
        self.yi = y
        self.xc = x
        self.yc = y
        self.xf = x
        self.yf = y
        self.string = "data"

        self.conversor()

        self.triangle = GooCanvas.CanvasPath(
            parent = layer,
            data = self.string,
            line_width = width,
            stroke_color_rgba = line_color,
            fill_color_rgba = fill_color
            )

        self.markers = [CG_Marker(layer, x, y, self.handler1),
                        CG_Marker(layer, x, y, self.handler2),
                        CG_Marker(layer, x, y, self.handler3)]

        # self.markers = [CG_Marker(layer, self.pts.get_point(0)[0], self.pts.get_point(0)[1], self.handler1),
        #                 CG_Marker(layer, self.pts.get_point(1)[0], self.pts.get_point(1)[1], self.handler2),
        #                 CG_Marker(layer, self.pts.get_point(2)[0], self.pts.get_point(2)[1], self.handler2)]


    def conversor(self):            #"M20,100 L50,50 L50,50 Z"
        self.string = "M%d,%d L%d,%d L%d,%d Z"%(self.xi, self.yi,
                                                self.xf, self.yf,
                                                self.xc, self.yc)


    def handler1(self, x, y):
        dx = x - self.xi
        dy = y - self.yi

        self.xi = x
        self.yi = y
        self.xc = self.xc + dx
        self.yc = self.yc + dy
        self.xf = self.xf + dx
        self.yf = self.yf + dy

        self.markers[1].goto_x_y(self.xc, self.yc, False)
        self.markers[2].goto_x_y(self.xf, self.yf, False)

        self.conversor()
        self.triangle.set_property("data", self.string)

    def handler2(self, x, y):
        self.xc = x
        self.yc = y

        self.conversor()
        self.triangle.set_property("data", self.string)

    def handler3(self, x, y):
        self.xf = x
        self.yf = y

        self.conversor()
        self.triangle.set_property("data", self.string)


class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.set_size_request(400, 400)

        canvas = GooCanvas.Canvas()
        cvroot = canvas.get_root_item()

        r = CG_Triangle(cvroot, 100, 140)

        self.add(canvas)
        self.show_all()

    def run(self):
        Gtk.main()


    def test_handler(self, x, y):
        print("El handler recibio: X=%d, Y=%d" % (x, y))



def main(args):
    mainwdw = MainWindow()
    mainwdw.run()

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))