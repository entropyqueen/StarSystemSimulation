from panda3d.core import LPoint3f, WindowProperties
from direct.gui.OnscreenText import OnscreenText, TextNode
import numpy as np

import config


class Actions:

    def __init__(self, base):
        self.help_text_node = None
        self.help_is_display = False
        self.pause_text_node = None
        self.base = base

        self.last_mouse_x = self.base.win.getProperties().getXSize() / 2
        self.last_mouse_y = self.base.win.getProperties().getYSize() / 2

    def increase_zoom(self):
        self.base.zoom_factor *= config.ZOOM_FACTOR_STEP
        for o in self.base.objects_to_display:
            o.delete_history()

    def decrease_zoom(self):
        if self.base.zoom_factor >= config.ZOOM_FACTOR_STEP**2:
            self.base.zoom_factor //= config.ZOOM_FACTOR_STEP
        else:
            self.base.zoom_factor *= (config.ZOOM_FACTOR_STEP / 10)
        for o in self.base.objects_to_display:
            o.delete_history()

    def mouse_switch_mode(self):
        wp = WindowProperties()
        if self.base.win.getProperties().get_mouse_mode() == WindowProperties.M_relative:
            wp.setMouseMode(WindowProperties.M_absolute)
            wp.setCursorHidden(False)
        else:
            self.base.win.movePointer(
                0,
                int(self.base.win.getProperties().getXSize() / 2),
                int(self.base.win.getProperties().getYSize() / 2)
            )
            self.last_mouse_x = self.base.win.getProperties().getXSize() / 2
            self.last_mouse_y = self.base.win.getProperties().getYSize() / 2
            wp.setMouseMode(WindowProperties.M_relative)
            wp.setCursorHidden(True)
        self.base.win.requestProperties(wp)

    def delete_selected(self):
        if self.base.selected_object is not None:
            self.base.universe.objects.remove(self.base.selected_object.obj)
            self.base.selected_object.obj_node_path.removeNode()
            self.base.objects_to_display.remove(self.base.selected_object)
            self.base.selected_object_iter -= 1
            self.select_object_next()
            if len(self.base.objects_to_display) == 0:
                self.base.selected_object = None
                self.base.selected_object_iter = 0

    def select_object_prev(self):
        if len(self.base.objects_to_display) == 0:
            return None
        self.base.selected_object_iter -= 1
        if self.base.selected_object_iter < 0:
            self.base.selected_object_iter = len(self.base.objects_to_display) - 1
        self.base.selected_object = self.base.objects_to_display[self.base.selected_object_iter]
        return self.base.selected_object

    def select_object_next(self):
        if len(self.base.objects_to_display) == 0:
            return None
        self.base.selected_object_iter += 1
        if self.base.selected_object_iter >= len(self.base.objects_to_display):
            self.base.selected_object_iter = 0
        self.base.selected_object = self.base.objects_to_display[self.base.selected_object_iter]
        return self.base.selected_object

    def focus_camera_on(self, obj):
        x, y, z = obj.pos
        dx = x + 10 * obj.scale
        dy = y - 10 * obj.scale
        dz = z

        try:
            # if there is a star we want to be between a star and the object to look at
            light = render.find('**/*_light')
            if light.getPos() != obj.pos:
                light_direction = (obj.pos - light.getPos()) / np.linalg.norm(obj.pos - light.getPos())
                pos = light_direction * (np.linalg.norm(obj.pos - light.getPos()) - 10 * obj.scale)
            else:
                pos = LPoint3f(dx, dy, dz)
        except AssertionError:
            pos = LPoint3f(dx, dy, dz)

        self.base.cam.setPos(pos)
        self.base.cam.lookAt(obj.obj_node_path)

    def focus_camera_on_prev(self):
        if self.base.selected_object is not None:
            self.base.cam.lookAt(self.select_object_prev().obj_node_path)

    def focus_camera_on_next(self):
        if self.base.selected_object is not None:
            self.base.cam.lookAt(self.select_object_next().obj_node_path)

    def focus_selected(self):
        self.base.lock_focus = not self.base.lock_focus
        if self.base.selected_object is not None and self.base.lock_focus:
            self.focus_camera_on(self.base.selected_object)

    def sim_pause(self):
        self.base.sim_paused = not self.base.sim_paused
        self.pause_message()

    def pause_message(self):
        if self.base.sim_paused:
            self.pause_text_node = OnscreenText(
                text=f'SIMULATION IS PAUSED (press {config.KEYMAP_ONCE["PAUSE"]} to resume)',
                pos=(0.1, -1.93), fg=(1, 1, 1, 1),
                parent=self.base.a2dTopLeft, align=TextNode.ALeft, scale=.05
            )
        elif self.pause_text_node is not None:
            self.pause_text_node.destroy()
            self.pause_text_node = None

    def toggle_help(self):
        if self.help_is_display:
            self.help_text_node.destroy()
            self.help_text_node = None
            if self.pause_text_node is not None:
                self.pause_text_node.show()
        else:
            if self.pause_text_node is not None:
                self.pause_text_node.hide()
            help_text = 'Help:\n  Repeating keys:\n'
            for k, v in config.KEYMAP_REP.items():
                help_text += f'    {k}:\t\t{v}\n'
            help_text += '\n  One time keys:\n'
            for k, v in config.KEYMAP_ONCE.items():
                help_text += f'    {k}:\t\t{v}\n'
            self.help_text_node = OnscreenText(
                text=help_text, pos=(1, -0.1), fg=(1, 1, 1, 1),
                parent=self.base.a2dTopLeft, align=TextNode.ALeft, scale=.04
            )
        self.help_is_display = not self.help_is_display
