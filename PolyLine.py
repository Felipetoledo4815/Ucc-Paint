

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk, GooCanvas

from ucc_marker import CG_Marker


class CG_PolyLine():
    def __init__(self,layer ,x , y, width = 2.0, color = 0xff0000ff):
        self.pts = GooCanvas.CanvasPoints.new(2)
        self.pts.set_point(0, x, y)
        self.pts.set_point(1, x, y)

        #self.width = 0

        self.line = GooCanvas.CanvasPolyline(
            parent = layer,
            points = self.pts,
            line_width = width,
            stroke_color_rgba = color)

        self.markers = [CG_Marker(layer, self.pts.get_point(0)[0], self.pts.get_point(0)[1], self.handler1),
                        CG_Marker(layer, self.pts.get_point(1)[0], self.pts.get_point(1)[1], self.handler2)]

    def handler1(self, x, y):
        dx = x - self.pts.get_point(0)[0]
        dy = y - self.pts.get_point(0)[1]

        self.pts.set_point(1, self.pts.get_point(1)[0] + dx, self.pts.get_point(1)[1] + dy)
        self.pts.set_point(0, x, y)

        self.line.set_property("points", self.pts)
        self.markers[1].goto_x_y(self.pts.get_point(1)[0],
                                 self.pts.get_point(1)[1], False)

    def handler2(self, x, y):
        if x > 0:
            self.pts.set_point(1, x, self.pts.get_point(1)[1])
            self.line.set_property("points", self.pts)
        if y > 0:
            self.pts.set_point(1, self.pts.get_point(1)[0], y)
            self.line.set_property("points", self.pts)






class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.set_size_request(400, 400)

        canvas = GooCanvas.Canvas()
        cvroot = canvas.get_root_item()

        r = CG_PolyLine(cvroot, 100, 140)

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