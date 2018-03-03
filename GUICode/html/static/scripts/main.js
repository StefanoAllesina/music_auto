
$(document).ready(function() {
    var project;
    $.ajax({
        method: 'GET',
        success: function(data) {
            addProjectsToNavBar(data);
        },
        error: function(error) {
            console.log(error);
            window.alert(error);
        },
        url: '/projects'
    });
    $("#projects").on('click', '.project', function(event) {
        var name = $(event.target).text();
        console.log(name);
        var url = `/${name}/boxes`;
        $.ajax({
            url: url,
            method: 'GET',
            success: function(data) {
                var boxes = [];
                console.log(data);
                var numPages = 0;
                for(var i in data) {
                    if(data[i].page > numPages) {
                        numPages = data[i].page;
                    }
                    var box = new Box(i, i, data[i].page, data[i].line, data[i].x, data[i].y, data[i].w, data[i].h);
                    boxes.push(box);
                }
                var s = Snap("#something");
                project = new Project(s, name, boxes, numPages);
                var pageSwitcher = new PageSwitcher(project.numPages, project.showPage);
                project.showPage(1);
                pageSwitcher.setPage(1);
            }
        });
    });
    $("#doneButton").click(function() {
        var boxes = project.getFinalBoxes();
        var finalBoxes = [];
        for(var i in boxes) {
            finalBoxes.push(boxes[i].toJSON());
        }
        var data = {
            boxes:finalBoxes,
            repeats:project.repeats
        };
        console.log(finalBoxes);
        var url = `/${project.projectName}/boxes`;
        $.ajax({
            url: url,
            method: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function(data) {
                console.log(data);
            }
        });
    });
    $("#toolbar").on('click', '.nav-link', function(event) {
        var item = $(event.target).text();
        if($(event.target).hasClass("disabled")) {
            return;
        }
        console.log(item);
        $("#toolbar").find(".nav-link").removeClass("active");
        $("#toolbar").find(".nav-link").addClass("disabled");
        $(event.target).addClass("active");
        if(item == "Add Repeat") {
            showAlert("<strong>Add Repeat</strong> Click to select start of repeat");
            project.editMode = 'repeat';
        } else if(item == "Add Da Capo") {
            showAlert("<strong>Add Da Capo</strong> Click to select Fine");
        } else if(item == "Add Dal Segno") {
            showAlert("<strong>Add Dal Segno</strong> Click to select D.S");
        } else if(item == "Split Box") {
            showAlert("<strong>Split Box</strong> Click in box to split");
            project.editMode = 'split';
        }
        project.unselectBox();
    });
    function split(evt) {
        var index = this.data("index");
        var box = self.boxes[index];
        var index = rect.data("index");
        //  var index = self.boxes.map(function (e) { return e.boxID; }).indexOf(boxID);
        var box = self.boxes[index];
        console.log(box);
        var point = getCursorPt(evt.clientX, evt.clientY);
        var oldWidth = point.x - box.x;
        var newWidth = box.w - oldWidth;
        var newBox = new Box(index, '', box.pageNum, box.lineNum, point.x, box.y, newWidth, box.h);
        box.w = oldWidth;
        self.boxes.splice(index + 1, 0, newBox);
        for (var i = 0; i < self.boxes.length; i++) {
            self.boxes[i].index = i;
        }
        self.showPage(self.currentPage);
    }
    function addRepeat() {
        

    }
    function clickBox(evt, box) {
        box.selected = true;
        if (self.selectedBox != -1) {
            self.boxes[self.selectedBox].selected = false;
        }
        self.selectedBox = index;
        self.showPage(self.currentPage);
    }
    function finishEdit() {
        project.clickBox = clickBox;
    }
});
