#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  ucc_marker.py
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


MARKER_BORDER_COLOR = 0xff0000ff
MARKER_FILL_COLOR   = 0xff0000ff
MARKER_LINE_WIDTH   = 1.0
MARKER_SIZE         = 8

class CG_Marker():
    """ Clase define un marcador ('handle') que servira luego para mover o
        redimensionar objetos en el area de dibujo.
        El marcador es sensible al boton 1 para moverlo.
        Parametros para el constructor:
            layer:      Capa (o CanvasGroup) en la cual dibujar al marcador
            x, y:       Coordenadas del centro del marcador
            handler:    Una referencia a una routina que sera llamada cuando
                        el marcador cambia de posicion.
    """
    def __init__(self, layer, x, y, handler):
        super(CG_Marker, self).__init__()
        self.startx = self.starty = None
        self.handler = handler

        self.marker = GooCanvas.CanvasRect(         # Creacion del marcador
                    parent = layer,
                    width = MARKER_SIZE, height=MARKER_SIZE,
                    stroke_color_rgba = MARKER_BORDER_COLOR,
                    line_width = MARKER_LINE_WIDTH,
                    fill_color_rgba = MARKER_FILL_COLOR)
        self.goto_x_y(x, y, False)                  # Reubicar el marcador a x, y

        self.marker.connect("button-press-event", self.on_button_press)
        self.marker.connect("button-release-event", self.on_button_release)
        self.marker.connect("motion-notify-event", self.on_motion_notify)


    def on_button_press(self, src, tgt, event):
        """ Cuando se oprime el boton 1, sobre el marcador, este se centrara
            automaticamente (llamada a goto_x_y), y llamara al handler para
            comunicar esta corrección al 'dueno' del marcador.
        """
        if event.button.button == 1:
            self.goto_x_y(event.x, event.y)
            self.handler(self.startx, self.starty)


    def on_button_release(self, src, tgt, event):
        """ Al soltar el boton 1, se reinician startx y starty, para indicar
            que el marcador se dejo de utilizar.
        """
        self.startx = self.starty = None


    def on_motion_notify(self, src, tgt, event):
        """ Atención a movimientos del raton.
        """
        if event.button.button == 1:                    # Boton 1 oprimido?
            if self.startx == None:                     # Si no se detectó correctamente
                return                                  # el activar (oprimir), salimos

            dx = event.x - self.startx                  # Calcular cuanto se movio
            dy = event.y - self.starty

            self.goto_x_y(self.marker.get_property("x") + dx,   # Corregir posicion
                          self.marker.get_property("y") + dy)

            self.handler(self.startx, self.starty)      # e informar al propietario
                                                        # del marcador

    def goto_x_y(self, x, y, update = True):
        """ Mover el marcador a una nueva posicion.
        """
        self.marker.set_property("x", x - MARKER_SIZE//2)
        self.marker.set_property("y", y - MARKER_SIZE//2)
        if update:
            self.startx = x
            self.starty = y



class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())

        canvas = GooCanvas.Canvas()
        cvroot = canvas.get_root_item()

        r = CG_Marker(cvroot, 100, 140, self.test_handler)

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
