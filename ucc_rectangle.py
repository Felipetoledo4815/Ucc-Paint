#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  ucc_rectangle.py
#
#  Copyright 2017 John Coppens <john@jcoppens.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk, GooCanvas

from ucc_marker import CG_Marker


class CG_Rectangle():
    """ Creacion de un rectangulo. Parametros del constructor:
            layer:          Capa ('CanvasGroup') en la cual dibujar
            x, y:           Punto inicial del rectangulo
            stroke_color:   Color del borde en formato RGBA
            line_width:     Ancho de la linea del borde en pixeles
            fill_color:     Color de relleno en format RGBA
    """
    def __init__(self, layer, x, y, stroke_color = 0x000000ff, line_width = 1.0,
                                    fill_color = 0x0000ffc0):
        self.rect = GooCanvas.CanvasRect(
                    parent = layer,
                    x = x,
                    y = y,
                    width = 0, height = 0,
                    stroke_color_rgba = stroke_color,
                    line_width = line_width,
                    fill_color_rgba = fill_color)

        self.markers = [CG_Marker(layer, x, y, self.handler1),
                        CG_Marker(layer, x, y, self.handler2)]


    def handler1(self, x, y):
        """ Este handler es asignado al marcador de la esquina superior izq.
            Movera la figura entera
        """
        self.rect.set_property("x", x)
        self.rect.set_property("y", y)
        self.markers[1].goto_x_y(x + self.rect.get_property("width"),
                                 y + self.rect.get_property("height"), False)


    def handler2(self, x, y):
        """ Este handler es asignado al marcador de la esquina inferior derecha.
            Cambiara el tamano de la figura
        """
        new_width  = x - self.rect.get_property("x")
        new_height = y - self.rect.get_property("y")
        if new_width > 0:
            self.rect.set_property("width", new_width)
        if new_height > 0:
            self.rect.set_property("height", new_height)


class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())

        canvas = GooCanvas.Canvas()
        cvroot = canvas.get_root_item()

        r = CG_Rectangle(cvroot, 100, 140)

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
