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
class ConfigFile():
    def __init__(self, filePath:str=dirs.getDir())-> None:
        self.CONFIGURATIONS = dict()
        self.CONFIGFILEPATH = filePath
        global defaultConfigs
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
                        self.CONFIGURATIONS.update({line[0]:line[1]})
                    elif "@" in line[1].upper():
                        try:
                            item = line[1][1]  ##gets only the first element of the string, either 1 or 0
                            item = True if int(item) else False
                            self.CONFIGURATIONS.update({line[0]:item}) ## INT ITEM RETURNS FALSE/TRUE

                        except ValueError:
                            raise ValueError (f"Config File Error (smIDEconfigs.py), the item {line[0]}'s value is not a boolean value, it MUST be a 1 or 0")
                        except IndexError:
                            raise IndexError (f"Config File Error (smIDEconfigs.py), the item {line[0]}'s value is empty, does it have a value?")
                    elif "=" in line[1].upper():
                        try:
                            item = line [1][1:]
                            item = int(item)
                            self.CONFIGURATIONS.update({line[0]:item})
                        except ValueError:
                            raise ValueError (f"Config File Error (smIDEconfigs.py), the item {line[0]}'s value is not an integer")
                        except IndexError:
                            raise IndexError (f"Config File Error (smIDEconfigs.py), the item {line[0]}'s value is empty, does it have a value?")
            
            return None
        except FileNotFoundError:
    
            print("File not found, Maybe the filePath is wrong or the file has been renamed? (configs.py)\nWould you like to create a new config file(y/n) ")
            
            rq = input().lower()
            if rq in ("yes", "y"): 
                print("Creating new file 'smIDE.cfg', please relaunch the program...")
                file = open(self.CONFIGFILEPATH, "w")
                file.write(defaultConfigs)
                file.close()
                sys.exit()
    def getSetting(self, setting:str) -> str|bool|int:
        try: 
            return self.CONFIGURATIONS[setting]
        except:
            try:
                default = self.getSetting("defaultHexColor")
                print(f"Configuration {setting} doesn't exist, Defaulting to default hex value {default}")
            except:
                ## When the config file doesnt have the defaultHexColor, it calls this:
                default = "#000000"
            return default
    
class Cache():
    def __init__(self, path:str) -> None:
        self.path = path
        return None
    def formatData(self, data:str) -> str|None:
        try:
            format = data  
            self.format = format
            return format
        except:
            return None
    def writeToCache(self, formattedData:str = "") -> None:
        
        
            #print(self.path)
            with open(self.path, "wt") as cache:
                if len(formattedData) == 0:
                    cache.write(self.format)
                else:
                    pass
            cache.close()
            '''except FileNotFoundError:
                print(f"Cache file {self.path} cannot be found, maybe it was initiated wrong or doesnt exist?")
            except:
                print("cannot wrte to cache..")'''
            return None
    def readCache(self) -> str|None:
        try:
            with open(self.path, "rt") as cache:
                data = cache.read()
                self.data = data
            cache.close()
            return data
        except FileNotFoundError:
             print(f"Cache file {self.path} cannot be found, maybe it was initiated wrong or doesnt exist?")
        except:
            print("Cannot read cache..")

   
