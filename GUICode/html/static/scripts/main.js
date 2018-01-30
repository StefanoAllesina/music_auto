function getCursorPt(x, y) {
    var svg = document.getElementsByTagName("svg")[0];
    svg = document.querySelector('svg');
    var pt = svg.createSVGPoint();
    pt.x = x;
    pt.y = y;
    var cursorpt = pt.matrixTransform(svg.getScreenCTM().inverse());
    return cursorpt;
}
function Box(boxID, pageNum, lineNum, x, y, w, h) {
    this.boxID = boxID;
    this.lineNum = lineNum;
    this.pageNum = pageNum;
    this.x = new Number(x);
    this.y = new Number(y);
    this.w = new Number(w);
    this.h = new Number(h);
    this.rect = {};
    this.dragging = 0;
    this.handleGroup1;
    this.handleGroup2;
    this.handle = new Array();
    var self = this;
    this.move1 = function(dx, dy, x, y) {
        var cursorpt = getCursorPt(x, y);
        var thisX = new Number(self.rect.attr("x"));
        var thisY = new Number(self.rect.attr("y"));
        var height = new Number(self.rect.attr("height"));
        var width = new Number(self.rect.attr("width"));
        height = height + thisY - cursorpt.y;
        width = width + thisX - cursorpt.x;
        self.rect.attr({
            x:cursorpt.x,
            y:cursorpt.y,
            height: height,
            width: width
        });
        self.handle[0].attr({
            cx:cursorpt.x,
            cy:cursorpt.y
        });
    }
    this.move2 = function (dx, dy, x, y) {
        var cursorpt = getCursorPt(x,y);
        var thisX = new Number(self.rect.attr("x"));
        var thisY = new Number(self.rect.attr("y"));
        var height = new Number(self.rect.attr("height"));
        var width = new Number(self.rect.attr("width"));
        height = cursorpt.y - thisY;
        width = cursorpt.x - thisX;
        self.rect.attr({
            height: height,
            width: width
        });
        self.handle[1].attr({
            cx: cursorpt.x,
            cy: cursorpt.y
        });
    }
    this.show = function(svg, clickHandle) {
        this.rect = svg.rect(this.x, this.y, this.w, this.h);
        this.rect.click(clickHandle);
        this.rect.data("boxID", self.boxID);
        var bb = this.rect.getBBox();
        this.handle[0] = svg.circle(bb.x, bb.y, 20).attr({ class: 'handler' });
        this.handle[1] = svg.circle(bb.x + bb.width, bb.y + bb.height, 20).attr({ class: 'handler' });
        this.handle[0].drag(this.move1, null, this.stop);
        this.handle[1].drag(this.move2, null, this.stop);
    }
    this.stop = function() {
        var x = self.rect.attr("x");
        var y = self.rect.attr("y");
        var width = self.rect.attr("width");
        var height = self.rect.attr("height");
        self.x = x;
        self.y = y;
        self.width = width;
        self.height = height;
    }
}
function Project(svg, projectName, boxes) {
    this.svg = svg;
    this.currentPage = 0;
    this.boxes = boxes;
    this.currentBoxes = [];
    var self = this;
    this.showBoxes = function() {
        self.currentBoxes = self.boxes.filter(function (item) { return item.pageNum == self.currentPage; });
        for (var i in self.currentBoxes) {
            self.currentBoxes[i].show(self.svg, self.clickBox);
        }
    }
    this.showPage = function(number) {
        self.currentPage = number;
        self.svg.clear();
        self.svg.image(`${projectName}/pages/${number}`);
        self.showBoxes();
    }
    this.clickBox = function(evt) {
        splitBox(this, evt);
    }
    function splitBox(rect, evt) {
        var boxID = rect.data("boxID");
        var index = self.boxes.map(function (e) { return e.boxID; }).indexOf(boxID);
        var box = self.boxes[index];
        var point = getCursorPt(evt.x, evt.y);
        var oldWidth = point.x - box.x;
        var newWidth = box.w - oldWidth;
        var newBox = new Box('', box.pageNum, box.lineNum, point.x, box.y, newWidth, box.h);
        box.w = oldWidth;
        self.boxes.splice(index, 0, newBox);
        self.showPage(self.currentPage);
    }
}
$(document).ready(function() {
    
    $.ajax({
        method: 'GET',
        success: function(data) {
            var table = '<table><tr><th>Project</th></tr>';
            for(var i = 0; i < data.length; i++) {
                table += `<tr><td class="score">${data[i]}</td></tr>`
            }
            table += '</table>';
            document.getElementById('table').innerHTML = table;
        },
        error: function(error) {
            console.log(error);
            window.alert(error);
        },
        url: '/projects'
    });
    $("#table").on('click', '.score', function(event) {
        var name = $(event.target).text();
        console.log(name);
        var url = `/${name}/boxes`;
        $.ajax({
            url: url,
            method: 'GET',
            success: function(data) {
                var boxes = [];
                console.log(data);
                for(var i in data) {
                    var box = new Box(data[i].box_id, data[i].page, data[i].line, data[i].x, data[i].y, data[i].w, data[i].h);
                    boxes.push(box);
                }
                var s = Snap("#something");
                var project = new Project(s, name, boxes);
                project.showPage(2);
            }
        });
    });
    
});