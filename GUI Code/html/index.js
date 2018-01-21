var express = require('express');
var app = express();
var path = require('path');
var fs = require('fs');
var csv = require('csv-parse');

// 
app.use('/scores', express.static(__dirname + '/scores/'));
app.use('/', express.static(__dirname + '/static/'));

app.get('/hello', function(req, res) {
    res.send('hello');
});

app.get('/fixBoxes', function(req, res) {
    var project = req.query.project;
    console.log(project);
});

app.get('/boxes', function(req, res) {
    var name = req.query.name;
});

app.get('/page', function(req, res) {
    var name = req.query.name;
    var pageNum = req.query.pageNum;
    console.log(req.query);
    fs.readFile('scores/Beethoven5/data/boxes.csv', function(err, data) {
        if(err) {
            console.log(err);
        } else {
            csv(data, {columns:true}, function(error, rows) {
                if(error) {
                    console.log(error);
                } else {
                    console.log(rows);
                    var data = {
                        file: '/scores/Beethoven5/content/pg_0002.jpg',
                        boxes: rows
                    };
                    res.set('Content-Type', 'application/json').send(data);
                }
            });
        }
    });
/*     var data = {
        file: __dirname + '/scores/Beethoven5/content/pg_0002.jpg',
        boxes: 'stuff'
    };
    res.send(__dirname + '/scores/Beethoven5/content/pg_0002.jpg'); */
});

app.get('/projects', function(req, res) {
    fs.readdir('scores', function(err, files) {
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