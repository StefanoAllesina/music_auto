
$(document).ready(function() {
    
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
                    var box = new Box(i, data[i].box_id, data[i].page, data[i].line, data[i].x, data[i].y, data[i].w, data[i].h);
                    boxes.push(box);
                }
                var s = Snap("#something");
                var project = new Project(s, name, boxes, numPages);
                var pageSwitcher = new PageSwitcher(project.numPages, project.showPage);
                project.showPage(1);
                pageSwitcher.setPage(1);
            }
        });
    });
    
});