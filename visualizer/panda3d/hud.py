from direct.gui.OnscreenText import OnscreenText, TextNode


class Hud:

    def __init__(self, base):

        self.base = base

        # Text info
        self.info_text = {}
        self.info_text_ids = {}

        # Axis info
        self.axis = None
        self.init_axis()

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
            parent=self.base.a2dTopLeft, align=TextNode.ALeft, scale=.04
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

    def update_axis(self, cam):
        self.axis.setH(cam.getH())
        self.axis.setP(cam.getP())
        self.axis.setR(cam.getR())

    def init_axis(self):
        self.axis = loader.loadModel('./models/axis.bam')
        self.axis.setScale(0.05)
        self.axis.setPos(self.base.a2dTopRight, -0.2, 0, -0.2)
        self.axis.reparentTo(render2d)
