import tkinter.simpledialog as tkBox
import tkinter.messagebox as tkMBox
import os
import sys
import requests
import webbrowser


class FailedRequest():pass ## This things entire existance is to make debugging easier, if you have this error, it is because python cant reach github, so either the repo is broken, you have no internet, or a firewall is blocking the request

REQUESTDOMAIN = "https://raw.github.com/Anton-Chernyshov/smallIDE/main/"
requiredFilesToInstall = ["smIDEconfigs.py", "smIDEmain.pyw", "smIDE.cfg", "smIDEerrors.py", "run.py", "start.bat", "smIDEterminal.py", "dirs.py"]
def openURL(url):
    if not webbrowser.open_new(url):
        print("No WebBrowser found..")
        print("")
        print("here is the URL tho:")
        print("https://github.com/Anton-Chernyshov/smallIDE/blob/main/LICENSE")
def getInput(input:str, prompt:str = "Prompt", initialValue:str = "") -> str: ## CREATES POPUP ASKING FOR STRING INPUT
    out = tkBox.askstring(prompt, input, initialvalue=initialValue)
    if type(out) == str:
        return out
    else:
        return ""
def getYesNo(input:str, prompt:str = "Prompt") -> bool: ## CREATES POPUP ASKING FOR BOOL INPUT
    out = tkMBox.askyesno(prompt, input)
    return out
def userAlert(input:str, prompt:str="Alert") -> bool:
    resp = tkMBox.askokcancel(prompt, input)
    return resp

def writeToFile(filePath:str, data:bytes|str): ## allows for bytes bcs python now. 
    if type(data) == bytes:
        data = data.decode() ## Defauults to uft8 
    try:
        with open(filePath, "w") as file:
            file.write(data)
            file.close()
    except FileNotFoundError:
        raise FileNotFoundError(f"Function writeToFile cannot open file {filePath} as it does not exist")
def getGithubRequest(URL:str) -> str|None:
    try:
        response = requests.get(URL)
        output = response.content
        #print(output)
        return output
    except:
        raise ("There was an error getting the request, try again please..")
def concatenatePath(*items:str) -> str:
    out = str()
    for i in range(len(items)):
        out += items[i]
    return out
def installFiles(filesList:list, dir:str) -> None:
     for i, fileName in enumerate(filesList):
        print(f"installing {fileName} ....\n")
        request = getGithubRequest(concatenatePath(REQUESTDOMAIN, fileName))
        print(f"request recieved from github, writing to file {fileName}\n")
        writeToFile(concatenatePath(dir,"\\", fileName), request)
        print(f"({i+1}/{len(requiredFilesToInstall)}) files installed..\n")
def exitNotes()->None:
    print("-"*50)
    print("""Some things to note:
          - Please dont rename the config file, or if you want to have many, ENSURE that there is at least 1 file called 'smIDE.cfg'
          - Keep all these files in the same directory as each other. If you move them to a different Dir, thats fine, as long as all of them are present.
          - If at any point any file is broken or doesn't work, you can just run the installer (this file), specifying which file you want to re-install
          """)
    print("Installation has finished, Enjoy!!")
    print("-"*50)
    input("press 'Enter' to quit...")
def init():
    curDir = os.getcwd()
    if not getYesNo("""
Is this a first time Install or are you patching files?
"Yes" for first time
"No" for patching/Reinstalling files
"""): ## IF USER IS PATCHING, IT GOES INTO THIS STATEMENT
        fileName = getInput(f"Please enter a filename from these files to reinstall/rewrite \n {requiredFilesToInstall}")
        while  fileName not in requiredFilesToInstall:
            
            if not userAlert("Invalid Filename"):
                sys.exit()
            fileName = getInput(f"Please enter a valid filename from these files to reinstall/rewrite \n {requiredFilesToInstall}")
        installToDirectory = getInput(" "*20+f"What directory is the file {fileName} inside?"+" "*20, "Select Installation Directory", curDir)
        installFiles([fileName], installToDirectory)
        exitNotes()
        sys.exit()
    if not userAlert("""
You are about to install 'Small IDE' onto your PC, would you like to begin the installation process?
By clicking OK and therefore continuing with the installation process, you agree to the user license on the github:
'https://github.com/Anton-Chernyshov/smallIDE/blob/main/LICENSE'.
Do you want to continue? (clicking cancel will open the license in the webbrowser before exiting the application. )
"""):
        openURL("https://github.com/Anton-Chernyshov/smallIDE/blob/main/LICENSE")
        sys.exit()

    
    installToDirectory = getInput('''What directory would you like to install to? This will contain the config file, and the other files for the code to run?
                                  This will default to the directory where this file is currently being run in unless changed.''', "Select Install Directory", curDir)
    
    if len(installToDirectory) == 0:
        installToDirectory = curDir

    
    installFiles(requiredFilesToInstall,installToDirectory)

    exitNotes()
init()






