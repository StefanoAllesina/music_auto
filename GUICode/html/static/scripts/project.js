function Project(svg, projectName, boxes, numPages) {
    this.svg = svg;
    this.currentPage = 0;
    this.boxes = boxes;
    this.currentBoxes = [];
    this.selectedBox = -1;
    var self = this;
    this.numPages = numPages;
    window.onkeyup = function(e) {
        var key = e.keyCode ? e.keyCode : e.which;
        if (key == 8 && self.selectedBox != -1) {
            if(self.boxes[self.selectedBox].selected) {
                self.boxes.splice(self.selectedBox, 1);
                for (var i = 0; i < self.boxes.length; i++) {
                    self.boxes[i].index = i;
                }
                self.selectedBox = -1;
                self.showPage(self.currentPage);
            }
        }
    }
    this.showBoxes = function () {
        self.currentBoxes = self.boxes.filter(function (item) { return item.pageNum == self.currentPage; });
        for (var i in self.currentBoxes) {
            self.currentBoxes[i].show(self.svg, self.clickBox);
        }
    }
    this.showPage = function(number) {
        self.currentPage = number;
        self.svg.clear();
        self.svg.image(`${projectName}/pages/${self.currentPage}`);
        self.showBoxes();
    }
    this.clickBox = function (evt) {
        var index = this.data("index");
        var box = self.boxes[index];
        if (self.selectedBox == index && self.boxes[self.selectedBox].selected == true) {
            splitBox(this, evt);
        } else {
            
            box.selected = true;
            if (self.selectedBox != -1) {
                self.boxes[self.selectedBox].selected = false;
            }
            self.selectedBox = index;
            self.showPage(self.currentPage);
        }
        
        
    }
    function splitBox(rect, evt) {
        var index = rect.data("index");
      //  var index = self.boxes.map(function (e) { return e.boxID; }).indexOf(boxID);
        var box = self.boxes[index];
        console.log(box);
        var point = getCursorPt(evt.clientX, evt.clientY);
        var oldWidth = point.x - box.x;
        var newWidth = box.w - oldWidth;
        var newBox = new Box(index, '', box.pageNum, box.lineNum, point.x, box.y, newWidth, box.h);
        box.w = oldWidth;
        self.boxes.splice(index+1, 0, newBox);
        for(var i = 0; i < self.boxes.length; i++) {
            self.boxes[i].index = i;
        }
        self.showPage(self.currentPage);
    }
}