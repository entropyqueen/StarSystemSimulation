from panda3d.core import LPoint3f, WindowProperties
from direct.gui.OnscreenText import OnscreenText, TextNode


import config


class Actions:

    def __init__(self, base):
        self.help_text_node = None
        self.help_is_display = False
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
        # TODO: Adjust zoom object to screen size
        x, y, z = obj.pos

        dx = x + 10*obj.scale
        dy = y + 10*obj.scale
        dz = z + 10*obj.scale
        #dst = np.linalg.norm(obj.obj.position - self.cam.getPos())  # distance in AU
        #unit_v = (obj.obj.position - self.obj.position) / dst
        #new_pos = LPoint3f(np.array(dx, dy, dz) * unit_v)
        new_pos = LPoint3f(dx, dy, dz)
        self.base.cam.setPos(new_pos)
        self.base.cam.lookAt(obj.obj_node_path)

    def focus_camera_on_prev(self):
        if self.base.selected_object is not None:
            self.base.cam.lookAt(self.select_object_prev().obj_node_path)

    def focus_camera_on_next(self):
        if self.base.selected_object is not None:
            self.base.cam.lookAt(self.select_object_next().obj_node_path)

    def focus_selected(self):
        if self.base.selected_object is not None:
            self.focus_camera_on(self.base.selected_object)

    def sim_pause(self):
        self.base.sim_paused = not self.base.sim_paused

    def toggle_help(self):
        if self.help_is_display:
            self.help_text_node.destroy()
        else:
            help_text = 'Help:\n  Repeating keys:'
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
