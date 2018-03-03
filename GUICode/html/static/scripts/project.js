function Project(svg, projectName, boxes, numPages) {
    this.svg = svg;
    this.currentPage = 0;
    this.boxes = boxes;
    this.currentBoxes = [];
    this.selectedBox = -1;
    var self = this;
    this.editMode = '';
    this.numPages = numPages;
    this.projectName = projectName;
    this.repeats = [];
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
    this.showBoxes = function (handler) {
        self.currentBoxes = self.boxes.filter(function (item) { return item.pageNum == self.currentPage; });
        for (var i in self.currentBoxes) {
            var box = self.currentBoxes[i];
            box.show(self.svg, self.clickBox);
            if(!box.selected) {
                for (var j in self.repeats) {
                    if (self.repeats[j].start == self.currentBoxes[i].boxID) {
                        self.currentBoxes[i].showRepeatFront();
                    }
                    if(self.repeats[j].end == self.currentBoxes[i].boxID) {
                        self.currentBoxes[i].showRepeatEnd();
                    }
                }
            }
        }
    }
    this.showRepeats = function() {
        for(var i in self.currentBoxes) {
            
        }
    }
    this.showPage = function(number) {
        self.currentPage = number;
        self.svg.clear();
        self.svg.image(`${self.projectName}/pages/${self.currentPage}`);
        self.showBoxes();
    }
    this.clickBox = function (evt) {
        var index = this.data("index");
        var box = self.boxes[index];
        if(self.editMode == 'split') {
            splitBox(this, evt);
            self.showPage(self.currentPage);
            dismissAlert();
            $("#toolbar").find(".nav-link").removeClass("active");
            $("#toolbar").find(".nav-link").removeClass("disabled");
            self.editMode = '';
        } else if(self.editMode == 'repeat') {
            if(clickIsAtFrontOfBox(box, evt)) {
                box.showRepeatFront();
                self.repeats.push({start:box.boxID});
                showAlert("<strong>Add Repeat</strong> Click for the end of the repeat");
                self.editMode = 'repeat2';
            } else if(clickIsAtEndOfBox(box,evt)) {
                showAlert('<strong>Add Repeat</strong> You can\'t add opening to end of line');
            } else {
                var newBox = splitBox(this, evt);
                self.repeats.push({ start: newBox.boxID });
                self.showPage(self.currentPage);
                showAlert("<strong>Add Repeat</strong> Click for the end of the repeat");
                self.editMode = 'repeat2';
            }
        } else if(self.editMode == 'repeat2') {
            if(clickIsAtFrontOfBox(box, evt)) {
                showAlert('<strong>Add Repeat</strong> You can\'t add closing repeat to the start of a line');
            } else if(clickIsAtEndOfBox(box,evt)) {
                box.showRepeatEnd();
                self.repeats[self.repeats.length-1].end = box.boxID;
                dismissAlert();
                self.editMode = '';
                $("#toolbar").find(".nav-link").removeClass("active");
                $("#toolbar").find(".nav-link").removeClass("disabled");                
            } else {
                splitBox(this,evt);
                self.repeats[self.repeats.length-1].end = box.boxID;
                self.showPage(self.currentPage);
                dismissAlert();
                self.editMode = '';
                $("#toolbar").find(".nav-link").removeClass("active");
                $("#toolbar").find(".nav-link").removeClass("disabled");                
            }
        } else {
            self.unselectBox();
            box.selected = true;
            self.selectedBox = index;
            self.showPage(self.currentPage);
        }
        // if (self.selectedBox == index && self.boxes[self.selectedBox].selected == true) {
            
        // } else {


        // }
        
        
        
    }
    this.getFinalBoxes = function() {
        var repeatArray = [];
        for(var i in self.repeats) {
            for(var j in self.boxes) {
                if(self.boxes[j].boxID == self.repeats[i].start) {
                    repeatArray = [];
                    while(self.boxes[j].boxID != self.repeats[i].end) {
                        repeatArray.push(self.boxes[j]);
                        j++;
                    }
                    repeatArray.push(self.boxes[j]);
                    self.boxes.splice(j+1, 0, ...repeatArray);
                    break;
                }
            }
        }
        return self.boxes;
    }
    this.unselectBox = function() {
        if (self.selectedBox != -1) {
            self.boxes[self.selectedBox].selected = false;
            self.selectedBox = -1;
            self.showPage(self.currentPage);
        }
    }
    function clickIsAtFrontOfBox(box, evt) {
        var point = getCursorPt(evt.clientX, evt.clientY);
        if(Math.abs(point.x - box.x) < 50) {
            return true;
        }
        return false;
    }
    function clickIsAtEndOfBox(box, evt) {
        var point = getCursorPt(evt.clientX, evt.clientY);
        if(Math.abs(point.x - (box.x + box.w)) < 50) {
            return true;
        }
        return false;
    }
    function splitBox(rect, evt) {
        debugger;
        var index = rect.data("index");
      //  var index = self.boxes.map(function (e) { return e.boxID; }).indexOf(boxID);
        var box = self.boxes[index];
        console.log(box);
        var point = getCursorPt(evt.clientX, evt.clientY);
        var oldWidth = point.x - box.x;
        var newWidth = box.w - oldWidth;
        var newBox = new Box(index, self.boxes.length, box.pageNum, box.lineNum, point.x, box.y, newWidth, box.h);
        for(var i in self.repeats) {
            if(self.repeats[i].end == box.boxID) {
                self.repeats[i].end = newBox.boxID;
            }
        }
        box.w = oldWidth;
        self.boxes.splice(Number(index)+1, 0, newBox);
        for(var i = 0; i < self.boxes.length; i++) {
            self.boxes[i].index = i;
        }
        return newBox;
    }

}