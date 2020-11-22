# -*- coding: utf8 -*-

import fileorganiser
import os

from fileorganiser import ReplaceExtensionRule
from fileorganiser import parseRules
from fileorganiser import MoveRule
from fileorganiser import RemoveRule
from fileorganiser import ReplaceRule
from fileorganiser import STOP

SOURCE_DIR = os.path.dirname(os.path.realpath(__file__)) + "/testData/"
DESTINATION_DIR = SOURCE_DIR + "test/"
SUB_DIR = "Marvel/Test/"

def createIfNotExist(filename):
    if os.path.isfile(filename) is False:
        testfile = open(filename, "a")
        testfile.close()

def deleteIfExists(filename):
    if os.path.isfile(filename):
        os.remove(filename)


# check the extension replacement simulation
file1 = os.path.join(SOURCE_DIR, "FileWithExtensionToReplace.zip")
file2 = os.path.join(SOURCE_DIR, "FileWithExtensionToReplace.cbz")
createIfNotExist(file1)
deleteIfExists(file2)
extensionRule = ReplaceExtensionRule("zip", "cbz", False)
extensionRule.execute(file1, False)
assert(os.path.isfile(file1) is True), "File extension was changed during a simulation"
assert(os.path.isfile(file2) is False), "Replace extension rule was executed during a simulation"
print("extension replacement simulation OK")


# check the real extension replacement
createIfNotExist(file1)
deleteIfExists(file2)
extensionRule = ReplaceExtensionRule("zip", "cbz", False)
extensionRule.execute(file1, True)
assert(os.path.isfile(file1) is False), "File extension was not changed"
assert(os.path.isfile(file2) is True), "File extension not changed"
print("real extension replacement OK")


# check filename part removal simulation  
file3 = os.path.join(SOURCE_DIR, "[Comics.FR] FileToRename.txt")
file4 = os.path.join(SOURCE_DIR, "FileToRename.txt")
createIfNotExist(file3)
deleteIfExists(file4)
removeRule1 = RemoveRule("\[?Comics\.?FR\]?\s?", False)
result1 = removeRule1.execute(file3, False)
assert(result1 == file4), "removeRule1 returned " + str(result1) + " instead of " + str(file4)
assert(os.path.isfile(file3) is True), "File was renamed during a simulation"
assert(os.path.isfile(file4) is False), "Source file does not exist after a simulation"
print("filename part removal simulation OK")

# check filename part removal does nothing when the string to be removed is not found  
createIfNotExist(file3)
deleteIfExists(file4)
removeRule2 = RemoveRule("FooBar", False)
result2 = removeRule2.execute(file3, False)
assert(result2 is None), "When the string to be removed was not found, a remove rule should return None" 
assert(os.path.isfile(file3) is True), "File was renamed although the string to be removed was not found"
assert(os.path.isfile(file4) is False), "Source file does not exist although the string to be removed was not found"
print("filename part removal does nothing when the string to be removed is not found OK")

# check real filename part removal
createIfNotExist(file3)
deleteIfExists(file4)
removeRule3 = RemoveRule("\[Comics\.FR\]", False)
result3 = removeRule3.execute(file3, True)
assert(result3 == file4), "removeRule3 returned " + str(result3) + " instead of " + str(file4)
assert(os.path.isfile(file3) is False), "File name not changed"
assert(os.path.isfile(file4) is True), "New file name is not the expected one"
print("real filename part removal OK")

# test the real filename part removal when multiple renaming rules apply
file3Multiple = os.path.join(SOURCE_DIR, "[Comics.FR][Comics.FR][Comics.FR]FileToRename[Comics.FR].txt")  
createIfNotExist(file3Multiple)
deleteIfExists(file4)
removeRule4 = RemoveRule("\[Comics\.FR\]", False)
result4 = removeRule4.execute(file3Multiple, True)
assert(result4 == file4), "removeRule4 returned " + str(result4) + " instead of " + str(file4)
assert(os.path.isfile(file3Multiple) is False), "File name not changed"
assert(os.path.isfile(file4) is True), "New file name is not the expected one"
print("real filename part removal when multiple renaming rules apply OK")

# check real filename part removal when there is a space to be removed
file3WithASpace =  os.path.join(SOURCE_DIR, "[Comics.FR] FileToRename.txt")
createIfNotExist(file3WithASpace)
deleteIfExists(file4)
removeRule5 = RemoveRule("\[Comics\.FR\]", False)
result5 = removeRule5.execute(file3WithASpace, True)
assert(result5 == file4),  "removeRule5 returned " + str(result5) + " instead of " + str(file4)
assert(os.path.isfile(file3WithASpace) is False), "File name not changed"
assert(os.path.isfile(file4) is True), "New file name is not the expected one"
print("real filename part removal when there is a space to be removed OK")

# test file moving simulation
file5 = os.path.join(SOURCE_DIR, "FileToMove.cbz")
file6 = os.path.join(DESTINATION_DIR, SUB_DIR, "FileToMove.cbz")
createIfNotExist(file5)
deleteIfExists(file6)
moveRule0 = MoveRule(["FileToMove"], DESTINATION_DIR, SUB_DIR, False)
moveResult0 = moveRule0.execute(file5, False)
assert(moveResult0 == STOP),  "moveRule0 returned " + str(moveResult0) + " instead of " + str(STOP)
assert(os.path.isfile(file5) is True), "File was moved from source folder during a simulation"
assert(os.path.isfile(file6) is False), "File was moved to destination folder during a simulation"
print("file moving simulation OK")

# test real file moving
file9 = os.path.join(SOURCE_DIR, "FileToMove.cbz")
file10 = os.path.join(DESTINATION_DIR, SUB_DIR, "FileToMove.cbz")
createIfNotExist(file9)
deleteIfExists(file10)
moveRule2 = MoveRule(["FileToMove"], DESTINATION_DIR, SUB_DIR, False)
moveResult2 = moveRule2.execute(file9, True)
assert(moveResult2 == STOP), "moveRule0 returned " + str(moveResult2) + " instead of " + str(STOP)
assert(os.path.isfile(file9) is False), "File still in the source directory"
assert(os.path.isfile(file10) is True), "File not moved to destination folder"
print("real file moving OK")

# check moving a file with a logical OR condition, case insensitive
# TODO: create two distinct tests
file7 = os.path.join(SOURCE_DIR, "[COMics-Fr]Iron-man l'HéRItagE.rar")
file8 = os.path.join(DESTINATION_DIR, SUB_DIR + "[COMics-Fr]Iron-man l'HéRItagE.rar")
createIfNotExist(file7)
deleteIfExists(file8)
moveRule1 = MoveRule(["Iron-man", "Héritage"], DESTINATION_DIR, SUB_DIR, False)
moveResult1 = moveRule1.execute(file7, True)
assert(moveResult1 == STOP), "moveRule1 returned " + str(moveResult1) + " instead of " + str(STOP)
assert(os.path.isfile(file7) is False), "File was moved from source folder during a simulation"
assert(os.path.isfile(file8) is True), "File was moved to destination folder during a simulation"
print("real file moving with a logical OR condition OK")

# check ReplaceRule simulation
file11 = os.path.join(SOURCE_DIR, "FileToRename.cbz")
file12 = os.path.join(SOURCE_DIR, "FileWithANewName.cbz")
createIfNotExist(file11)
deleteIfExists(file12)
replaceRule1 = ReplaceRule('ToRename', 'WithANewName', False)
replaceResult1 = replaceRule1.execute(file11, False)
assert(replaceResult1 == file12), "replaceRule1 returned " + str(replaceResult1) + " instead of " + str(file12)
assert(os.path.isfile(file11) is True), "File was altered during a renaming simulation"
assert(os.path.isfile(file12) is False), "File was renamed during a renaming simulation"
print("Simulation of part replacement in filename OK")

# check ReplaceRule real execution
createIfNotExist(file11)
deleteIfExists(file12)
replaceRule2 = ReplaceRule('ToRename', 'WithANewName', False)
replaceResult2 = replaceRule2.execute(file11, True)
assert(replaceResult2 == file12), "replaceRule2 returned " + str(replaceResult2) + " instead of " + str(file12)
assert(os.path.isfile(file11) is False), "File was not altered during a renaming"
assert(os.path.isfile(file12) is True), "File was not renamed during a renaming"
print("Real part replacement in filename OK")

# tester que parseRules renvoie un tableau et son contenu
result = parseRules(SOURCE_DIR + "rules.json", DESTINATION_DIR, False)
assert(isinstance(result, list)), "parseRules must return a list"
assert(len(result) == 10), "parseRules must return a ten element list"
assert(isinstance(result[0], fileorganiser.fileorganiser.ReplaceExtensionRule)), "First rule must be a ReplaceExtensionRule instance"
assert(isinstance(result[1], fileorganiser.fileorganiser.ReplaceExtensionRule)), "Second rule must be a ReplaceExtensionRule instance"
assert(isinstance(result[2], fileorganiser.fileorganiser.RemoveRule)), "Third rule must be a RemoveRule instance"
assert(isinstance(result[3], fileorganiser.fileorganiser.RemoveRule)), "Fourth rule must be a RemoveRule instance"
assert(isinstance(result[4], fileorganiser.fileorganiser.RemoveRule)), "Fifth rule must be a RemoveRule instance"
assert(isinstance(result[5], fileorganiser.fileorganiser.RemoveRule)), "Sixth rule must be a RemoveRule instance"
assert(isinstance(result[6], fileorganiser.fileorganiser.RemoveRule)), "Seventh rule must be a RemoveRule instance"
assert(isinstance(result[7], fileorganiser.fileorganiser.RemoveRule)), "Eighth rule must be a RemoveRule instance"
assert(isinstance(result[8], fileorganiser.fileorganiser.MoveRule)), "Ninth rule must be a MoveRule instance"
assert(isinstance(result[9], fileorganiser.fileorganiser.MoveRule)), "Tenth rule must be a MoveRule instance"
print("Test Rule file parsing OK")