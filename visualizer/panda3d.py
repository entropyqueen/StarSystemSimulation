import sys
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, Vec3, LPoint3f
from direct.gui.OnscreenText import OnscreenText, TextNode
from astropy import units as u
import numpy as np

import config
from utils import hex_to_rgb_norm
from physics.universe import Universe
from physics import sol
from visualizer.panda3d_object_display import ObjectDisplay


class PandaVisualizer(ShowBase):
    def __init__(self, realist_view=False):
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
        self.init_controls()
        self.cam_speed = config.CAM_SPEED
        self.cam_rotation_speed = config.CAM_ROTATION_SPEED
        self.last_mouse_x, self.last_mouse_y = 0, 0

        self.realist_view = realist_view
        self.sim_paused = False
        self.units = u.Rjup
        # Initialize Universe, and populate with Sol
        self.universe = Universe()
        self.universe.dt = 1 * u.h
        system = sol.create_Sol_system(self.universe)
        for obj in system:
            texture = None
            try:
                texture = sol.texture_map[obj.name]
            except KeyError:
                pass
            self.objects_to_display.append(
                ObjectDisplay(obj, units=self.units, realist_view=realist_view, texture_path=texture)
            )
        self.selected_object = self.objects_to_display[self.selected_object_iter]

        self.focus_selected()
        self.axis = None
        self.init_axis()

        # Launch tasks
        self.update_task = self.taskMgr.add(self.update, 'update')
        self.mouse_task = self.taskMgr.add(self.mouse_control, 'mouse_control')
        self.keyboard_task = self.taskMgr.add(self.keyboard_control, 'keyboard_control')

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
            if k == 'FOCUS_TARGET':
                self.accept(v, self.focus_selected)
            if k == 'PAUSE':
                self.accept(v, self.sim_pause)
            if k == 'QUIT':
                self.accept(v, sys.exit)

    def update_keymap(self, control_name, control_state):
        self.keymap_rep[control_name] = control_state

    def init_default_display(self):
        self.setBackgroundColor(*hex_to_rgb_norm('#000000'))

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

        self.display_infos()
        self.update_axis()

        if config.VERBOSE:
            print('===============================================================')
            print(str(self.universe))

        if config.CSV:
            with open(config.CSV_OUTPUT, 'w') as f:
                f.write(self.universe.to_csv())

        if not self.sim_paused:
            self.universe.update()

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
        x, y, z = obj.pos

        dx = x + 10*obj.scale
        dy = y + 10*obj.scale
        dz = z + 10*obj.scale

        self.cam.setPos(dx, dy, dz)
        self.cam.lookAt(obj.obj_node_path)

    def focus_camera_on_prev(self):
        self.cam.lookAt(self.select_object_prev().obj_node_path)

    def focus_camera_on_next(self):
        self.cam.lookAt(self.select_object_next().obj_node_path)

    def focus_selected(self):
        self.focus_camera_on(self.selected_object)

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

    def del_info(self, key):
        try:
            if isinstance(self.info_text_ids[self.info_text[key]], OnscreenText):
                self.info_text_ids[self.info_text[key]].destroy()
                del self.info_text_ids[self.info_text[key]]
                del self.info_text[key]
        except KeyError:
            # nothing to delete
            pass

    def display_infos(self):
        self.info('sim_date', f'Simulation date: {self.universe.str_date}')
        self.info('cam_info', f'Camera Infos: FOV: {int(self.cam.node().getLens().get_hfov())}')
        self.info(
            'cam_pos',
            f'\tx:{self.cam.getX():.2} y: {self.cam.getY():.2} z: {self.cam.getZ():.2}'
        )
        self.info(
            'cam_rot',
            f'\th:{self.cam.getH():.2} p: {self.cam.getP():.2} r: {self.cam.getR():.2}'
        )
        if self.sim_paused:
            self.info('pause', 'Sim State: PAUSED')
        else:
            self.info('pause', 'Sim State: RUNNING')

        self.info(
            'focus_cam_l1',
            f'Selected: [{self.selected_object.obj.name}]:'
        )
        self.info(
            'focus_cam_l2',
            f'\t R = {self.selected_object.obj.radius.to(u.km):.2e} '
            f'(display size: {self.selected_object.scale:.2e})'
        )
        self.info(
            'focus_cam_l3', '\t'
            f'x: {self.selected_object.pos[0]:.2e}, '
            f'y: {self.selected_object.pos[1]:.2e}, '
            f'z: {self.selected_object.pos.getZ():.2e}'
        )
        self.info(
            'dst_to_selected',
            f'Distance to selected: {np.linalg.norm(tuple(self.cam.getPos() - self.selected_object.pos)):.2e}'
        )
        self.info('zoom', f'zoom lvl: {self.zoom_factor:.2e}')

    def sim_pause(self):
        self.sim_paused = not self.sim_paused

    def update_axis(self):
        self.axis.setH(self.cam.getH())
        self.axis.setP(self.cam.getP())
        self.axis.setR(self.cam.getR())

    def init_axis(self):
        self.axis = self.loader.loadModel('./models/axis.glb')
        self.axis.setScale(0.05)
        self.axis.setPos(self.a2dTopRight, -0.2, 0, -0.2)
        self.axis.reparentTo(self.render2d)
