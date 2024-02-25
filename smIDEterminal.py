import tkinter
import subprocess
import os
class Terminal():
    def __init__(self, rootBody:tkinter.Tk,width:int = 100, height:int = 10, bgColor:str = "#000000", textColor:str = "#ffffff", caretColor:str="#ffffff", inputPrompt:str = "> ", canSeeIfModified:bool=False) -> None: #height and width is in characters
        self.rootObject = rootBody
        self.bgColor = bgColor
        self.textColor = textColor
        self.caretColor = caretColor
        self.bodyObject = tkinter.Text(self.rootObject, height=height, width=width, bg=bgColor, fg=textColor, insertbackground=caretColor)
        self.length = self.getLength()
        self.inputPrompt = inputPrompt  
        self.canSeeIfModified = canSeeIfModified   
    def pack(self) -> None:
        try:
            self.bodyObject.pack()
        except:
            print("cannot pack object, have you parsed the root body??")
        return None
        
    def writeRawText(self, data:str = "", startPoint:str = "end") -> None:
        #startPoint can be "1.0" to insert at the start or "end" to insert at the end"
        try:
            data = str(data)
            self.bodyObject.insert(chars=data, index=startPoint)
        except:
            print(f"Failed to write text from {self.bodyObject}, maybe you parsed the wrong object when initiating the terminal?? Or parsed the wrong args into this func??")
        return None
    def overwriteRawText(self, data:str = "") -> None:
        try:
            self.bodyObject.delete("1.0", "end")
            self.bodyObject.insert(chars=data, index="end")
        except:
            print(f"Failed to write text from {self.bodyObject}, maybe you parsed the wrong object when initiating the terminal?? Or parsed the wrong args into this func??")
        return None
    
    def getRawText(self, startPoint:str = "1.0", endPoint:str = "end") -> str|None: # returns as a string
        try:
            text = self.bodyObject.get(startPoint,endPoint)
            return text
        except:
            print(f"Failed to get text from {self.bodyObject}, maybe you parsed the wrong object when initiating the terminal?? Or parsed the wrong args into this func??")
            return None
        
    def getText(self, startPoint:str = "1.0", endPoint:str = "end") -> list[str]|None: # Returns each item as string in a list
        try:
            text = self.getRawText(startPoint, endPoint)
            out = text.split()
            return out
        except:
            print(f"Failed to get text from {self.bodyObject}, maybe you parsed the wrong object when initiating the terminal?? Or parsed the wrong args into this func??")
            return None
        
    def getLength(self) -> int:
        length = len(self.getRawText())
        return int(length)
    def write(self, data:str="") -> None:
        self.writeRawText(str(data.decode("utf-8"))+str(self.inputPrompt))    
        return None
    def run(self) -> None:
        
        
        return None
    def runCommand(self, command:str = "") -> None:
        
        
        return None
    def writeToBody(self) -> None:
        #self.bodyObject.
        return None

