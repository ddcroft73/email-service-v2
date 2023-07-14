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

class FileHandler():
    def __init__(self):
        pass  # Notsure if I'll need it... just in case.
    
    def get_contents(self, file_name: str) -> str:
        try:
            with open(file_name, 'r') as f:
                data: str = f.read()
            return data
        
        except FileNotFoundError:
            raise FileExistsError(f'Cannot find: {file_name}')
        
        except Exception as e:
            raise FileReadError(f'An Error occured trying to read: {file_name}.\n {str(e)}')
            

    def mkdir(self, directory: str) -> None:
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)

        except Exception as e:
            raise CreateDirectoryError(
                f"Error attempting to create the directory: {directory}\n{str(e)}"
            )
        
    def rmdir(self, directory: str) -> None:
        try:
            shutil.rmtree(directory)

        except FileNotFoundError:
            raise FileExistsError(f'The directory: {directory}\nDoes not Exist..')
        
        except Exception as e:
            raise RemoveDirectoryError(f'An error occured trying to remove a directory: {str(e)} ')
        

    def write(self, file_name: str, data: str, mode: str) -> None:
        try:
            with open(file_name, mode) as f:
                f.write(data)

        except Exception as e:
            raise FileWriteError(
                f"An error occured attempting to write to file: {file_name} in {mode} mode.\n{str(e)}"
            )        
        

    def delete(self, file_name: str) -> None:
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
        if not Path(file_name).exists():
            return False
        return True

    def copy(self, old_locale: str, new_locale: str)-> None:        
        if self.exists(old_locale):
            shutil.copy(old_locale, new_locale)        
    
    def move(self, old_locale: str, new_locale: str)-> None:
        if self.exists(old_locale):
            shutil.move(old_locale, new_locale)


file_system = FileHandler()