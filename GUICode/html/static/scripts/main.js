
$(document).ready(function() {
    
    $.ajax({
        method: 'GET',
        success: function(data) {
            var list = '';
            for(var i = 0; i < data.length; i++) {
                list += `<a class="dropdown-item project" href = "#" >${data[i]}</a >`;
            }
            document.getElementById('projects').innerHTML = list;
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
                for(var i in data) {
                    var box = new Box(i, data[i].box_id, data[i].page, data[i].line, data[i].x, data[i].y, data[i].w, data[i].h);
                    boxes.push(box);
                }
                var s = Snap("#something");
                var project = new Project(s, name, boxes);
                project.showPage(2);
            }
        });
    });
    
});