function Box(boxID, pageNum, lineNum, x, y, w, h) {
    this.boxID = boxID;
    this.lineNum = lineNum;
    this.pageNum = pageNum;
    this.x = x;
    this.y = y;
    this.w = w;
    this.h = h;
    this.rect = {};
    this.dragging = 0;
    this.handleGroup1;
    this.handleGroup2;
    var self = this;
    this.move1 = function(dx, dy, x, y) {
        var svg = document.getElementsByTagName("svg")[0];
        console.log(this.attr("x"));
        svg = document.querySelector('svg');
        var pt = svg.createSVGPoint();
        pt.x = x;
        pt.y = y;
        var cursorpt = pt.matrixTransform(svg.getScreenCTM().inverse());
        var thisX = new Number(this[0].attr("x"));
        var thisY = new Number(this[0].attr("y"));
        var height = new Number(this[0].attr("height"));
        var width = new Number(this[0].attr("width"));
        height = height + thisY - cursorpt.y;
        width = width + thisX - cursorpt.x;
        this[0].attr({
            x:cursorpt.x,
            y:cursorpt.y,
            height: height,
            width: width
        });
        this[1].attr({
            cx:cursorpt.x,
            cy:cursorpt.y
        });
    }
    this.move2 = function (dx, dy, x, y) {
        var svg = document.getElementsByTagName("svg")[0];
        svg = document.querySelector('svg');
        var pt = svg.createSVGPoint();
        pt.x = x;
        pt.y = y;
        var cursorpt = pt.matrixTransform(svg.getScreenCTM().inverse());
        var thisX = new Number(this[0].attr("x"));
        var thisY = new Number(this[0].attr("y"));
        var height = new Number(this[0].attr("height"));
        var width = new Number(this[0].attr("width"));
        height = cursorpt.y - thisY;
        width = cursorpt.x - thisX;
        this[0].attr({
            height: height,
            width: width
        });
        this[1].attr({
            cx: cursorpt.x,
            cy: cursorpt.y
        });
    }
    this.show = function(svg) {
        this.rect = svg.rect(this.x, this.y, this.w, this.h);
        var bb = this.rect.getBBox();
        var handle = new Array();
        handle[0] = svg.circle(bb.x, bb.y, 20).attr({ class: 'handler' });
        handle[1] = svg.circle(bb.x + bb.width, bb.y + bb.height, 20).attr({ class: 'handler' });
        this.handleGroup1 = svg.group(this.rect, handle[0]);
        this.handleGroup1.drag(this.move1, null, this.stop);
        this.handleGroup2 = svg.group(this.rect, handle[1]);
        this.handleGroup2.drag(this.move2, null, this.stop);
    }
    this.stop = function() {
        var x = this[0].attr("x");
        var y = this[0].attr("y");
        var width = this[0].attr("width");
        var height = this[0].attr("height");
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
    this.showPage = function(number) {
        this.currentPage = number;
        svg.image(`${projectName}/pages/${number}`);
        this.currentBoxes = this.boxes.filter(function(item) {return item.pageNum == number;});
        for(var i in this.currentBoxes) {
            this.currentBoxes[i].show(svg);
        }
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