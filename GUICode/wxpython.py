import wx

class MyPanel(wx.Panel):
    """ class MyPanel creates a panel to draw on, inherits wx.Panel """
    def __init__(self, parent, id):
        # create a panel
        wx.Panel.__init__(self, parent, id)
        self.SetBackgroundColour("white")
        self.InitRect()

    def InitRect(self):
        """set up the device context (DC) for painting"""
        self.dc = wx.ClientDC(self)
     #   self.dc.BeginDrawing()
      #  self.dc.SetPen(wx.Pen("grey",style=wx.TRANSPARENT))
      #  self.dc.SetBrush(wx.Brush("grey", wx.SOLID))
        # set x, y, w, h for rectangle
        self.dc.SetPen(wx.Pen("grey"))
        self.dc.SetBrush(wx.Brush("grey", wx.SOLID))
        self.dc.DrawRectangle(250,250,50, 50)
       # self.dc.EndDrawing()
        del self.dc

class Example(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)

        self.InitUI()
    
    def InitUI(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)

        self.SetSize((800,800))
        self.SetTitle('Simple menu')
        self.Centre()
        self.Show(True)
        MyPanel(self,1)
    def OnQuit(self, e):
        self.Close()

def main():
    ex = wx.App()
    Example(None)
    ex.MainLoop()

if __name__ == '__main__':
    main()