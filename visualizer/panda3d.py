import sys
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, Vec3
from direct.gui.OnscreenText import OnscreenText, TextNode

import config
from utils import hex_to_rgb_norm
from physics.universe import Universe
from physics.sol import create_Sol_system
from visualizer.panda3d_object_display import ObjectDisplay


class PandaVisualizer(ShowBase):
    def __init__(self):
        super().__init__()

        # Window properties
        wp = WindowProperties()
        wp.setMouseMode(WindowProperties.M_relative)
        wp.setCursorHidden(True)
        wp.setSize(config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT)
        self.win.requestProperties(wp)

        self.zoom_factor = config.DEFAULT_ZOOM
        self.init_default_display()

        # Initialize display settings
        self.info_text = {}
        self.info_text_ids = {}
        self.objects_to_display = []
        self.selected_object_iter = 0

        # Controls initialization
        self.keymap_rep = {}
        for k in config.KEYMAP_REP.keys():
            self.keymap_rep[k] = False
        self.focus_selected = False
        self.init_controls()
        self.cam_speed = config.CAM_SPEED
        self.cam_rotation_speed = config.CAM_ROTATION_SPEED
        self.last_mouse_x, self.last_mouse_y = 0, 0

        # Initialize Universe, and populate with Sol
        self.universe = Universe()
        sol = create_Sol_system(self.universe)
        for obj in sol:
            self.objects_to_display.append(ObjectDisplay(obj))
        self.selected_object = self.objects_to_display[self.selected_object_iter]
        self.info('sim_date', f'Simulation date: {self.universe.str_date}')

        # Launch tasks
        self.update_task = self.taskMgr.add(self.update, 'update')
        self.mouse_task = self.taskMgr.add(self.mouse_control, 'mouse_control')
        self.keyboard_task = self.taskMgr.add(self.keyboard_control, 'keyboard_control')
        self.focus_camera_on(self.selected_object)

    def init_controls(self):
        self.disableMouse()
        for k, v in config.KEYMAP_REP.items():
            if v not in ['mouse_x', 'mouse_y']:
                self.accept(v, self.update_keymap, [k, True])
                self.accept(f'{v}-up', self.update_keymap, [k, False])
        for k, v in config.KEYMAP_ONCE.items():
            if k == 'ZOOM_IN':
                self.accept(v, self.increase_zoom)
            if k == 'ZOOM_OUT':
                self.accept(v, self.decrease_zoom)
            if k == 'TARGET_PREV':
                self.accept(v, self.focus_camera_on_prev)
            if k == 'TARGET_NEXT':
                self.accept(v, self.focus_camera_on_next)
            if k == 'LOCK_FOCUS':
                self.accept(v, self.toggle_focus)
            if k == 'QUIT':
                self.accept(v, sys.exit)

    def update_keymap(self, control_name, control_state):
        self.keymap_rep[control_name] = control_state

    def init_default_display(self):
        self.setBackgroundColor(*hex_to_rgb_norm('#000000'))
        self.cam.setPos(0, -20, 20)
        self.cam.lookAt(0, 0, 0)

    def keyboard_control(self, task):
        dt = globalClock.getDt()
        s = self.cam_speed
        r = self.cam_rotation_speed

        if self.keymap_rep['FWD']:
            self.cam.setPos(self.cam, Vec3(0, s * dt, 0))
        if self.keymap_rep['BACKWD']:
            self.cam.setPos(self.cam, Vec3(0, -s * dt, 0))
        if self.keymap_rep['RIGHT']:
            self.cam.setPos(self.cam, Vec3(s * dt, 0, 0))
        if self.keymap_rep['LEFT']:
            self.cam.setPos(self.cam, Vec3(-s * dt, 0, 0))
        if self.keymap_rep['UP']:
            self.cam.setPos(self.cam, Vec3(0, 0, s * dt))
        if self.keymap_rep['DOWN']:
            self.cam.setPos(self.cam, Vec3(0, 0, -s * dt))
        if self.keymap_rep['ROLL_R']:
            self.cam.setHpr(self.cam, Vec3(0, 0, r * dt))
        if self.keymap_rep['ROLL_L']:
            self.cam.setHpr(self.cam, Vec3(0, 0, -r * dt))
        if self.keymap_rep['MVT_SPEED+']:
            self.cam_speed += config.CAM_SPEED_STEP
            self.cam_rotation_speed *= config.CAM_ROTATION_SPEED_STEP
            if self.cam_speed > config.MAX_CAM_SPEED:
                self.cam_speed = config.MAX_CAM_SPEED
            if self.cam_speed > config.MAX_CAM_ROTATION_SPEED:
                self.cam_speed = config.MAX_CAM_ROTATION_SPEED
        if self.keymap_rep['MVT_SPEED-']:
            self.cam_speed //= config.CAM_SPEED_STEP
            self.cam_rotation_speed -= config.CAM_ROTATION_SPEED_STEP
            if self.cam_speed < config.MIN_CAM_SPEED:
                self.cam_speed = config.MIN_CAM_SPEED
            if self.cam_speed < config.MIN_CAM_ROTATION_SPEED:
                self.cam_speed = config.MIN_CAM_ROTATION_SPEED
        return task.cont

    def increase_zoom(self):
        self.zoom_factor *= config.ZOOM_FACTOR_STEP

    def decrease_zoom(self):
        self.zoom_factor //= config.ZOOM_FACTOR_STEP
        if self.zoom_factor < 1:
            self.zoom_factor = 1

    def mouse_control(self, task):
        x, y, dx, dy = 0, 0, 0, 0
        mw = self.mouseWatcherNode
        has_mouse = mw.hasMouse()
        if has_mouse:
            x, y = mw.getMouseX(), mw.getMouseY()
            dx = (self.last_mouse_x - x) * 10 * config.MOUSE_SENSITIVITY
            dy = (y - self.last_mouse_y) * 10 * config.MOUSE_SENSITIVITY

        self.last_mouse_x, self.last_mouse_y = x, y
        self.cam.setH(self.cam, dx)
        self.cam.setP(self.cam, dy)
        return task.cont

    def update(self, task):
        dt = globalClock.getDt()

        self.info('sim_date', f'Simulation date: {self.universe.str_date}')
        if config.VERBOSE:
            print('===============================================================')
            print(str(self.universe))

        if config.CSV:
            with open(config.CSV_OUTPUT, 'w') as f:
                f.write(self.universe.to_csv())
        self.universe.update()
        if self.focus_selected:
            self.focus_camera_on(self.selected_object)
        for obj in self.objects_to_display:
            obj.zoom_factor = self.zoom_factor
            obj.update()
        return task.cont

    def select_object_prev(self):
        self.selected_object_iter -= 1
        if self.selected_object_iter < 0:
            self.selected_object_iter = len(self.objects_to_display) - 1
        self.selected_object = self.objects_to_display[self.selected_object_iter]
        return self.selected_object

    def select_object_next(self):
        self.selected_object_iter += 1
        if self.selected_object_iter >= len(self.objects_to_display):
            self.selected_object_iter = 0
        self.selected_object = self.objects_to_display[self.selected_object_iter]
        return self.selected_object

    def focus_camera_on(self, obj):
        # TODO: Adjust zoom object to screen size
        self.info('focus_camera', f'Focusing on {obj.obj.name}')
        x, y, z = obj.pos
        y -= 2 * obj.radius
        self.cam.setPos(x, y, z)
        self.cam.lookAt(*obj.pos)

    def focus_camera_on_prev(self):
        self.focus_camera_on(self.select_object_prev())

    def focus_camera_on_next(self):
        self.focus_camera_on(self.select_object_next())

    def toggle_focus(self):
        self.focus_selected = not self.focus_selected

    def foobar(self):
        axis = self.loader.loadModel('models/zup-axis')
        axis.reparentTo(self.render)

    def add_info_text(self, key, text):

        idx = 0
        if len(self.info_text_ids) == 0:
            idx = 0
        else:
            for idx, k in enumerate(sorted(self.info_text_ids)):
                if idx != k:
                    break
                else:
                    idx += 1
        self.info_text[key] = idx
        self.info_text_ids[idx] = OnscreenText(
            text=text, pos=(0.06, -.06 * (idx + 0.5)), fg=(1, 1, 1, 1),
            parent=self.a2dTopLeft, align=TextNode.ALeft, scale=.04
        )

    def info(self, key, text):
        try:
            if key not in self.info_text:
                self.add_info_text(key, text)
            else:
                idx = self.info_text[key]
                if isinstance(self.info_text_ids[idx], OnscreenText):
                    self.info_text_ids[idx].setText(text)
        except KeyError:
            # nothing to update
            pass

    def del_info_text(self, key):
        try:
            if isinstance(self.info_text_ids[self.info_text[key]], OnscreenText):
                self.info_text_ids[self.info_text[key]].destroy()
        except KeyError:
            # nothing to delete
            pass
