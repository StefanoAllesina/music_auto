var express = require('express');
var app = express();
var path = require('path');
var fs = require('fs');
var csv = require('csv');

var PROJECT_DIR = process.argv[2];
app.use('/', express.static(__dirname + '/static/'));
app.use(express.json());

app.get('/:project/pages', function(req, res) {
    var project = req.params.project;
    fs.readdir(path.join(PROJECT_DIR, project, 'pages'), function(err, pages) {
        if(err) {
            console.log(err);
        } else {
            res.set('Content-Type', 'application/json').send(JSON.stringify(pages));
        }
    });
});
app.get('/:project/pages/:page', function(req, res) {
    var project = req.params.project;
    var page = req.params.page;
    fs.createReadStream(path.join(PROJECT_DIR, project, 'pages', page) + '.jpg').pipe(res);
});

app.get('/:project/boxes', function(req, res) {
    var project = req.params.project;
    fs.readFile(path.join(PROJECT_DIR, project, 'boxes.csv'), function(err, data) {
        if(err) {
            console.log(err);
        } else {
            csv.parse(data, {columns:true}, function(error, rows) {
                if(error) {
                    console.log(error);
                } else {
                    res.set('Content-Type', 'application/json').send(rows);
                }
            });
        }
    });
});
app.post('/:project/boxes', function(req, res) {
    var project = req.params.project;
    csv.stringify(req.body, {header:true}, function(err, data) {
        fs.writeFile(path.join(PROJECT_DIR, project, 'boxes.csv'), data, function(err) {
            if(err) {
                console.log(err);
            } else {
                res.send('success');
            }
        });
    });
});

app.get('/projects', function(req, res) {
    fs.readdir(PROJECT_DIR, function(err, files) {
        if(err) {
            console.log(err);
        } else {
            res.set('Content-Type', 'application/json').send(JSON.stringify(files));
        }
    });
});
app.listen(3000, function() {
    console.log('app is listening on port 3000');
});
