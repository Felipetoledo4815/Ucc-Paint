#!/usr/bin/env python3

# -*- coding: utf-8 -*-
#
##  ucc_editor.py
#
#  Copyright 2017 Unknown <root@hp425>
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
gi.require_version('GooCanvas', '2.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GooCanvas
import os.path as osp

from ucc_marker import CG_Marker
from ucc_rectangle import CG_Rectangle
from PolyLine import CG_PolyLine
from ucc_bezier import CG_Bezier


ICON_DIR            = "icons"           # Los iconos estan en un sub-directorio


class CG_Toolbox(Gtk.HBox):
    """ Clase maneja la 'caja de herramientas' para seleccionar caracteristicas
        de los elementos a dibujar.
        Hereda de HBox (caja horizontal)
    """
    # defino un enum con estas variables con las que voy a moverme en
    # la caja de herramientas, range es un generador de numeros, en este
    # caso generaria 0, 1, 2 y 3 y al 0 lo asigna a RECT, el 1 a BEZIER y asi...
    RECT, BEZIER, ELLIPSE, LINE, TRIANGLE, NONE= range(6)

    def __init__(self):
        super(CG_Toolbox, self).__init__()
        # svg_file es la imagen en ese formato y el hint es el cartel de ayuda en la imagen
        # kind indica el tipo de herramienta que se va a emplear a partir del enum
        for svg_file, hint, kind in (
                    ("ucc_rect.svg",     "Rectangulo",   CG_Toolbox.RECT),
                    ("ucc_bezier.svg",   "Curva Bezier", CG_Toolbox.BEZIER),
                    ("ucc_ellipse.svg",  "Ellipse",      CG_Toolbox.ELLIPSE),
                    ("ucc_line.svg",     "Linea recta",  CG_Toolbox.LINE),
                    ("ucc_triangle.svg", "Triangulo",    CG_Toolbox.TRIANGLE) ):
                    # se agrega la , para indicar que es una tupla
                    # en caso de ser un solo elemento

            self.mode = CG_Toolbox.NONE

            # pixbuf contenedor de la imagen, ancho, alto (-1 ignora) y
            # true (mantiene el aspecto de la figura original)
            pxb = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                        osp.join(ICON_DIR, svg_file), 32, -1, True)

            # defino imagen que va a contener el pixbuf
            img = Gtk.Image.new_from_pixbuf(pxb)

            # defino toglebutton (para que pueda mantenerse activo)
            btn = Gtk.ToggleButton(image = img,                 # Imagen a mostrar
                                   tooltip_text = hint,         # Texto de ayuda
                                   active = self.mode == kind)  # Estado activo inicial

            # Agregar propiedad al boton con su tipo (kind)
            btn.kind = kind

            btn.ident = btn.connect("clicked", self.on_button_clicked, kind)

            # Los false indican que no debe extenderse al ancho y altos completos
            # el 2 indica que se van a dejar 2 px de padding
            self.pack_start(btn, False, False, 2)
            
        self.lw_spbtn = Gtk.SpinButton.new_with_range(2.0, 20.0, 0.5)
        self.lw_spbtn.set_tooltip_text("Grosor de linea")
        self.pack_start(self.lw_spbtn, False, False, 2)
        
        color = Gdk.RGBA()
        color.green = 1
        color.red = 0
        color.blue = 0
        color.alpha = 1
        self.line_color_btn = Gtk.ColorButton.new_with_rgba(color)
        self.line_color_btn.set_tooltip_text("Color de linea")
        self.line_color_btn.set_alpha(1.0)
        self.pack_start(self.line_color_btn, False, False, 2)

        color = Gdk.RGBA()
        color.green = 1
        color.red = 0
        color.blue = 0
        color.alpha = 1
        self.fill_color_btn = Gtk.ColorButton.new_with_rgba(color)
        self.fill_color_btn.set_tooltip_text("Color de llenado")
        self.fill_color_btn.set_use_alpha(True)
        self.pack_start(self.fill_color_btn, False, False, 2)


    def on_button_clicked(self, btn, kind):
        for b in self.get_children():
            if b == self.lw_spbtn:
                return
            # hace que self reconozca quienes son sus hijos
            with b.handler_block(b.ident):
                # bloqueo el handler que recibe el b.id (click del boton)
                # mientras se modifica la condicion del estado activo del boton:
                b.set_active(b.kind == kind)
                self.mode = kind
        # seteo el mode de la caja de herramientas por el tipo presionado




class CG_Canvas(Gtk.ScrolledWindow):
    """ Area de dibujo. El area de dibujo se ubica en un ScrolledWindow, para
        agregar barras desplazadoras laterales.
    """
    def __init__(self, tb):
        super(CG_Canvas, self).__init__()
        self.toolbox = tb

        self.canvas = GooCanvas.Canvas()
        self.cvroot = self.canvas.get_root_item()
        self.canvas.connect("button-press-event", self.on_button_pressed)
        self.sheet = GooCanvas.CanvasGroup(
                    parent = self.cvroot,
                    x = 0, y = 0)

        self.add(self.canvas)
        
        
    def gdkcolor_to_int(self, color):
        r, g, b = color.to_floats()
        col = int(r * 255)
        col = col * 256 + int(g * 255)
        col = col * 256 + int(b * 255)
        col = col * 256 + 255
        return col
        
        
    def on_button_pressed(self, src, event):
        if event.button != 1: return
        lw = self.toolbox.lw_spbtn.get_value()
        lcolor = self.toolbox.line_color_btn.get_color()
        fcolor = self.toolbox.fill_color_btn.get_color()
        if self.toolbox.mode == CG_Toolbox.RECT:
            CG_Rectangle(self.sheet, event.x, event.y,
                         stroke_color = self.gdkcolor_to_int(lcolor),
                         line_width = lw,
                         fill_color = self.gdkcolor_to_int(fcolor))
            self.toolbox.mode = CG_Toolbox.NONE
            CG_Toolbox.on_button_clicked(self.toolbox, self.toolbox, CG_Toolbox.NONE)   #Deberia pasarle un btn pero nunca se usa porque adentro de la f() hace un for
        elif self.toolbox.mode == CG_Toolbox.LINE:
            CG_PolyLine(self.sheet, event.x, event.y,
                        width = lw,
                        color = self.gdkcolor_to_int(lcolor))
            self.toolbox.mode = CG_Toolbox.NONE
            CG_Toolbox.on_button_clicked(self.toolbox, self.toolbox, CG_Toolbox.NONE)   #Deberia pasarle un btn pero nunca se usa porque adentro de la f() hace un for
        elif self.toolbox.mode == CG_Toolbox.BEZIER:
            CG_Bezier(self.sheet, event.x, event.y,
                      width=lw,
                      color=self.gdkcolor_to_int(lcolor)
                      )
            self.toolbox.mode = CG_Toolbox.NONE
            CG_Toolbox.on_button_clicked(self.toolbox, self.toolbox, CG_Toolbox.NONE)   #Deberia pasarle un btn pero nunca se usa porque adentro de la f() hace un for






class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect('destroy', lambda x: Gtk.main_quit())
        self.set_size_request(400, 400)

        tb = CG_Toolbox()                       # instancia de caja de herramientas
        cv = CG_Canvas(tb)                      # instancia del area de dibujo

        vbox = Gtk.VBox()                       # defino caja vertical
        vbox.pack_start(tb, False, False, 2)    # insertar toolbox, sin expansion
        vbox.pack_start(cv, True, True, 0)      # insertar area de dibujo - con expansion

        self.add(vbox)                          # insertar caja vertical en ventana
        self.show_all()

    def run(self):
        Gtk.main()


def main():
    mw = MainWindow()
    mw.run()
    return 0

if __name__ == '__main__':
    main()
