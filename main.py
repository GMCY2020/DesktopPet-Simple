# -*- coding = utf-8 -*-
# @Time     : 2021/01/26
# @Author   : GMCY
# @File     : main.py
# @Software : PyCharm

import os
import cfg_keqing  # 这个是刻晴的
import cfg_diaona  # 这个是迪奥娜的
import sys
import random
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class DesktopPet(QWidget):
    def __init__(self, cfg, parent=None, **kwargs):
        super(DesktopPet, self).__init__(parent)
        self.cfg = cfg
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.repaint()
        self.pet_images = self.randomLoadPetImages()
        self.image = QLabel(self)
        self.setImage(self.pet_images[0][0])
        self.is_follow_mouse = False
        self.mouse_drag_pos = self.pos()
        self.resize(800, 820)
        self.randomPosition()
        self.show()
        self.is_running_action = False
        self.action_images = []
        self.action_pointer = 0
        self.action_max_len = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.randomAct)
        self.timer.start(270)

    def randomAct(self):
        if not self.is_running_action:
            self.is_running_action = True
            self.action_images = random.choice(self.pet_images)
            self.action_max_len = len(self.action_images)
            self.action_pointer = 0
        self.runFrame()

    def runFrame(self):
        if self.action_pointer == self.action_max_len:
            self.is_running_action = False
            self.action_pointer = 0
            self.action_max_len = 0
        self.setImage(self.action_images[self.action_pointer])
        self.action_pointer += 1

    def setImage(self, image):
        self.image.setPixmap(QPixmap.fromImage(image))

    def randomLoadPetImages(self):
        pet_name = random.choice(list(self.cfg.PET_ACTIONS_MAP.keys()))
        actions = self.cfg.PET_ACTIONS_MAP[pet_name]
        pet_images = []
        for action in actions:
            pet_images.append(
                [self.loadImage(os.path.join(self.cfg.ROOT_DIR, pet_name, 'shime' + item + '.png')) for item in
                 action])

        return pet_images

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def loadImage(self, imagepath):
        image = QImage()
        image.load(imagepath)
        return image

    def randomPosition(self):
        screen_geo = QDesktopWidget().screenGeometry()
        pet_geo = self.geometry()
        width = (screen_geo.width() - pet_geo.width()) * random.random()
        height = (screen_geo.height() - pet_geo.height()) * random.random()
        self.move(width, height)

    def quit(self):
        self.close()
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 这里选择 刻晴-cfg_keqing 还是 迪奥娜-cfg_diaona
    pet = DesktopPet(cfg_keqing)

    sys.exit(app.exec_())