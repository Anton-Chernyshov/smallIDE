import subprocess
import os
import dirs
import smIDEerrors

def main() -> None:
 try:
    subprocess.run(["py", "smIDEmain.py"], shell=True)
 except:
    try:
       subprocess.run(["python" , "smIDEmain.py"], shell=True)
    except:
       raise smIDEerrors.PythonCommandError (f"Is python installed Globablly?? The File {__file__ } cannot access it")
if __name__ == "__main__":
    main()

