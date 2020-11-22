# -*- coding: utf8 -*-

import sys
import argparse
import time
import os
import shutil
import json
import re
import string
from pprint import pprint

NEW_LINE = "\n                                      "
STOP = -1
modificationCount = 0

def log(message, quiet):
    ''' adds message to the log file '''
    now = time.strftime('%d/%m/%y %H:%M:%S', time.localtime())
    logfile = open("log.txt", "a")
    logfile.write(now + " : " + message + "\n\n")
    logfile.close()
    if quiet is False:
        try:
            # print(message.encode('cp437'))
            print(message.encode(sys.getfilesystemencoding()))
        except:
            pass
        print()

def move(filename, destination, real, quiet):
    '''moves a given file to the destination folder
       when real is true, the moving is performed; otherwise it is just simulated'''
    global modificationCount
    if real is True:
        try:
            if(os.path.isfile(destination)):
                log("MOVE ERROR: " +  destination + " ALREADY EXISTS", quiet)
                return None
            else:
                os.renames(encodeFilename(filename), encodeFilename(destination))
                log("MOVED " + str(filename) + NEW_LINE + "TO " + destination, quiet)
                modificationCount += 1
                return STOP
        except IOError as e:
            log("MOVE ERROR: " + str(e) + " - SOURCE: " + filename + " DESTINATION: " + destination, quiet)
            return None

    else:
        log("[SIMULATION] MOVED " + str(filename) + NEW_LINE + "TO: " + destination, quiet)
        return STOP


def rename(destination, oldName, newName, real, quiet):
    '''Renames a given file'''
    global modificationCount
    if real is True:
        try:
            if(os.path.isfile(newName)):
                # TODO add filename to destination
                filename = oldName[oldName.rfind(os.sep)+1:]
                log("DEBUG: oldName=" + oldName + ", filename= " + filename, quiet )
                log("DEBUG: destination=" + destination, quiet )
                move(oldName, os.path.join(destination, "duplicates", filename), real, quiet) 
                log("INFO: " + newName + " MOVED TO duplicates directory", quiet)
                return None

            os.renames(encodeFilename(oldName), encodeFilename(newName))
            while not os.path.isfile(newName):
                log("WAITING FOR RENAMING OF " + oldName + NEW_LINE + "TO " + newName, quiet)
                time.sleep(1)

            modificationCount += 1
            log("RENAMED " + oldName + NEW_LINE + "TO " + newName, quiet)
            return newName
        except IOError as e:
            log("RENAMING ERROR: " + str(e) + " - SOURCE: " + oldName + " NEW NAME: " + newName, quiet)
            return None
    else:
        log("[SIMULATION] RENAMED " + oldName + NEW_LINE + "TO " + newName, quiet)
        return newName



def parseRules(filename, destination, quiet):
    ''' loads and parses the rule file
        returns a Rule list'''
    json_file = open(filename, encoding='utf-8')
    try:
        json_rules = json.load(json_file)
    except Exception as e:
        log("ERROR: invalid Json in " + filename + " - " + str(e), quiet)
        sys.exit()
    json_file.close()
    moveRules = []
    replaceExtensionRules = []
    removeRules = []
    replaceRules = []

    for key in json_rules:
        length = len(json_rules[key])
        if key == "remove":
            k = 0
            while k < length:
                stringToRemove = json_rules[key][k]["delete"]
                removeRules.append(RemoveRule(destination, stringToRemove, quiet))
                k = k + 1
        elif key == "replace":
            l = 0
            while l < length:
                stringToReplace = json_rules[key][l]["string"]
                replacementString = json_rules[key][l]["with"]
                replaceRules.append(ReplaceRule(destination, stringToReplace, replacementString, quiet))
                l = l + 1
        elif key == "replace-extension":
            i = 0
            while i < length:
                oldExtension = json_rules[key][i]["replace"]
                newExtension = json_rules[key][i]["with"]
                replaceExtensionRules.append(ReplaceExtensionRule(destination, oldExtension, newExtension, quiet))
                i = i + 1 
        elif key == "move":
            j = 0
            while j < length:
                name = json_rules[key][j]["contains"]
                newDir = json_rules[key][j]["destination"]
                if "&&" in name:
                    criterias = name.split(" && ")
                    moveRules.append(MoveRule(criterias, destination, newDir, quiet))
                else:
                    moveRules.append(MoveRule([name], destination, newDir, quiet))
                j = j + 1 

    allRules = replaceExtensionRules + removeRules + replaceRules + moveRules
    return allRules


def applyRules(source, rules, real):
    ''' iterate on files in source directory and apply them the rules '''
    files = [f for f in os.listdir(source) if os.path.isfile(os.path.join(source, f))]
    for index, file in enumerate(files):
        if file != None:              
            absoluteFilename = encodeFilename(os.path.join(source, file))
            for rule in rules:
                result = rule.execute(absoluteFilename, real)
                if result == STOP:
                    break
                elif result != None:
                    sourceDirLength = len(source) + 1

                    log("Replacing " + files[index] + NEW_LINE + " with " + result[sourceDirLength:], True)
                    files[index] = encodeFilename(result[sourceDirLength:])

def encodeFilename(filename):
    '''encode filename with current OS encoding'''
    return filename
    newName = str(filename.encode(sys.getfilesystemencoding()))
    # log("Name: " + filename + " - Encoded Name = " + newName, False)
    return newName

class Rule(object):
    # Base Rule
    def execute(self, filename, real):
        pass

class ReplaceRule(Rule):
    # Replaces all occurences of a given string in the filename with another given string
    # this function is case insensitive
    # stringToReplace str regular expression
    # replacementString str
    def __init__(self, destination, stringToReplace, replacementString, quiet):
        self.destination = destination
        self.stringToReplace = stringToReplace
        self.replacementString = replacementString
        self.quiet = quiet

    def execute(self, filename, real):
        global modificationCount
        dirname, shortFileName = os.path.split(filename)
        leftPart, extension = os.path.splitext(shortFileName)
        
        regex = re.compile(self.stringToReplace, re.IGNORECASE)
        if (regex.search(leftPart)):
            log("REPLACING "+ self.stringToReplace + " with: " + self.replacementString, False)
            modificationCount += 1
            newName = re.sub(regex, self.replacementString, leftPart)
            if newName[0:1].isspace():
                newName = newName[1:]
            return rename(self.destination, filename, dirname + os.sep + newName + extension, real, self.quiet)
        else:
            return None

def dump(obj):
   for attr in dir(obj):
       if hasattr( obj, attr ):
           print( "obj.%s = %s" % (attr, getattr(obj, attr)))

class RemoveRule(ReplaceRule):
    # Removes unwanted part from filename
    def __init__(self, destination, stringToRemove, quiet):
        self.destination = destination
        self.stringToReplace = stringToRemove
        self.replacementString = ""
        self.quiet = quiet


class MoveRule(Rule):
    # Regle de déplacement du fichier
    def __init__(self, nameList, destination, newDir, quiet):
        self.nameList = nameList
        self.destination = destination
        self.newDir = newDir
        self.quiet = quiet

    def execute(self, filename, real):
        allNamesInList = True
        for name in self.nameList:
            if name.lower() in filename.lower():
                pass
            else:
                allNamesInList = False
        if allNamesInList is True:
            head, tail = os.path.split(filename)
            finalPath = self.destination + os.sep + self.newDir + os.sep + tail
            return move(filename, finalPath, real, self.quiet)
        else:
            return None

class ReplaceExtensionRule(Rule):
    # replaces a given file extension with another given extension
    def __init__(self, destination, oldExtension, newExtension, quiet):
        self.oldExtension = oldExtension
        self.newExtension = newExtension
        self.destination = destination
        self.quiet = quiet

    def execute(self, filename, real):
        # replaces the extension if it is equal to oldExtension.
        index = filename.rfind(".")
        currentExtension = filename[index+1 :]
        if currentExtension == self.oldExtension:
            newName = filename[0 : index + 1] + self.newExtension
            return rename(self.destination, filename, newName, real, self.quiet)
        else:
            return None


def main():
    global modificationCount
    parser = argparse.ArgumentParser()
    actualDir = os.path.dirname(sys.argv[0])

    encoding = sys.getfilesystemencoding()
    if(encoding is None):
        log("System encoding is the default one", False)
    else:
        log("System encoding is " + str(encoding), False)

    parser.add_argument("destination")  # Mandatory
    parser.add_argument("--real", action="store_true")
    parser.add_argument("--source", default=os.getcwd())
    parser.add_argument("--rules", default=os.path.join(actualDir, "rules.json"))
    parser.add_argument("--quiet", default=False)

    args = parser.parse_args()

    if(os.path.isfile(args.rules)):
        log("--------------------------------------------------------", False)

        log("Applying rules from   " + args.rules, False)
        log("Source directory      " + args.source, False)
        log("Destination directory " + args.destination, False)
        if(args.real is True):
            log("Modifications will be applied", False)
        else:
            log("Modifications will be simulated", False)


        allRules = parseRules(args.rules, args.destination, args.quiet)
        while True:
            modificationCount = 0
            applyRules(args.source, allRules, args.real)
            if (modificationCount == 0):
                break
            
            log(str(modificationCount) + " file(s) modified", args.quiet)
    else:    
        print("ERROR: rule file not found: " + args.rules)

if __name__ == "__main__":
    main()
