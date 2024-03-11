##Imports from python
import tkinter as tki
import tkinter.messagebox
import tkinter.simpledialog
import subprocess
import sys
import os
## Custom File Imports
import smIDEconfigs
from smIDEerrors import *



##INITIALIZE PROGRAM (GET DATA FROM CONFIG)
CONFIGURATIONS = smIDEconfigs.ConfigFile()
## GLOBAL VARS
lastOpenedCache = smIDEconfigs.Cache(smIDEconfigs.CACHEFILEPATH)
CURRENTOPENFILE = lastOpenedCache.readCache() ## FILEPATH OF CURRENT STRING
ISAUTOSAVE = CONFIGURATIONS.getSetting("isAutoSave")
WORKINGDIR = os.getcwd()
titleBarTitle = ""

## PROCEDURES AND FUNCTIONS
def listDirs(path:str = WORKINGDIR) -> list:
    dirs = os.listdir(path)
    return dirs
def getInput(input:str, prompt:str = "Prompt", initialValue:str = "") -> str: ## CREATES POPUP ASKING FOR STRING INPUT
    out = tkinter.simpledialog.askstring(prompt, input, initialvalue=initialValue)
    if type(out) == str:
        return out
    else:
        return str()
def getYesNo(input:str, prompt:str = "Prompt") -> bool: ## CREATES POPUP ASKING FOR BOOL INPUT
    out = tkinter.messagebox.askyesno(prompt, input)
    return out
def userAlert(input:str, prompt:str="Alert") -> bool:
    resp = tkinter.messagebox.askokcancel(prompt, input)
    return resp
def setWorkingDir(curr:bool = False) ->None:
    global WORKINGDIR
    if not curr:
        dir = getInput("What Directory would you like to work in? (This will ensure that creating / opening files without the full filepath will come from this directory)", "Change Working Directory", WORKINGDIR)
        WORKINGDIR = dir
        os.chdir(WORKINGDIR)
    else:
        WORKINGDIR = os.getcwd()
    userAlert(f"Set working Directory to {WORKINGDIR}")
    updateTitleBody(f"Working from {WORKINGDIR}")
def writeToBody(textObject:tki.Text, text:str = "", writemode:int = 0) -> str: ## by default clears the object referenced
    if writemode not in {0, 1, 2}: ## checks if a valid writemode is entered
        writemode = 0
    if writemode == 0: ## OVERWRITE TEXT
        textObject.delete("1.0", tki.END)
        textObject.insert(tki.END, text)
    elif writemode == 1: ## APPEND to current text
        textObject.insert(tki.INSERT, text)
    elif writemode == 2: ## PREPEND TO THE CURRENT TEXT
        textObject.insert("1.0", text)
    else:
        print("ERROR WRITING TO BODY")

    return text
def getFromBody(textObject:tki.Text) -> str: ## GETS text from referenced body
    return textObject.get("1.0", tki.END)

def runCMD(command:list = [str()]) -> str:
    try:
        output = subprocess.call(command, shell=True)
        return output

    except:
        return(f"the command {str().join(command)} cannot be executed, or throws an error upon execution.\nRead the console for more")
def getFromFile(filePath:str) -> str:
    try:
        with open(filePath, "r") as file:
            global CURRENTOPENFILE 
            CURRENTOPENFILE = filePath
            data = file.read()
            file.close()
            updateTitleBody()
            return data
    except FileNotFoundError: 
        CURRENTOPENFILE = str()

        raise FileNotFoundError(f"Function getFromFile cannot open file {filePath} as it does not exist")
    
def writeToFile(filePath:str, data:str) -> str:
    global CURRENTOPENFILE
    try:
        with open(filePath, "w") as file:
            file.write(data)
            file.close()
            
        CURRENTOPENFILE = str()
        updateTitleBody()
        return None
    except FileNotFoundError:
        raise FileNotFoundError(f"Function writeToFile cannot open file {filePath} as it does not exist")
##TKINTER ACCESSED PROCEDURES
def updateTitleBody(infoType:str = "") -> None:
    if infoType == "": ## DEFAULT TYPE, WHEN SHOWING WHAT FILE IS OPEN
        global CURRENTOPENFILE
        global titleBarTitle
        titleBarTitle = writeToBody(titleBody, f"Opened :'{CURRENTOPENFILE}'")
    else:
        titleBarTitle = writeToBody(titleBody, infoType)
    return None
def runCode(): 

    os.system(f"start /wait cmd /c {"py -i "+CURRENTOPENFILE}") ## opens a new terminal window to run the current file in

def openFile(FILENAME:str = str()):
    if len(FILENAME) == 0:
        FILENAME = getInput(f"Please enter a FileName")
    try:
        writeToBody(textEditor, getFromFile(FILENAME))
    except:
        print(f"File {FILENAME} does not exist, Creating file {FILENAME}..")
        updateTitleBody(f"File {FILENAME} does not exist, Creating file {FILENAME}..")
        makeFile(FILENAME)
        writeToBody(textEditor, getFromFile(FILENAME))

    
        
    

def saveFile() -> None:  
    if ISAUTOSAVE: ## RESETS THE MODIFIED FLAG
        textEditor._resetting_modified_flag = True
        try:
            textEditor.tk.call(textEditor._w, 'edit', 'modified', 0)
        finally:
            textEditor._resetting_modified_flag = False


    global CURRENTOPENFILE
    if len(CURRENTOPENFILE) != 0:
        FILENAME = CURRENTOPENFILE
    else:

        FILENAME = "untitled.txt" ## default filename 
        CURRENTOPENFILE = FILENAME
    lastOpenedCache.formatData(CURRENTOPENFILE)
    lastOpenedCache.writeToCache()
    with open(FILENAME, "w") as file:
        code = getFromBody(textEditor)
        file.write(code)
        file.close()
    updateTitleBody()
    return None
def makeFile(FILENAME:str = str()) -> None:
    if len(FILENAME) == 0:
        FILENAME = getInput("FileName")
    if FILENAME in listDirs():
        if not userAlert(f"The file {FILENAME} already exists, Are you sure you want to overwrite it?", "OVERWRITING WARNING"):
            return None
    file = open(FILENAME, "w")
    file.close()
    openFile(FILENAME)
    updateTitleBody()
    return None
def sncFile(): ## SAVE AND EXIT
    saveFile()
    sys.exit()


def openConfigFile() -> None:
    openFile(smIDEconfigs.CONFIGFILEPATH)
    updateTitleBody()
    return None
def newInstanceOfIDE() -> None: ## Havent added support for the EXE format yet.. CBA ATM
    fileName = __file__
    if ".py" in fileName or ".pyw" in fileName:
        runCMD(["py", fileName])
    else:
        raise FileTypeError ("This file extension isn't a python file, yet you are running this python code. How in all that is holy have you done that?")
    return None
def seeFiles()-> None:
    userAlert([i+"\n" for i in listDirs()], f"Files in dir {WORKINGDIR}")
    return None
def refreshIDE() -> None:
    global CONFIGURATIONS
    CONFIGURATIONS = smIDEconfigs.ConfigFile() ## REREADS THE INIT FILE, resetting the values in the code to its ones
    mainloop.destroy()
    newInstanceOfIDE()
    return None
def manualSave() -> None:
    saveFile()
    userAlert("Saved File")
def renameFile(oldFileName:str = CURRENTOPENFILE, newFileName:str=str()) -> None:
    global CURRENTOPENFILE
    if len(newFileName) == 0:
        newFileName = getInput(f"What do you want to rename the file {oldFileName} to?", "FileRename", oldFileName)
    try:
        os.rename(CURRENTOPENFILE, newFileName)
        CURRENTOPENFILE = newFileName
        updateTitleBody()
    except:
        print(f"cannot rename file {oldFileName} to {newFileName}")
    return None

def parseText(text:str) -> str:
    if len(text) == 0:
        return str
    for i in text:
        pass
## I cant for the life of me figure out why tkinter is parsing a "self" argument here, but it is, and it doesnt matter, so i am just going to ignore it..    
def onModified(toMakeTkinterHappyIgnoreThisVariableNameOrItsGeneralExistence=""): ## RUNS WHENEVER the text in the main window is changed
    
    saveFile()


## MAIN LOOP

mainloop = tki.Tk()
mainloop.title("Small IDE")
mainloop.configure(background=CONFIGURATIONS.getSetting("mainBackGround"))



titleBody = tki.Text(width=CONFIGURATIONS.getSetting("generalBodyWidth"),
                     height=CONFIGURATIONS.getSetting("titleBodyHeight"),
                     bg = CONFIGURATIONS.getSetting("titleBodyBackground"),
                     fg = CONFIGURATIONS.getSetting("titleBodyTextColor"),
                     insertbackground=CONFIGURATIONS.getSetting("titleBodyCursorColor"),
                     
                     )
titleBody.pack()

textEditor = tki.Text(width=CONFIGURATIONS.getSetting("generalBodyWidth"),
                     height=CONFIGURATIONS.getSetting("textEditorBodyHeight"), 
                     bg=CONFIGURATIONS.getSetting("textEditorBackground"), 
                     fg=CONFIGURATIONS.getSetting("textEditorTextColor"), 
                     insertbackground=CONFIGURATIONS.getSetting("textEditorCursorColor"),
                     wrap="word",
                     )
textEditor.pack()
textEditor.bind_all('<<Modified>>', onModified)

menuBar = tki.Menu(mainloop)
## RUNBAR
runBar = tki.Menu(menuBar, tearoff=0)
runBar.add_command(label="Run", command=runCode)
runBar.add_command(label="Exit without Saving", command=sys.exit) ## INSTAQUIT!!


## FILEBAR
fileBar = tki.Menu(menuBar,tearoff=0)
fileBar.add_cascade(label="Make File", command=makeFile)
fileBar.add_cascade(label="Open File", command=openFile)
fileBar.add_cascade(label="Save File", command=manualSave)
fileBar.add_cascade(label="Save and Close File", command=sncFile)
fileBar.add_cascade(label="Change Directory", command=setWorkingDir)
fileBar.add_cascade(label="Show Files", command= seeFiles)
fileBar.add_cascade(label="Rename Current File", command=renameFile)
## SETTINGSBAR
settingsBar = tki.Menu(menuBar, tearoff=0)
settingsBar.add_cascade(label="openConfigFile", command=openConfigFile)
settingsBar.add_cascade(label="Refresh IDE", command=refreshIDE)
settingsBar.add_cascade(label="New Instance", command=newInstanceOfIDE)
## add the menus
menuBar.add_cascade(label="Run", menu=runBar)
menuBar.add_cascade(label="File", menu=fileBar)
menuBar.add_cascade(label="Settings", menu=settingsBar)

openFile(CURRENTOPENFILE) ## Opens up the last opened file

mainloop.config(menu=menuBar)
mainloop.mainloop()








