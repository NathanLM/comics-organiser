# Comics Organiser
Comics organiser is a command line tool. It automatically organises digital comics in a given directory.  
They are renamed and moved according to a set of rules.

## Requirements
Python 2.7+ (could be changed to any higher python release, like Python 3.3)

## Usage:

`organise [-real] [-quiet] [-source path/to/comics] [-rules path/to/rulefile] [-log path/to/logfile] path/to/destination/directory`

options:

* `-real`    really perform the operations. By default operations are just simulated and logged.  

* `-log`     the path and name of the log file. Default value is comicsorganiser.log  

* `-source`  the path of the directory in which the comics to be organised are located. When this option is not provided, the current directory is used.  

* `-rules`   the path and name of the file containing the rules to be applied. When this options is not provided the rules are loaded from the default rule file. 
If this file is not found the execution stops.  

* `-quiet`    disables the output of the logs on the command line. By default all operations are displayed on screen.  

## Examples:

`organise /usr/me/documents/comics`

Simulates the renaming and moving of files from the current directory to /usr/me/documents/comics.  
The operations are not performed, they are just displayed on the command line and logged in the current directory, 
in a file named comicsorganiser.log. The log lines starts with [simulation].  
The log lines are displayed on screen.  
The default ruleset is used.  

`organise -rules /usr/me/documents/comics/rules.json usr/me/documents/comics`

Same as above, except the rules to be used are defined in a file named rules.json and located in the current directory.


`organise -real -source /user/me/downloads/comics -quiet -log comics.log /usr/me/documents/comics/sorted`

Renames and moves comics from the directory /user/me/downloads/comics according to the default rules.  
All movings and renamings are logged in the current directory, in a file name comics.log.  
If this file exists, the new log lines are appended at the end of the file. Otherwise, the file is created.  
The log lines are not displayed on screen. Only error messages and end of operation message are.

##Rules:
The rules are stored in a [json](http://json.org) file.

They are two types of rules:
* file moving rules
* file renaming rules

### Moving rules
The rules are processed in the order their appear in the rule file. As soon as a rule may be applied to the current file, the remaining rules are ignored.

Example: 
* move all files containing "SpiderMan" in their name to the subdirectory "FR/Marvel/Spiderman" of the destination folder.
* move files containing "Héritage" and "Iron-Man" in their name to the subdirectory "FR/Héritage/IronMan" of the destination folder. 

```
"move": [
    { "SpiderMan" : "FR/Marvel/Spiderman"} ,
    "Héritage && Iron-Man" : "FR/Héritage/IronMan"
    }
]
```

### Renaming rules

All rules are applied.

Examples:

* Replace .zip extensions with .cbz and .rar extensions with .cbr :

```
"replace-extension": [
    { "zip": "cbz" },
    { "rar": "cbr" }
]
```
* Replace "SpiderMan" with "Spider-Man" in the file name:

```
"replace-": [
    { "SpiderMan": "Spider-Man" }
]
```

* Removes [Comics.fr], [Comics FR] and all their case variants:

```
"remove": [
    "[Comics.fr]",
    "[Comics FR]"
]
```
#### Sample rule file

```
"move": [
    { "SpiderMan" : "FR/Marvel/Spiderman"} ,
    "Héritage && Iron-Man" : "FR/Héritage/IronMan"
    }
],
"replace-extension": [
    { "zip": "cbz" },
    { "rar": "cbr" }
],
"remove": [
    "[Comics.fr]",
    "[Comics FR]"
]
```






