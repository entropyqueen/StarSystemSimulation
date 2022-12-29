import sys
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, Vec3

from math import pi, sin, cos

import config
from utils import hex_to_rgb_norm


class Visualizer(ShowBase):
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
            'QUIT': False,
        }
        self.init_controls()
        self.cam_speed = config.CAM_SPEED
        self.cam_rotation_speed = config.CAM_ROTATION_SPEED
        self.updateTask = self.taskMgr.add(self.keyboard_control, "keyboardControl")
        self.last_mouse_x, self.last_mouse_y = None, None
        self.mouseTask = self.taskMgr.add(self.mouse_control, "MouseControl")

        self.init_default_display()
        self.foobar()

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
        self.cam.setPos(0.0, -10, 10.0)
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
            # Or applying a coefficient to distances / changing universe size?
            pass
        if self.keymap['ZOOM_OUT']:
            pass
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

    def recenterMouse(self):
        self.win.movePointer(
            0,
            int(self.win.getProperties().getXSize() / 2),
            int(self.win.getProperties().getYSize() / 2)
        )
        self.last_mouse_x, self.last_mouse_y = 0, 0

    def foobar(self):
        axis = self.loader.loadModel('models/zup-axis')
        axis.reparentTo(self.render)

        sphere = self.loader.loadModel('./models/sphere.glb')
        sphere.setScale(1, 1, 1)
        sphere.setPos(0, 0, 0)
        sphere.setColor(*hex_to_rgb_norm('#5b5ddf'))
        sphere.reparentTo(self.render)
