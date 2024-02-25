import os
import sys
import dirs
CONFIGFILEPATH = dirs.joinDirs(dirs.getDir(),"smIDE.cfg" )  
CACHEFILEPATH = dirs.joinDirs(dirs.getDir(), "smIDE.cache")
## THESE WILL EVENTUALLY BE GOTTEN FROM THE SMIDE.CFG BUT I HAVENT WRITTEN THAT YET..
#####################
defaultConfigs = '''
##NOTES
# THE "#" PREFIX is a hexadecimal color (#ffffff)
# the "@" prefix is a boolean value, True or false, denoted as @1 or @0   (True or False)
# Comments, denoted with a # at the start of a line, can only be placed at the start of a line, they do not work anywhere else
## GENERAL SETTINGS
defaultHexColor: #FF0000
isAutoSave: @1
openLastFileOnStartup: @1
## MAIN COLOR SETTINGS
mainBackGround: #0a0a0a
## TEXT EDITOR SETTINGS
textEditorBackground: #0a0a0a
textEditorTextColor: #cacaca
textEditorCursorColor: #dbdbdb
## CONSOLE SETTINGS
consoleBackground: #0a0a0a
consoleTextColor: #cacaca
consoleCursorColor: #dbdbdb
## TITLEBODY SETTINGS
titleBodyBackground: #0a0a0a
titleBodyTextColor: #cacaca
titleBodyCursorColor: #dbdbdb



'''
def init() -> dict:
    CONFIGURATIONS = dict()
    try:
        with open(CONFIGFILEPATH, "r") as configFile:
            for line in configFile:
                line = "".join(line.split()) ## CLEARS ALL WHITESPACE
                if len(line) == 0:
                    continue
                if line[0] == "#":
                    line = ""
                    continue

                line = line.split(":") ## DIFFERENT ELEMENTS
                if "#" in line[1].upper(): ## Checks for Hex values, returning only the first 6 AlNum chars
                    line[1] = line[1][:7]
                    CONFIGURATIONS.update({line[0]:line[1]})
                elif "@" in line[1].upper():
                    try:
                        Item = line[1][1]  ##gets only the first element of the string, either 1 or 0
                        Item = True if int(Item) else False
                        CONFIGURATIONS.update({line[0]:Item}) ## INT ITEM RETURNS FALSE/TRUE

                    except ValueError:
                        raise ValueError (f"Config File Error (smIDEconfigs.py), the item {line[0]}'s value is not a boolean value, it MUST be a 1 or 0")
                    except IndexError:
                        raise IndexError (f"Config File Error (smIDEconfigs.py), the item {line[0]}'s value is empty, does it have a value?")
        return CONFIGURATIONS
    except FileNotFoundError:
 
        print("File not found, Maybe the filePath is wrong or the file has been renamed? (configs.py)\nWould you like to create a new config file(y/n) ")
        
        rq = input().lower()
        if rq in ("yes", "y"): 
            print("Creating new file 'smIDE.cfg', please relaunch the program...")
            file = open(CONFIGFILEPATH, "w")
            file.write(defaultConfigs)
            file.close()
            sys.exit()
class cache():
    def __init__(self, path:str) -> None:
        self.path = path
        return None
    def formatData(self,key:str, data:str) -> str|None:
        try:
            format = {key:data}  #{"NAME":"DATASTRAND"}
            self.format = format
            return format
        except:
            return None
    def writeToCache(self, formattedData:str = "") -> None:
        
        try:
            print(self.path)
            with open(self.path, "a") as cache:
                if len(formattedData) == 0:
                    cache.write(self.format+"\n")
                else:
                    cache.writable(formattedData+"\n")
            cache.close()
        except FileNotFoundError:
            print(f"Cache file {self.path} cannot be found, maybe it was initiated wrong or doesnt exist?")
        except:
            print("cannot wrte to cache..")
        return None
    def readCache(self) -> str|None:
        try:
            with open(self.path, "r") as cache:
                data = cache.read()
                data = dict(data)
                self.data = data
            cache.close()
            return data
        except FileNotFoundError:
             print(f"Cache file {self.path} cannot be found, maybe it was initiated wrong or doesnt exist?")
        except:
            print("Cannot read cache..")

    def getFromCache(self, key:str) -> str|None:
        self.readCache()
        try:
            return self.data[key]
             
        except KeyError:
            print(f"The key {key} does't exist in the cache, is it the right one?")
            return None
        except:
            print("Failed to get data from cache")
            return None
