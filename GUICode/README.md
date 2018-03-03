# Using NodeJS

* We will be using NodeJS with Express.  
    * NodeJS Documentation: https://nodejs.org/docs/latest-v7.x/api/
    * ExpressJS documentation: https://expressjs.com/en/4x/api.html
        * You'll want to look at the Application, Request and Response sections of the documentation mostly.
        * Application is the primary part of express and is usually used like this:
        ```javascript
        // the way to include modules in nodejs
        // the convention is to name required items in camelCase
        var express = require('express');
        // creates a singleton instance of the app server
        // it is called app or server by convention
        var app = express();
        app.get('/path', function(request, response) {
            // do something with the request
            // do something with the response
            res.send('Hello World!');
        });
        app.listen(3000, function() {
            console.log('app is listening on port 3000');
        });
        ```
# Install NodeJS

### macOS

* Check if Node is already installed in your Terminal

    Node is Installed (skip to step 2):
    ```
    user$ node --version
    v6.11.2
    ```

    Node is not Installed (continue step 1):
    ```
    user$ node --version
    command not found
    ```
* Go to https://nodejs.org/en/download/ and follow the instructions to install NodeJS

    When you are done run the command above again:
    ```
    user$ node --version
    v6.11.2
    ```

### Linux

* Check if Node is already installed in your Terminal

    Node is Installed (skip to step 2):
    ```
    user$ nodejs --version
    v4.2.6
    ```

    Node is not Installed (continue step 1):
    ```
    user$ nodejs --version
    The program 'nodejs' is currently not installed. You can install it by typing: sudo apt install nodejs-legacy
    ```
* Install NodeJS using apt-get.

    ```
    user$ sudo apt-get update
    ...
    user$ sudo apt-get install nodejs npm -y
    ```

    When you are done run the command above again:
    ```
    user$ nodejs --version
    v4.2.6
    ```