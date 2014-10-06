#!/usr/bin/python
# -*- coding: utf-8 -*-
#coding: utf-8
# vim: expandtab sw=4 ts=4

import sys,os
from PyQt4 import QtGui,QtCore

class captchaDialog(QtGui.QWidget):
    def __init__(self, parent, imgPath):
        QtGui.QWidget.__init__(self, None)
        self.root = parent
        self.imgPath = imgPath
        self.value=""
        self.initUI()
        self.center()

    def getPixmapQt(self,path):
        u"""
        使用Qt的方法获取pixmap, 数字1为magic number，看文档这个是指定format的
        任何数字都会解码jpeg成功，否则解码jpeg失败
        @see http://stackoverflow.com/questions/16990914/python-pyqt-qpixmap-returns-null-for-a-valid-image
        """
        return QtGui.QPixmap(path,"1")

    def initUI(self):
        # 没有这行代码图片会花掉，不知道啥
        self.setGeometry(QtCore.QRect(50,50,240,160))

        layout = QtGui.QHBoxLayout(self)
        layout.setMargin(5)

        imgLabel = QtGui.QLabel('Text', self)
        img = self.getPixmapQt(self.imgPath)
        imgSize = img.size()
        magnify = 4
        imgLabel.setFixedSize(imgSize.width() * magnify, imgSize.height() * magnify)
        imgLabel.setPixmap(img.scaled(imgLabel.size(), QtCore.Qt.KeepAspectRatio))
        layout.addWidget(imgLabel)

        lineEdit = QtGui.QLineEdit(self)
        layout.addWidget(lineEdit)

        QtCore.QObject.connect(lineEdit, QtCore.SIGNAL("textChanged(QString)"),self.onTextChange)

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def center2(self):
        u"""
        只是另外一种使窗口居中的方法
        """
        size = self.size()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        self.move(centerPoint.x() - size.width() / 2, centerPoint.y() - size.height() / 2)

    def onTextChange(self, val):
        self.value=val
        if len(val) >= 4:
            self.close()
        return val

    def getSupportedFormats(self):
        return tuple(str(imgFormat) for imgFormat in QtGui.QImageReader.supportedImageFormats())

def show_captcha(captchaPath):
    root = QtGui.QApplication(sys.argv)
    d = captchaDialog(root, captchaPath)
    
    #激活窗口
    #@see http://stackoverflow.com/questions/12118939/how-to-make-a-pyqt4-window-jump-to-the-front
    d.setWindowTitle(u"速度输入验证码，不区分大小写")
    d.setWindowState(d.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
    d.activateWindow()

    d.show()
    root.exec_()
    return d.value

def main():
    a = show_captcha(os.path.join(os.getcwd(),"pass_code.jpeg"))
    print a

if __name__ == '__main__':
    main()
