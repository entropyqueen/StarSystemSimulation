import sys
from panda3d.core import WindowProperties, Vec3

import config
from visualizer.panda3d.actions import Actions


class Inputs:

    def __init__(self, base):

        self.base = base

        self.keymap_rep = {}
        for k in config.KEYMAP_REP.keys():
            self.keymap_rep[k] = False
        self.cam_speed = config.CAM_SPEED
        self.cam_rotation_speed = config.CAM_ROTATION_SPEED
        self.last_mouse_x = 0
        self.last_mouse_y = 0

        self.actions = Actions(base)

        self.init_controls()

    def start_task(self):
        self.base.taskMgr.add(self.mouse_control, 'mouse_control')
        self.base.taskMgr.add(self.keyboard_control, 'keyboard_control')

    def update_keymap(self, control_name, control_state):
        self.keymap_rep[control_name] = control_state

    def init_controls(self):
        for k, v in config.KEYMAP_REP.items():
            if v not in ['mouse_x', 'mouse_y']:
                self.base.accept(v, self.update_keymap, [k, True])
                self.base.accept(f'{v}-up', self.update_keymap, [k, False])
        for k, v in config.KEYMAP_ONCE.items():
            if k == 'ZOOM_IN':
                self.base.accept(v, self.actions.increase_zoom)
            if k == 'ZOOM_OUT':
                self.base.accept(v, self.actions.decrease_zoom)
            if k == 'TARGET_PREV':
                self.base.accept(v, self.actions.focus_camera_on_prev)
            if k == 'TARGET_NEXT':
                self.base.accept(v, self.actions.focus_camera_on_next)
            if k == 'FOCUS_TARGET':
                self.base.accept(v, self.actions.focus_selected)
            if k == 'PAUSE':
                self.base.accept(v, self.actions.sim_pause)
            if k == 'MOUSE_SWITCH_MODE':
                self.base.accept(v, self.actions.mouse_switch_mode)
            if k == 'DELETE':
                self.base.accept(v, self.actions.delete_selected)
            if k == 'HELP':
                self.base.accept(v, self.actions.toggle_help)
            if k == 'QUIT':
                self.base.accept(v, sys.exit)

    def keyboard_control(self, task):
        dt = globalClock.getDt()
        s = self.cam_speed
        r = self.cam_rotation_speed

        if self.keymap_rep['FWD']:
            self.base.cam.setPos(self.base.cam, Vec3(0, s * dt, 0))
        if self.keymap_rep['BACKWD']:
            self.base.cam.setPos(self.base.cam, Vec3(0, -s * dt, 0))
        if self.keymap_rep['RIGHT']:
            self.base.cam.setPos(self.base.cam, Vec3(s * dt, 0, 0))
        if self.keymap_rep['LEFT']:
            self.base.cam.setPos(self.base.cam, Vec3(-s * dt, 0, 0))
        if self.keymap_rep['UP']:
            self.base.cam.setPos(self.base.cam, Vec3(0, 0, s * dt))
        if self.keymap_rep['DOWN']:
            self.base.cam.setPos(self.base.cam, Vec3(0, 0, -s * dt))
        if self.keymap_rep['ROLL_R']:
            self.base.cam.setHpr(self.base.cam, Vec3(0, 0, r * dt))
        if self.keymap_rep['ROLL_L']:
            self.base.cam.setHpr(self.base.cam, Vec3(0, 0, -r * dt))
        if self.keymap_rep['MVT_SPEED+']:
            self.cam_speed *= config.CAM_SPEED_STEP
            self.cam_rotation_speed *= config.CAM_ROTATION_SPEED_STEP
            if self.cam_speed > config.MAX_CAM_SPEED:
                self.cam_speed = config.MAX_CAM_SPEED
            if self.cam_speed > config.MAX_CAM_ROTATION_SPEED:
                self.cam_speed = config.MAX_CAM_ROTATION_SPEED
        if self.keymap_rep['MVT_SPEED-']:
            self.cam_speed //= config.CAM_SPEED_STEP
            self.cam_rotation_speed //= config.CAM_ROTATION_SPEED_STEP
            if self.cam_speed < config.MIN_CAM_SPEED:
                self.cam_speed = config.MIN_CAM_SPEED
            if self.cam_speed < config.MIN_CAM_ROTATION_SPEED:
                self.cam_speed = config.MIN_CAM_ROTATION_SPEED
        return task.cont

    def mouse_control(self, task):
        if self.base.win.getProperties().get_mouse_mode() == WindowProperties.M_absolute:
            return task.cont

        x, y, dx, dy = 0, 0, 0, 0
        mw = self.base.mouseWatcherNode
        has_mouse = mw.hasMouse()
        if has_mouse:
            x, y = mw.getMouseX(), mw.getMouseY()
            dx = (self.last_mouse_x - x) * 10 * config.MOUSE_SENSITIVITY
            dy = (y - self.last_mouse_y) * 10 * config.MOUSE_SENSITIVITY

        if config.MOUSE_INVERT_X:
            dx = -dx
        if config.MOUSE_INVERT_Y:
            dy = -dy

        self.last_mouse_x, self.last_mouse_y = x, y
        self.base.cam.setH(self.base.cam, dx)
        self.base.cam.setP(self.base.cam, dy)
        return task.cont
