class FileTypeError(BaseException): pass
class PythonCommandError(BaseException): pass
class DirectoryExistsError(BaseException): 
    def __str__():
        return "This directory already exists.."

