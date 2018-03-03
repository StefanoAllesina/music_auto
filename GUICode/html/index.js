var express = require('express');
var app = express();
var path = require('path');
var fs = require('fs');
var csv = require('csv');

var multer = require('multer');
var ejs = require('ejs');
var http = require("http");
var bodyParser = require('body-parser');
var rimraf = require('rimraf');
var copydir = require('copy-dir')
var mkdirp = require('mkdirp')




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
    var boxes = req.body.boxes;
    var repeats = req.body.repeats;
    console.log(boxes);
    console.log(repeats);
    res.send('success');
    /* csv.stringify(req.body, {header:true}, function(err, data) {
        fs.writeFile(path.join(PROJECT_DIR, project, 'boxes.csv'), data, function(err) {
            if(err) {
                console.log(err);
            } else {
                res.send('success');
            }
        });
    }); */
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

/********************************************************************/
//uploaded image will be stored in this file
var destinationPath = './public/original/';
//processed files are kept here
var processedPath = './public/';
//Storage engine

const Storage = multer.diskStorage({
    //sets the destination
    destination: destinationPath,
    //sets the filename of the uploaded thing
    filename: function(req, file, callback) {
        var ext = path.extname(file.originalname)

        callback(null, Date.now() + file.originalname) 
    }
    });

var upload = multer({
    storage: Storage
}).single('myImage');
//can do .array instead of .single for array of images


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
//child process
var pythonExecutable = "python";

//converts Uint8array to string
//https://ourcodeworld.com/articles/read/286/how-to-execute-a-python-script-and-retrieve-output-data-and-errors-in-node-js
var Uint8arrayToString = function(data){
    return String.fromCharCode.apply(null,data)
}


//EJS
app.set('view engine', 'ejs');

//public folder that will be static
app.use(express.static('./public'));

var filteredItems;

//finds all previous images that are in folder
fs.readdir(processedPath, function(err, items)
    {
        //Note: apple folders have a .DC_store in every folder
        filteredItems = items.filter( function(item){
            if (item !== 'original' && item !== '.DS_Store')
            {
                return item;
            }
        });
        filteredItems.sort();

    })


app.get('/upload',function(req,res){
    res.render('upload', {
        images: filteredItems
    });

})

app.post('/upload', (req,res) => {
    //if previous file is given 
    if (req.body.fileName != undefined)
    {
        console.log(req.body.fileName);

        res.render('upload', {
        msg: '',
        images: filteredItems,
        // file: `/processed/${req.body.fileName}`
        file: `/${req.body.fileName}`
    });
    }
    else

    //if a new file is uploaded
    {
    upload(req,res, (err) => {
        //if error
        if (err)
        {
            console.log('Error alert');
        }
        else {
            if (req.file != undefined)
            {

                // var html = buildHtml(req);   
                var data = req.file.filename + " " + req.body.projectname;
  
                var UniqueProjectName = true
                for (var i = 0; i < filteredItems.length; i++){
                    if (filteredItems[i] === req.body.projectname)
                    {
                        UniqueProjectName = false
                    }
                }

                if (UniqueProjectName == false)
                {
                    var render = res.render('upload', {
                        images: filteredItems,
                        msg: 'There is a previous project with that name'
                        });
                }
                else
                {
                filteredItems.push(req.body.projectname)
                const spawn = require('child_process').spawn;   
                const scriptExecution = spawn("python", ["combine.py"]);
                // const scriptExecution = spawn("python", ["helloworld.py"]);


                scriptExecution.stdout.on('data', (data) => {
                    console.log(String.fromCharCode.apply(null,data));
                });

                scriptExecution.stdin.write(data);
                scriptExecution.stdin.end();
                scriptExecution.on('exit', function(){
                    console.log('exited')
                    var path1 = `/${data}`

                    var render = res.render('upload',
                    {
                        images: filteredItems,
                        msg: 'File successfully uploaded',
                        file: path1
                    });
                });
            }
            }
        }
    }); //end of upload
    } //end of else
});


// Delete
app.get('/delete', (req, res) => {
    var render = res.render('delete', {
    images: filteredItems
    });

});

app.post('/delete', (req,res) => {

    del_path = "./public/" + req.body.fileName;
    rimraf(del_path, function () { console.log('file deleted'); });

    filteredItems = filteredItems.filter(function(item) { 
    return item !== req.body.fileName
})

    var render = res.render('delete', {
    images: filteredItems,
    msg: 'File deleted'
    });
});


app.get('/rename', (req, res) => {



    var render = res.render('rename', {
    images: filteredItems,
    msg: ""
    });

});

app.post('/rename', (req, res) =>{
    var newName = req.body.projectname;
    var oldName = req.body.fileName;

    var UniqueProjectName = true
    for (var i = 0; i < filteredItems.length; i++){
        if (filteredItems[i] === req.body.projectname)
        {
            UniqueProjectName = false
        }
    }

    if (UniqueProjectName == false)
    {
        var render = res.render('rename', {
            images: filteredItems,
            msg: 'There is a previous project with that name'
            });
    }
    else {

        oldDirectory = "./public/" + oldName + "/";
        newDirectory = "./public/" + newName + "/";
        fs.rename(oldDirectory, newDirectory, function(err) {
            if ( err ) console.log('ERROR: ' + err);
        });

        filteredItems.push(newName);
        filteredItems = filteredItems.filter(function(item) { 
            return item !== oldName
        });

        filteredItems.sort()

        var render = res.render('rename', {
            images: filteredItems,
            msg: ''
            });

    }

});


app.get('/duplicate', (req, res) => {



    var render = res.render('duplicate', {
    images: filteredItems,
    msg: ""
    });

});

app.post('/duplicate', (req, res) =>{
    console.log("post rename")
    console.log(req.body)

    var copyProject = req.body.projectname;
    var originalProject = req.body.fileName;

    var UniqueProjectName = true
    for (var i = 0; i < filteredItems.length; i++){
        if (filteredItems[i] === copyProject)
        {
            UniqueProjectName = false
        }
    }

    if (UniqueProjectName == false)
    {
        var render = res.render('duplicate', {
            images: filteredItems,
            msg: 'There is a previous project with that name'
            });
    }
    else {

        oldDirectory = "./public/" + originalProject + "/";
        newDirectory = "./public/" + copyProject + "/";

        copydir(oldDirectory, newDirectory,function(err){
              if(err){
                console.log('Error: ' + err);
              }
            });

        filteredItems.push(copyProject);
        filteredItems.sort();
        var render = res.render('duplicate', {
            images: filteredItems,
            msg: ''
            });

    }
});


app.listen(3000, function() {
    console.log('app is listening on port 3000');
});
