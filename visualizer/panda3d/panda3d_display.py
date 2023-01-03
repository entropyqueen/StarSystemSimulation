from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from direct.filter.CommonFilters import CommonFilters
from astropy import units as u
import numpy as np

import config
from loader.loader import StarSystemLoader
from utils import hex_to_rgb_norm
from physics.universe import Universe
from loader import sol
from visualizer.panda3d.inputs import Inputs
from visualizer.panda3d.hud import Hud
from visualizer.panda3d.object_display import ObjectDisplay
from visualizer.panda3d.skybox import SkyBox


class Panda3dDisplay(ShowBase):
    def __init__(self, star_system_path):
        super().__init__()

        # Window properties
        wp = WindowProperties()
        wp.setTitle('Star System Simulator')
        wp.setMouseMode(WindowProperties.M_absolute)
        wp.setCursorHidden(False)
        wp.setSize(config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT)
        self.win.requestProperties(wp)

        # Initialize display settings
        SkyBox(self)
        self.hud = Hud(self)
        self.filters = CommonFilters(self.win, self.cam)
        self.filters.setBloom(blend=(0, 0, 0, 1), desat=-0.5, mintrigger=0.8, maxtrigger=1, intensity=1.0, size=1000)
        self.zoom_factor = config.DEFAULT_ZOOM

        # Controls initialization
        self.disableMouse()  # disable panda's default mouse controls
        self.inputs = Inputs(self)

        # Initialize objects
        self.objects_to_display = []
        self.selected_object = None
        self.selected_object_iter = 0

        # Initialize simulation
        self.realist_view = config.REALIST_VIEW
        self.sim_paused = True
        # Initialize Universe, and populate with Sol
        self.universe = Universe()

        # Load Star System
        ss_loader = StarSystemLoader(self.universe)
        system, self.units, _ = ss_loader.load(star_system_path)

        for obj in system:
            texture = None
            model = './models/sphere.glb'
            if obj.name in sol.texture_map:
                texture = sol.texture_map[obj.name]
            if obj.name in sol.model_map:
                model = sol.model_map[obj.name]
            self.objects_to_display.append(
                ObjectDisplay(
                    self, obj,
                    units=self.units['d_unit'], realist_view=self.realist_view,
                    model_path=model, textures=texture
                )
            )
        for obj1 in self.objects_to_display:
            if obj1.obj.is_star:
                for obj2 in self.objects_to_display:
                    if obj1 is not obj2:
                        obj2.obj_model.setLight(obj1.light_node_path)

        self.selected_object = self.objects_to_display[self.selected_object_iter]

        # Launch simulation
        self.update_task = self.taskMgr.add(self.update, 'update')
        self.inputs.start_task()

        # self.cam.lookAt(self.select_object_next().obj_node_path)

    def init_default_display(self):
        self.setBackgroundColor(*hex_to_rgb_norm('#000000'))

    def update(self, task):
        dt = globalClock.getDt()

        self.display_infos()
        self.hud.update_axis(self.cam)

        if not self.sim_paused:
            self.universe.update()

        for obj in self.objects_to_display:
            obj.update()
        return task.cont

    def display_infos(self):
        self.hud.info('sim_date', f'Simulation date: {self.universe.str_date}')
        self.hud.info('cam_info', f'Camera Infos: FOV: {int(self.cam.node().getLens().get_hfov())}')
        self.hud.info(
            'cam_pos',
            f'\tx:{self.cam.getX():.2} y: {self.cam.getY():.2} z: {self.cam.getZ():.2}'
        )
        self.hud.info(
            'cam_rot',
            f'\th:{self.cam.getH():.2} p: {self.cam.getP():.2} r: {self.cam.getR():.2}'
        )
        if self.sim_paused:
            self.hud.info('pause', 'Sim State: PAUSED')
        else:
            self.hud.info('pause', 'Sim State: RUNNING')

        try:
            self.hud.info(
                'focus_cam_l1',
                f'Selected: [{self.selected_object.obj.name}]:'
            )
            self.hud.info(
                'focus_cam_l2',
                f'\tR = {self.selected_object.obj.radius.to(u.km):.2e} '
                f'(display size: {self.selected_object.scale:.2e})'
            )
            self.hud.info(
                'focus_cam_l3', '\t'
                f'x: {self.selected_object.pos[0]:.2e}, '
                f'y: {self.selected_object.pos[1]:.2e}, '
                f'z: {self.selected_object.pos.getZ():.2e}'
            )
            self.hud.info(
                'dst_to_selected',
                f'Distance to selected: {np.linalg.norm(tuple(self.cam.getPos() - self.selected_object.pos)):.2e}'
            )
        except AttributeError:
            self.hud.info('focus_cam_l1', 'Selected: [None]:')
            self.hud.info('focus_cam_l2', '\tR = 0 (display size: 0)')
            self.hud.info('focus_cam_l3', '\tx: 0, y: 0, z:0')
            self.hud.info('dst_to_selected', 'Distance to selected: 0')

        self.hud.info('zoom', f'zoom lvl: {self.zoom_factor:.2e}')
