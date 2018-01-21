var express = require('express');
var app = express();
var path = require('path');

// 
app.use('/', express.static(__dirname + '/static/'));

app.get('/hello', function(req, res) {
    res.send('hello');
});


app.listen(3000);