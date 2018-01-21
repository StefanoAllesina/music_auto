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