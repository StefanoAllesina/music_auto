from tkinter import *

"""
This uses the python GUI tkinter to draw rectangles. 
The class Rectangle makes a rectangle. If the rectangle is RIGHT clicked,
the user can then LEFT click, and drag to make a new rectangle. 
"""
class Rectangle():

	def __init__(self, masterWidget, canvas, x0, y0, x1, y1):
		"""
    	input: (x0, y0, x1, y1)
    	x0,y0 is the top left coordinate of the rectangle.
    	x1,y1 is the bottom right coordinate of the rectangle
    	"""
		self.masterWidget = masterWidget
		self.canvas = canvas

		#coordinates of rectangles
		self.x0 = x0
		self.y0 = y0
		self.x1 = x1
		self.y1 = y1

		#coordinate of temp rectangle that appears as you're dragging it
		self.tempX0, self.tempX1, self.tempY0, self.tempY1 = None, None, None, None
		self.tempRect = None

		self.rect = self.canvas.create_rectangle(self.x0,self.y0,self.x1,self.y1, fill ="blue")
		
		self.canvas.tag_bind(self.rect,"<Button-2>", self.select) 
		#weird- according to doc, button3 is the right click.
		#but on my laptop, button2 is the right click. 

	#when you right click (or middle click?) the middle of the rectangle
	def select(self, event):			
		self.canvas.bind("<Button-1>", self.clickTLRectangle)
		self.canvas.bind("<ButtonRelease-1>", self.releaseBTRectangle)
		self.canvas.tag_unbind("<Button-2>", self.rect)

	#top left of new rectangle, creates temporary rectangle as well
	def clickTLRectangle(self, event):
		self.x0 = event.x
		self.y0 = event.y
		self.canvas.bind("<B1-Motion>", self.drawTempRect)
		self.tempRect = self.canvas.create_rectangle(self.x0,self.y0,self.x0,self.y0, fill ="yellow")

	#bottom right of new rectangle, deletes temporary rectangle
	def releaseBTRectangle(self,event):
		self.x1 = event.x
		self.y1 = event.y

		#delete temp rectangle, and change coords of origin rectangle to match it
		self.canvas.delete(self.tempRect)
		self.canvas.coords(self.rect, self.x0, self.y0, self.x1, self.y1)

		#return to status quo
		self.canvas.tag_bind(self.rect,"<Button-2>", self.select)
		self.canvas.unbind("<Button-1>")
		self.canvas.unbind("<ButtonRelease-1>")
		self.canvas.unbind("<B1-Motion>") 

	#draws the temporary rectangle as you're dragging it 
	def drawTempRect(self, event):
		self.canvas.coords(self.tempRect, self.x0, self.y0, event.x, event.y)

#main widget window that appears
window = Tk()
window.geometry("500x500")

#make canvas to draw rectangles on
canvas = Canvas(window, width = 500, height = 500, background = "green")
canvas.pack()
#make rectangle
x0, y0, x1, y1 = 10, 10, 100, 100
drawRectangle = Rectangle(window, canvas, x0, y0, x1, y1)

#for future reference, if the rectangle is made too small, it might be hard to click within it to redraw rectangle
# one option is to only change rectangle dimensions if it meets a minimum area
# also, canvas has function find_closest() that will return the closest canvas object. This
# could be good when there are multiple rectangles


window.mainloop()


