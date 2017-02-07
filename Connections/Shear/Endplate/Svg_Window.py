'''
Created on Oct 20, 2016

@author: USER
'''
# from PyQt4 import QtSvg, QtGui, QtCore
from PyQt5 import QtSvg
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QFileDialog, QSpacerItem, QSizePolicy, QPushButton, \
                            QMessageBox, QHBoxLayout, QFrame, QLabel,QGridLayout
import sys
import shutil


class SvgWindow(object):
    #     def __init__(self, parent=None):
    #     def __init__(self):
    #         QApplication.__init__(self)
    #         self.mainController = parent
    #         self.call_svgwindow(filename, view)

    def call_svgwindow(self, filename, view, folder):
        self.folder = folder
        self.svgWidget = QtSvg.QSvgWidget()
        # self.svgWidget.renderer().load(filename)

        self.label = QLabel(self.svgWidget)
        self.label.setFrameShape(QFrame.Box)
        self.label.setFrameShadow(QFrame.Plain)
        self.label.setPixmap(QPixmap(filename))
        self.label.setScaledContents(True)

        self.gridlayout = QGridLayout(self.svgWidget)
        self.gridlayout.addWidget(self.label, 0, 0, 1, 3)
        spaceritem = QSpacerItem(260,20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridlayout.addItem(spaceritem, 1, 0, 1, 1)

        self.horizontallayout = QHBoxLayout()
        self.gridlayout.addLayout(self.horizontallayout, 1, 1, 1, 1)
        spaceritem2 = QSpacerItem(260, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridlayout.addItem(spaceritem2, 1, 2, 1, 1)
        self.svgWidget.setFixedSize(900, 700)

        # spaceritem1 = QSpacerItem(18, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # self.horizontallayout.addItem(spaceritem1)

        self.btn_save_png = QPushButton('Save as PNG', self.svgWidget)
        self.btn_save_png.setToolTip('Saves 2D Image as PNG')
        self.btn_save_png.resize(self.btn_save_png.sizeHint())
        self.btn_save_svg = QPushButton('Save as SVG', self.svgWidget)
        self.btn_save_svg.setToolTip('Saves 2D Image as SVG')
        self.btn_save_svg.resize(self.btn_save_svg.sizeHint())

        self.horizontallayout.addWidget(self.btn_save_png)
        self.horizontallayout.addWidget(self.btn_save_svg)

        myfont = QFont()
        myfont.setBold(True)
        myfont.setPointSize(10)
        myfont.setFamily("Arial")
        self.btn_save_png.setFont(myfont)
        self.btn_save_svg.setFont(myfont)
        self.svgWidget.setWindowTitle('2D View')
        self.svgWidget.show()

        self.btn_save_png.clicked.connect(lambda: self.save_2d_image_png_names(view))
        self.btn_save_svg.clicked.connect(lambda: self.save_2d_image_svg_names(view))

    def save_2d_image_png_names(self, view):
        #         view = self.go_to_open_svg(view)
        # self.btn_save.clicked.connect(view)

        if view == "Front":

            png_image_path = self.folder + "/images_html/endFront.png"
            options = QFileDialog.Options()
            file_tup = QFileDialog.getSaveFileName(None, "Save File As", self.folder + "/", "PNG (*.png)",options=options)
            file_name = str(file_tup[0])
            shutil.copyfile(png_image_path, file_name)


            png_image_path = self.folder + "/images_html/endFront.png"
            shutil.copyfile(png_image_path, str(QFileDialog.getSaveFileName(None, "Save File As", self.folder + "/", "PNG (*.png)")))
        elif view == "Side":
            png_image_path = self.folder + "/images_html/endSide.png"
            shutil.copyfile(png_image_path, str(QFileDialog.getSaveFileName(None, "Save File As", self.folder + "/", "PNG (*.png)")))
        else:
            png_image_path = self.folder + "/images_html/endTop.png"
            shutil.copyfile(png_image_path, str(QFileDialog.getSaveFileName(None, "Save File As", self.folder + "/", "PNG (*.png)")))

        QMessageBox.about(None, 'Information', "Image Saved")

    def save_2d_image_svg_names(self, view):
        #         view = self.go_to_open_svg(view)
        # self.btn_save.clicked.connect(view)

        if view == "Front":
            png_image_path = self.folder + "/images_html/endFront.svg"
            shutil.copyfile(png_image_path, str(QFileDialog.getSaveFileName(None, "Save File As", self.folder + "/", "SVG (*.svg)")))
        elif view == "Side":
            png_image_path = self.folder + "/images_html/endSide.svg"
            shutil.copyfile(png_image_path, str(QFileDialog.getSaveFileName(None, "Save File As", self.folder + "/", "SVG (*.svg)")))
        else:
            png_image_path = self.folder + "/images_html/endTop.svg"
            shutil.copyfile(png_image_path, str(QFileDialog.getSaveFileName(None, "Save File As", self.folder + "/", "SVG (*.svg)")))

        QMessageBox.about(None, 'Information', "Image Saved")


def main():
    app = QApplication(sys.argv)
    ex = SvgWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
