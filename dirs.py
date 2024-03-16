import os
import sys
import smIDEerrors
def getDir() -> str|None:
 """
 Gets the current working directory from os.getcdw()
 """
 try:
  curDir = os.getcwd()
 except:
  raise smIDEerrors.DirectoryExistsError("Cannot get current directory")
 if len(curDir) == 0:
  return None
 return curDir

def joinDirs(*dirs:str) -> str|None:
 """
 Formats directory's with \ characters
 """
 output = str()
 dirs = list(dirs)
 if len(dirs) == 0:
  return None
 
 for dir in dirs:
  if type(dir) == str:
   output += dir +"\\" # dir
 #print(output)

 if "." in dirs[-1]:
  output = output[:-1]
 return output
  












