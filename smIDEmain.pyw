##Imports from python
import tkinter as tki
import tkinter.messagebox
import tkinter.simpledialog
import subprocess
import sys
import os

## Custom File Imports
import smIDEconfigs ## configurator
from smIDEerrors import *



##INITIALIZE PROGRAM (GET DATA FROM CONFIG)
CONFIGURATIONS = smIDEconfigs.init()

def getSetting(setting:str) -> str:
    try: 
        return CONFIGURATIONS[setting]
    except:
        default = getSetting("defaultHexColor")
        print(f"Configuration {setting} doesn't exist, Defaulting to default hex value {default}")
        return default
    
## GLOBAL VARS
CURRENTOPENFILE = str() ## FILEPATH OF CURRENT STRING
ISAUTOSAVE = getSetting("isAutoSave")

## PROCEDURES AND FUNCTIONS

def getInput(input:str, prompt:str = "Prompt", initialValue:str = "") -> str: ## CREATES POPUP ASKING FOR STRING INPUT
    out = tkinter.simpledialog.askstring(prompt, input, initialvalue=initialValue)
    if type(out) == str:
        return out
    else:
        return ""
def getYesNo(input:str) -> bool: ## CREATES POPUP ASKING FOR BOOL INPUT
    out = tkinter.messagebox.askyesno("Prompt", input)
    return True if out=="yes" else False
def userAlert(input:str):
    tkinter.messagebox.askokcancel("ALERT", input)

def writeToBody(textObject:tki.Text, text:str = "", writemode:int = 0): ## by default clears the object referenced
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


def getFromBody(textObject:tki.Text) -> str: ## GETS text from referenced body
    return textObject.get("1.0", tki.END)

def runCMD(command:list = [str()]) -> str:
    try:
        output = subprocess.check_output(command, shell=True)
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
def updateTitleBody(infoType:str = ""):
    if infoType == "": ## DEFAULT TYPE, WHEN SHOWING WHAT FILE IS OPEN

        global CURRENTOPENFILE
        writeToBody(titleBody, f"Opened :'{CURRENTOPENFILE}'")
    else:
        writeToBody(titleBody, infoType)
def runCode(): ## runs code, and writes output to the console body
    ##code = getFromBody(textEditor)
    command = ["py", CURRENTOPENFILE]
    print(command)
    output = runCMD(command=command)

    writeToBody(console, output, 1)
    
def openFile(FILENAME=str()):
    if len(FILENAME) == 0:
        FILENAME = getInput("FileName")
    try:
        writeToBody(textEditor, getFromFile(FILENAME))
    except:
        print(f"File {FILENAME} does not exist, Creating file {FILENAME}..")
        updateTitleBody(f"File {FILENAME} does not exist, Creating file {FILENAME}..")
        makeFile(FILENAME)
        writeToBody(textEditor, getFromFile(FILENAME))

    
        
    

def saveFile():  
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
        FILENAME = getInput("FileName")
    with open(FILENAME, "w") as file:
        code = getFromBody(textEditor)
        file.write(code)
        file.close()
    updateTitleBody()
    
def makeFile(FILENAME:str = str()):
    if len(FILENAME) == "0":
        FILENAME = getInput("FileName")
    file = open(FILENAME, "w")
    file.close()
    openFile(FILENAME)
    updateTitleBody()
def sncFile(): ## SAVE AND EXIT
    saveFile()
    exit()


def openConfigFile():
    openFile(smIDEconfigs.CONFIGFILEPATH)
    updateTitleBody()
def newInstanceOfIDE(): ## Havent added support for the EXE format yet.. CBA ATM
    fileName = __file__
    if ".py" in fileName or ".pyw" in fileName:
        runCMD(["py", fileName])
    else:
        raise FileTypeError ("This file extension isn't a python file, yet you are running this python code. How in all that is holy have you done that?")

def refreshIDE():
    CONFIGURATIONS = smIDEconfigs.init() ## REREADS THE INIT FILE, resetting the values in the code to its ones
    mainloop.destroy()
    newInstanceOfIDE()


## I cant for the life of me figure out why tkinter is parsing a "self" argument here, but it is, and it doesnt matter, so i am just going to ignore it..    
def onModified(toMakeTkinterHappyIgnoreThisVariableNameOrItsGeneralExistence=""): ## RUNS WHENEVER the text in the main window is changed
    
    saveFile()



## MAIN LOOP

mainloop = tki.Tk()
mainloop.title("Small IDE")
mainloop.configure(background=getSetting("mainBackGround"))
mainloop.geometry("1920x1080")


titleBody = tki.Text(width=180,
                     height=1,
                     bg = getSetting("titleBodyBackground"),
                     fg = getSetting("titleBodyTextColor"),
                     insertbackground=getSetting("titleBodyCursorColor"),
                     
                     )
titleBody.pack()

textEditor = tki.Text(width=180,
                     height=50, 
                     bg=getSetting("textEditorBackground"), 
                     fg=getSetting("textEditorTextColor"), 
                     insertbackground=getSetting("textEditorCursorColor")
                     )
textEditor.pack()
textEditor.bind_all('<<Modified>>', onModified)
console = tki.Text(width=180,
                    height=9, 
                    bg=getSetting("consoleBackground"),
                    fg=getSetting("consoleTextColor"), 
                    insertbackground=getSetting("consoleCursorColor")
                    )
console.pack()

menuBar = tki.Menu(mainloop)
## RUNBAR
runBar = tki.Menu(menuBar, tearoff=0)
runBar.add_command(label="Run", command=runCode)
runBar.add_command(label="Exit without Saving", command=sys.exit) ## INSTAQUIT!!


## FILEBAR
fileBar = tki.Menu(menuBar,tearoff=0)
fileBar.add_cascade(label="Make File", command=makeFile)
fileBar.add_cascade(label="Open File", command=openFile)
fileBar.add_cascade(label="Save File", command=saveFile)
fileBar.add_cascade(label="Save and Close File", command=sncFile)

## SETTINGSBAR
settingsBar = tki.Menu(menuBar, tearoff=0)
settingsBar.add_cascade(label="openConfigFile", command=openConfigFile)
settingsBar.add_cascade(label="Refresh IDE", command=refreshIDE)
settingsBar.add_cascade(label="New Instance", command=newInstanceOfIDE)
## add the menus
menuBar.add_cascade(label="Run", menu=runBar)
menuBar.add_cascade(label="File", menu=fileBar)
menuBar.add_cascade(label="Settings", menu=settingsBar)



mainloop.config(menu=menuBar)
mainloop.mainloop()




