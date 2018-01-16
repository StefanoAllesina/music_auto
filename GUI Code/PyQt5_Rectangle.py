import os
import sys
from PyQt5 import QtGui, QtCore 
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QBrush
from PyQt5.QtCore import Qt
#import PyQt5
from PyQt5.QtWidgets import *

"""
This uses the python GUI PyQt5
The class Rectangle makes a rectangle. If the rectangle is clicked, it turns blue.
The user can then click and drag to make a new rectangle.
If the new rectangle is too small (area <500), the original rectangle is returned. 
"""

#make a rectangle widget
class Rectangle(QWidget):
    """
    input: (x0, y0, x1, y1)
    x0,y0 is the top left coordinate of the rectangle.
    x1,y1 is the bottom right coordinate of the rectangle
    """
    def __init__(self, x0, y0, x1,y1):
        super().__init__()
        # temp rectangle that is drawn when you're dragging
        self.tempBegin = QtCore.QPoint()
        self.tempEnd = QtCore.QPoint()

        #coordinates of actual rectangle 
        self.topLeft = QtCore.QPoint(x0,y0)
        self.bottomRight = QtCore.QPoint(x1,y1)
        self.rectangle = QtCore.QRect(self.topLeft, self.bottomRight)
        self.tempCoord = self.bottomRight 
        #temporary variable in case new rectangle is too small, and old rectangle is kept.
        self.click = 0
        self.show()
 
    def paintEvent(self, event):
        #make QPainter objects
        qp = QtGui.QPainter(self)
        brush = QtGui.QBrush(QtGui.QColor(100, 10, 10, 40))  
        qp.setBrush(brush)
        #draw temp Rectangle that appears when you're dragging the mouse   
        qp.drawRect(QtCore.QRect(self.tempBegin, self.tempEnd))


        #if the rectangle has been clicked, turn it blue 
        if self.click == 1: 
            brush = QtGui.QBrush(QtGui.QColor(0,0,255,127))
        else:
            brush = QtGui.QBrush(Qt.DiagCrossPattern) 
        qp.setBrush(brush)


        #draw rectangle
        if self.topLeft != None and self.bottomRight != None:   
            qp.drawRect(self.rectangle)
        
    def mousePressEvent(self, event):
        self.tempBegin = event.pos()
        self.tempEnd = event.pos()

        #Step 1: after clicking within the rectangle, the next click redefines the TopLeft coordinate. 
        if self.click ==1:
            self.topLeft = event.pos()
            self.bottomRight = None
            self.update()
            self.click = 2

        #Step 0:only initiate the clicking process when the mouse clicks within the rectangle
        if self.rectangle.contains(event.pos()) and self.click == 0:
            self.click = 1
            self.update()

    #for drawing the temp rectangle as you're dragging the mouse
    def mouseMoveEvent(self, event):
        #Step 3: mouse is being dragged. Updates temp rectangle.
        if self.click == 2:
            self.tempEnd = event.pos()
            self.update()

    #Step 4: Mouse has been released. 
    def mouseReleaseEvent(self, event):
        
        if self.click == 2:
            #essentially makes temp rectangle disappear
            self.tempBegin = event.pos()
            self.tempEnd = event.pos()


            if self.bottomRight == None:
                deltaY = abs(event.pos().y() - self.topLeft.y())
                deltaX = abs(event.pos().x() - self.topLeft.x())

                #this is so a minimum sized rectangle is created.
                # prevents a user making a tiny rectangle where it's impossible to click again
                #if a too small rectangle is created, the original rectangle is returned. 
                if deltaY * deltaX >= 500:
                    self.bottomRight = event.pos()
                    self.tempCoord = self.bottomRight
                    self.rectangle = QtCore.QRect(self.topLeft, self.bottomRight)
                else:
                    print('rectangle too small')
                    self.bottomRight = self.tempCoord
            
            self.click = 0 #resets back to step 0
            self.update()

if __name__ == '__main__':
   app = QApplication(sys.argv)
   x0, y0, x1, y1 = 10, 10, 100, 100
   a = Rectangle(x0, y0, x1, y1)

   sys.exit(app.exec_())
