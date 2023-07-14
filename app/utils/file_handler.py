from pathlib import Path
import shutil

class CreateDirectoryError(Exception):
    pass
class RemoveDirectoryError(Exception):
    pass
class FileWriteError(Exception):
    pass
class FileDeleteError(Exception):
    pass
class FileReadError(Exception):
    pass

class FileMoveError(Exception):
    pass

class FileHandler():
    def __init__(self):
        pass  # Notsure if I'll need it... just in case.
    
    def get_contents(self, file_name: str) -> str:
        '''
        Will return the contents of a file in a string.
        '''
        try:
            with open(file_name, 'r') as f:
                data: str = f.read()
            return data
        
        except FileNotFoundError:
            raise FileExistsError(f'Cannot find: {file_name}')
        
        except Exception as e:
            raise FileReadError(f'An Error occured trying to read: {file_name}.\n {str(e)}')
            

    def mkdir(self, directory: str) -> None:
        '''
        Will create a directory at the given Path. Will create any parent directories that do not exist.
        Will not raise an exception if the directory already exists. Just steps away.
        '''
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)

        except Exception as e:
            raise CreateDirectoryError(
                f"Error attempting to create the directory: {directory}\n{str(e)}"
            )
        
    def rmdir(self, directory: str) -> None:
        '''
        Will remove the given path. If there arefilesorsub directories in the path,
        They will be removed with no warnings or messages. Only responses will be on failure.
        '''
        try:
            shutil.rmtree(directory)

        except FileNotFoundError:
            raise FileExistsError(f'The directory: {directory}\nDoes not Exist..')
        
        except Exception as e:
            raise RemoveDirectoryError(f'An error occured trying to remove a directory: {str(e)} ')
        

    def write(self, file_name: str, data: str, mode: str) -> None:
        '''
        Writes data to a file. THe mode is adjustable so append, overwrite. All fairgame. 
        '''
        try:
            with open(file_name, mode) as f:
                f.write(data)

        except Exception as e:
            raise FileWriteError(
                f"An error occured attempting to write to file: {file_name} in {mode} mode.\n{str(e)}"
            )        
        

    def delete(self, file_name: str) -> None:
        '''
        Deletes a file in the given path. No response unless in the event of a failure.
        '''
        if self.exists(file_name):
            try:
               Path(file_name).unlink()

            except FileNotFoundError:
               raise FileDeleteError(f'The file {file_name} does not exist.')
            
            except Exception as e:
                raise FileDeleteError(
                    f'An error occured while attempting to delete a file: {str(e)}'
                )
            
    
    def exists(self, file_name: str) -> bool:
        '''
        Checks the existence of the file in the path. True if it lives, False if not. 
        '''
        if not Path(file_name).exists():
            return False
        return True

    def copy(self, old_locale: str, new_locale: str)-> None:    
        '''
        Will copy a file from one location to another, only if it exists.
        '''    
        if self.exists(old_locale):
            shutil.copy(old_locale, new_locale)        
        else:
            raise FileNotFoundError(f'THe file: {old_locale} could not be found.\nCopy process terminated.')    
    
    def move(self, old_locale: str, new_locale: str)-> None:
        '''
        Will move, the old copy will be deleted. A file from one spot to another, if it exists.
        '''
        if self.exists(old_locale):
            try:
               shutil.move(old_locale, new_locale)
               
            except Exception as e:
                raise FileMoveError(f'An error occured in the process of moving: {old_locale}\n{str(e)}')   
        else:
            raise FileNotFoundError(f'THe file: {old_locale} could not be found.\nCopy process terminated.')    
    

file_system = FileHandler()