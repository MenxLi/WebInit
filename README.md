# WebInit
Initiate the working directory to contain html, css and javascript files based on template.

The template file and can be found and modified in "webInitTemplate" folder.

## Usage
```
➜ webinit -h
usage: webinit [-h] [--asset] [-c CSS_FNAME] [-j JS_FNAME] name

Init a directory to be webpage.

positional arguments:
  name                  Name of the main html file.

  optional arguments:
    -h, --help            show this help message and exit
    --asset               Use asset directory.
    -c CSS_FNAME, --css_fname CSS_FNAME
                          CSS file name, set to "None" to not creating css file.
    -j JS_FNAME, --js_fname JS_FNAME
                          JavaScript file name, set to "None" to not creating javascript file.

```

Examples:
First make a soft link to make the script included in the $PATH.
```
sudo chmod a+x ./webInit.py
sudo ln -s /usr/bin/webinit ./webInit.py
```
Use:
```
webinit index                   # Create index.html style.css and script.js in the working directory
webinit index.html              # Same as above
webinit main -j app             # Create main.html style.css and app.js in the working directory
webinit index --asset           # Create assets folder and put css and js file into it
```
