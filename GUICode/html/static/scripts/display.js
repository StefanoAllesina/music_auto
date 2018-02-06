function PageSwitcher(numPages, switchFunc) {
    this.switchFunc = switchFunc;
    this.numPages = numPages;
    this.currentPage = 0;
    var self = this;
    var html = '<li id="previous" class="page-item"><a class="page-link" href="#">Previous</a></li>';
    for (var i = 1; i <= this.numPages; i++) {
        html += `<li class="page-item" id="page-${i}"><a class="page-link" href="#">${i}</a></li>`;
    }
    html += '<li id="next" class="page-item"><a class="page-link" href="#">Next</a></li>';
    document.getElementById('pageSwitcher').innerHTML = html;
    $("#pageSwitcher").on('click', '.page-link', function(event) {
        var button = $(event.target).text();
        var number = self.currentPage;
        if(button == 'Previous') {
            number -= 1;
        } else if(button == 'Next') {
            number += 1;
        } else {
            number = new Number(button);
        }
        self.setPage(number);
        self.switchFunc(number);
    });
    this.setPage = function(page) {
        if(page != this.currentPage) {
            $("#pageSwitcher").find(`#page-${this.currentPage}`).removeClass("active");
            $("#pageSwitcher").find(`#page-${page}`).addClass("active");
            if(page == 1) {
                $("#pageSwitcher").find("#previous").addClass("disabled");
            } else if(page == self.numPages) {
                $("#pageSwitcher").find("#next").addClass("disabled");
            } else {
                $("#pageSwitcher").find("#previous").removeClass("disabled");
                $("#pageSwitcher").find("#next").removeClass("disabled");
            }
            this.currentPage = page;
        }
    };
}

function addProjectsToNavBar(projectNameArray) {
    var list = '';
    for (var i = 0; i < projectNameArray.length; i++) {
        list += `<a class="dropdown-item project" href = "#" >${projectNameArray[i]}</a >`;
    }
    document.getElementById('projects').innerHTML = list;
}