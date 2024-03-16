##Imports from python
import tkinter as tki
import tkinter.messagebox
import tkinter.simpledialog
import subprocess
import sys
import os
from tkinter import filedialog
#from custom tkinter import *
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
    """
    Returns a list of all directories in the current directory
    """
    dirs = os.listdir(path)
    return dirs
def getInput(input:str, prompt:str = "Prompt", initialValue:str = "") -> str: ## CREATES POPUP ASKING FOR STRING INPUT
    """
    Gets user input as string, returns empty if |Cancel|
    """
    out = tkinter.simpledialog.askstring(prompt, input, initialvalue=initialValue)
    if type(out) == str:
        return out
    else:
        return str()
def getYesNo(input:str, prompt:str = "Prompt") -> bool: ## CREATES POPUP ASKING FOR BOOL INPUT
    """
    Gives user an alert Yes | No and returns True | False
    """
    out = tkinter.messagebox.askyesno(prompt, input)
    return out
def userAlert(input:str, prompt:str="Alert") -> bool:
    """
    Gives user an alert OK | Cancel and returns True | False
    """
    resp = tkinter.messagebox.askokcancel(prompt, input)
    return resp
def setWorkingDir(curr:bool = False) ->None:
    """
    Changes the directory
    """
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
    """
    writes data to referenced body
    """
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
    """
    Gets all text from the referenced body
    """
    return textObject.get("1.0", tki.END)

def runCMD(command:list = [str()]) -> str:

    """
    Runs command under subprocess.call()
    """
    try:
        output = subprocess.call(command, shell=True)
        return output

    except:
        return(f"the command {str().join(command)} cannot be executed, or throws an error upon execution.\nRead the console for more")
def getFromFile(filePath:str) -> str:
    """
    Used to open a file and get data from it
    """
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
    """
    writes to a specific file, used by saveFile()
    """
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
    """
    writes to specifically the body titleBody
    """
    if infoType == "": ## DEFAULT TYPE, WHEN SHOWING WHAT FILE IS OPEN
        global CURRENTOPENFILE
        global titleBarTitle
        titleBarTitle = writeToBody(titleBody, f"Opened :'{CURRENTOPENFILE}'")
    else:
        titleBarTitle = writeToBody(titleBody, infoType)
    return None
def runCode(): 

    os.system(f"start /wait cmd /c {'py -i '+CURRENTOPENFILE}") ## opens a new terminal window to run the current file in

def openFile(FILENAME:str = ""):
    """
    Opens windows fileExporer to get a filePath.
    """
    if len(FILENAME) == 0:
        mainloop.filename = filedialog.askopenfilename(initialdir=WORKINGDIR, title ='Open File', filetypes = (('Python Files', '*.py'),('All Files', '*.*')))
        FILENAME = mainloop.filename
    try:
        writeToBody(textEditor, getFromFile(FILENAME))
    except:
        print(f"File {FILENAME} does not exist, Creating file {FILENAME}..")
        updateTitleBody(f"File {FILENAME} does not exist, Creating file {FILENAME}..")
        makeFile(FILENAME)
        writeToBody(textEditor, getFromFile(FILENAME))

def saveFile() -> None:  
    """
    Opens current open file, then writes to it..
    """


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
def makeFile(FILENAME:str|None = str()) -> None:
    
    """
    Creates the file FILENAME at current directory...
    """
    if type(FILENAME) == None:
        return None
    if len(FILENAME) == 0:
        FILENAME = getInput("FileName")
        if len(FILENAME)== 0:
            return None
    if FILENAME in listDirs():
        if not userAlert(f"The file {FILENAME} already exists, Are you sure you want to overwrite it?", "OVERWRITING WARNING"):
            return None
    file = open(FILENAME, "w")
    file.close()
    openFile(FILENAME)
    updateTitleBody()
    return None
def sncFile(): ## SAVE AND EXIT
    """
    Shortcut to save file and quit the program
    """
    saveFile()
    sys.exit(0)


def openConfigFile() -> None:
    """
    Shortcut to open the inbuilt config file
    """
    openFile(smIDEconfigs.CONFIGFILEPATH)
    updateTitleBody()
    return None
def newInstanceOfIDE() -> None: ## Havent added support for the EXE format yet.. CBA ATM
    """
    Uses the runCMD to rerun the file.. only works if python is installed globally and called by the 'py' cmd
    """
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
    """
    destroys mainloop and calls newInstanceOfIDE
    """
    global CONFIGURATIONS
    CONFIGURATIONS = smIDEconfigs.ConfigFile() ## REREADS THE INIT FILE, resetting the values in the code to its ones
    mainloop.destroy()
    newInstanceOfIDE()
    return None
def manualSave() -> None:
    saveFile()
    userAlert("Saved File")
    
def renameFile(oldFileName:str = CURRENTOPENFILE, newFileName:str=str()) -> None:
    """
    procedure to rename file
    """
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
def updateTextInfo():
    cursorPos = textEditor.index(tkinter.INSERT), textEditor.index(tkinter.CURRENT)
    fileName = CURRENTOPENFILE.split("/")[-1]
    info = f"fileName: '{fileName}'  |column: {cursorPos} |row: {1} "
    writeToBody(textInfo,info)

def parseText(text:str) -> str:
    """
    Iterates through the text, and colours by adding tkinter tag objects
    """
    if len(text) == 0:
        return str
    ## Parse text
    
    textEditor.tag_config("blank", foreground="#ffffff") ## tag for brackets
    textEditor.tag_config("bracket", foreground="#ebcd0c") ## tag for brackets
    textEditor.tag_config("bracket2", foreground="#4fd3fc")
    textEditor.tag_config("speechMark", foreground="#ff7b00") ## tag for strings
    textEditor.tag_config("comment", foreground="#777777")
    textEditor.tag_config("declareVariable", foreground="#34a2ea")
    textList = text.split("\n")
    textDict = {}
    ## creates a dict of {linenumber:line}
    for i, item in enumerate(textList):

        textDict.update({i+1:item})
    ## goes through the dict, looking for characters and "painting" them the right tag color
    for i in textDict:

        for j, item in enumerate(textDict[i]):

            if item in {"(", ")", "[", "]", "{", "}"}:
                textEditor.tag_add("bracket", str(i)+"."+str(j), str(i)+"."+str(j+1))
            elif item in {"'",'"'}:
                textEditor.tag_add("speechMark", str(i)+"."+str(j), str(i)+"."+str(j+1) )
            elif item == "#":
                textEditor.tag_add("comment", str(i)+"."+str(j), str(i)+"."+str(len(textDict[i])))
            elif item == "=":
                textEditor.tag_add("declareVariable", str(i)+"."+"0", str(i)+"."+str(j))
            else:
                for tag in textEditor.tag_names():
                    textEditor.tag_remove(tag, str(i)+"."+str(j), str(i)+"."+str(j+1))

## I cant for the life of me figure out why tkinter is parsing a "self" argument here, but it is, and it doesnt matter, so i am just going to ignore it..    
def onModified(toMakeTkinterHappyIgnoreThisVariableNameOrItsGeneralExistence=""): ## RUNS WHENEVER the text in the main window is changed
    """
    This is ran every time that the body "textEditor" is modified. it is bound to tkinters modification flag..
    """
    updateTextInfo()
    parseText(getFromBody(textEditor))
    if ISAUTOSAVE: ## RESETS THE MODIFIED FLAG
        
        textEditor._resetting_modified_flag = True
        try:
            textEditor.tk.call(textEditor._w, 'edit', 'modified', 0)
        finally:
            textEditor._resetting_modified_flag = False
        saveFile()
    else:
        mainloop.title("*Small IDE")


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
textInfo = tki.Text(width=CONFIGURATIONS.getSetting("generalBodyWidth"),
                    height=CONFIGURATIONS.getSetting("infoBodyHeight"),
                    bg = CONFIGURATIONS.getSetting("infoBodyBackground"),
                    fg=CONFIGURATIONS.getSetting("infoBodyTextColor"),
                    insertbackground=CONFIGURATIONS.getSetting("infoBodyCursorColor")
                     )
textInfo.pack()
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

if CONFIGURATIONS.getSetting("openLastFileOnStartup"):
    openFile(CURRENTOPENFILE) ## Opens up the last opened file

mainloop.config(menu=menuBar)
mainloop.mainloop()