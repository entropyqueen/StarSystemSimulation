import sys
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, Vec3

import config
from utils import hex_to_rgb_norm
from physics.universe import Universe
from physics.sol import create_Sol_system
from visualizer.panda3d_object_display import ObjectDisplay


class PandaVisualizer(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Window properties
        wp = WindowProperties()
        wp.setMouseMode(WindowProperties.M_relative)
        wp.setCursorHidden(True)
        wp.setSize(config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT)
        self.win.requestProperties(wp)

        self.keymap = {
            'FWD': False,
            'BACKWD': False,
            'UP': False,
            'LEFT': False,
            'DOWN': False,
            'RIGHT': False,
            'ROLL_R': False,
            'ROLL_L': False,
            'ZOOM_IN': False,
            'ZOOM_OUT': False,
            'MVT_SPEED+': False,
            'MVT_SPEED-': False,
            'TARGET_PREV': False,
            'TARGET_NEXT': False,
            'QUIT': False,
        }
        self.init_controls()
        self.cam_speed = config.CAM_SPEED
        self.cam_rotation_speed = config.CAM_ROTATION_SPEED
        self.keyboard_task = self.taskMgr.add(self.keyboard_control, 'keyboard_control')
        self.last_mouse_x, self.last_mouse_y = 0, 0
        self.mouse_task = self.taskMgr.add(self.mouse_control, 'mouse_control')

        self.init_default_display()
        # self.foobar()

        # Initialize Universe, and populate with Sol
        self.universe = Universe()
        sol = create_Sol_system(self.universe)
        self.objects_to_display = []
        for obj in sol:
            self.objects_to_display.append(ObjectDisplay(obj))
        self.selected_object_iter = 0
        self.selected_object = self.objects_to_display[self.selected_object_iter]
        self.update_task = self.taskMgr.add(self.update, 'update')

    def init_controls(self):
        self.disableMouse()
        for k, v in config.KEYMAP.items():
            if v not in ['mouse_x', 'mouse_y']:
                self.accept(v, self.update_keymap, [k, True])
                self.accept(f'{v}-up', self.update_keymap, [k, False])

    def update_keymap(self, control_name, control_state):
        self.keymap[control_name] = control_state

    def init_default_display(self):
        self.setBackgroundColor(*hex_to_rgb_norm('#000000'))
        self.cam.setPos(0, -20, 20)
        self.cam.lookAt(0, 0, 0)

    def keyboard_control(self, task):
        dt = globalClock.getDt()
        s = self.cam_speed
        r = self.cam_rotation_speed

        if self.keymap['FWD']:
            self.cam.setPos(self.cam, Vec3(0, s * dt, 0))
        if self.keymap['BACKWD']:
            self.cam.setPos(self.cam, Vec3(0, -s * dt, 0))
        if self.keymap['RIGHT']:
            self.cam.setPos(self.cam, Vec3(s * dt, 0, 0))
        if self.keymap['LEFT']:
            self.cam.setPos(self.cam, Vec3(-s * dt, 0, 0))
        if self.keymap['UP']:
            self.cam.setPos(self.cam, Vec3(0, 0, s * dt))
        if self.keymap['DOWN']:
            self.cam.setPos(self.cam, Vec3(0, 0, -s * dt))
        if self.keymap['ROLL_R']:
            self.cam.setHpr(self.cam, Vec3(0, 0, r * dt))
        if self.keymap['ROLL_L']:
            self.cam.setHpr(self.cam, Vec3(0, 0, -r * dt))
        if self.keymap['MVT_SPEED+']:
            self.cam_speed += config.CAM_SPEED_STEP
            self.cam_rotation_speed += config.CAM_ROTATION_SPEED_STEP
            if self.cam_speed > config.MAX_CAM_SPEED:
                self.cam_speed = config.MAX_CAM_SPEED
            if self.cam_speed > config.MAX_CAM_ROTATION_SPEED:
                self.cam_speed = config.MAX_CAM_ROTATION_SPEED
        if self.keymap['MVT_SPEED-']:
            self.cam_speed -= config.CAM_SPEED_STEP
            self.cam_rotation_speed -= config.CAM_ROTATION_SPEED_STEP
            if self.cam_speed < config.MIN_CAM_SPEED:
                self.cam_speed = config.MIN_CAM_SPEED
            if self.cam_speed < config.MIN_CAM_ROTATION_SPEED:
                self.cam_speed = config.MIN_CAM_ROTATION_SPEED
        if self.keymap['ZOOM_IN']:
            # Zooming is FWD ?
            # Or applying a coefficient to distances / changing u size?
            pass
        if self.keymap['ZOOM_OUT']:
            pass
        if self.keymap['TARGET_PREV']:
            self.cam.lookAt(*self.select_object('prev').pos)
        if self.keymap['TARGET_NEXT']:
            self.cam.lookAt(*self.select_object('next').pos)
        if self.keymap['QUIT']:
            sys.exit(0)
        return task.cont

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

        if config.VERBOSE:
            print('===============================================================')
            print(str(self.universe))

        if config.CSV:
            with open(config.CSV_OUTPUT, 'w') as f:
                f.write(self.universe.to_csv())
        self.universe.update()
        for obj in self.objects_to_display:
            obj.update()

        return task.cont

    def select_object(self, direction):
        if direction == 'next':
            self.selected_object_iter += 1
        else:
            self.selected_object_iter -= 1
        if self.selected_object_iter < 0:
            self.selected_object_iter = len(self.objects_to_display) - 1
        elif self.selected_object_iter >= len(self.objects_to_display):
            self.selected_object_iter = 0
        self.selected_object = self.objects_to_display[self.selected_object_iter]
        return self.selected_object

    def foobar(self):
        axis = self.loader.loadModel('models/zup-axis')
        axis.reparentTo(self.render)

