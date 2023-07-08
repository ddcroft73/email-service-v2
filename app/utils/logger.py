from pathlib import Path
from datetime import datetime
from datetime import time
from config.settings import settings
#
# Custom simple Logger class.
#
#  It's like Python Logger, but it works without having to be perfect. If I ask it to log something it does it
#  and I don't have to dig through docs to fivure out why my INFO logger is working.. somewhat, but my ERROR
#  logger is not. Or Why my INFO lofs are now going to the Celery log this time, and the screen the next.
#
#   I am not going to write this with different log levels.. basically, If it says log it, log it.
#  The type of message will be determined by the method called.


"""
  THINGS TO CONSIDER!!
The information you are currently asking for—`info_filename`, `error_filename`, and `destination`—should be sufficient for basic logging functionality. However, depending on your specific requirements, there might be additional information or configurations that you may want to consider:

1. Log file formats: You could allow the user to specify the format or structure of the log files. 
For example, they might want to include timestamps, log levels, or additional metadata in each log entry.

2. Log rotation settings: If you want to implement log rotation, you could provide options for the 
maximum file size or the maximum number of log files to keep. This allows the user to manage the size and 
number of log files generated over time.

3. Logging levels: While you mentioned that you want to keep it simple and only log INFO, ERROR, and 
WARNING messages, you could still consider providing an option for users to specify a logging level. This way, 
they can set a minimum logging level, and only messages at or above that level would be logged.

4. Logging configuration: Depending on the complexity of your logging requirements, you might want to allow 
users to configure additional settings like log format, logging output destinations (e.g., different log files 
for different modules or components), or log filtering based on specific criteria.

Remember to consider the specific needs of your application or project and determine if any additional information 
or configurations are required for your logger class.

Add the ability to rchive logs once they reach a certain size. 
Add a method so the user can set the archive directory.
Make sure there is a default for this
"""


class Logger:    
    # Need to define out theprefix and or suffix for each message type.
    INFO_PRE: str = 'INFO: '
    DEBUG_PRE: str = 'DEBUG: '
    ERROR_PRE: str = 'ERROR: '
    WARN_PRE: str = 'WARNING: '

    FILE: int = 0
    SCREEN: int = 1
    BOTH: int = 2

    INFO: int = 10
    DEBUG: int = 20
    ERROR: int = 30
    WARN: int = 40
    LOG_FILE_MAX_SIZE: int = 1000 #lines
    LOG_ARCHIVE_DIRECTORY: str = './log-archives'
    # set up a default file location incase the user doesnt enter a file loation for any log type,
    # but they select FILE. All logs will go to a common file in the root directory.        
    DEFAULT_LOG_FILE: str = f'./{settings.PROJECT_NAME}'
    
    timestamp: bool = True
    log_file_size: str 
    error_file_lifespan: int
    start_time: str
    start_date: str


    def __init__(
        self,
        info_filename: str = None,
        error_filename: str = None,
        warning_filename: str = None,
        debug_filename: str = None, 
        output_destination: str = FILE,
        debug_mode: bool = False,
    ):
        self.info_filename = info_filename
        self.error_filename = error_filename
        self.warning_filename = warning_filename
        self.debug_filename = debug_filename
        self.output_destination = output_destination
        self.debug_mode = debug_mode
        
        # setup the files that will be written to.        
        if self.output_destination == self.FILE or self.output_destination == self.BOTH:
            if self.info_filename:
                self.__set_filename(self.info_filename)

            if self.error_filename:
                self.__set_filename(self.error_filename)

            if self.warning_filename:
                self.__set_filename(self.warning_filename)

            if self.debug_filename:
                self.__set_filename(self.debug_filename)

            # This will allow a user toinstatntiate the class with minimal args, 
            # and still have output ported to a file. If any one is missing then that info
            # goes DEAFULT
            if self.output_destination == self.FILE:
                if (
                    self.info_filename == None or 
                    self.error_filename == None or 
                    self.warning_filename == None or
                    self.debug_filename == None
                ):
                    self.__set_filename(self.DEFAULT_LOG_FILE)

        # Grab the start time and Date to be inserted at the top of any logfile on creation.
        self.start_date, self.start_date = self.date_time_now()
        
        
    def __write_disk(self, msg: str, level: int):

        def __write_msg(msg: str, fname: str):            
            try:
              with open(fname, 'a') as f:                
                 f.write(msg)  

            except FileNotFoundError as err:
                print(f"Some how {fname} did not get created.\n{err}")                
            except:
                print(f"ERROR: There was an error attempting a write action on:  {fname}")                

        if level == self.INFO:
            fname = self.info_filename

        elif level == self.WARN:
            fname = self.warning_filename

        elif level == self.DEBUG:
            fname = self.debug_filename

        elif level == self.ERROR:
            fname = self.error_filename
        else:
            # if no file name is entered then write the file to the root directory
            if fname == "": fname == self.DEFAULT_LOG_FILE

        __write_msg(msg, fname)
                

    def __print_screen(self, msg: str):
        print(msg)       
    

    def __route_output(self, msg: str, level: int):
        ''' Whenever a log message is invoked, this method will route the output to the proper direction(s)
        '''
        if self.output_destination == self.FILE and self.output_destination != self.BOTH:
           self.__write_disk(msg, level)

        if self.output_destination == self.SCREEN:
            self.__print_screen(msg)

        if self.output_destination == self.BOTH:
            self.__print_screen(msg)
            self.__write_disk(msg, level)
    

    def __set_filename(self, filename: str):
       ''' This method creates the initial file. If a file already exists, it does nada.
       '''       
       msg: str = f' [ {filename} ] created on {self.start_date} @ {self.start_time}\n\n'

       if Path(filename).exists:
           return       
       with open(filename, 'w') as f:
           f.write(msg)
       

    
    def date_time_now(self) -> tuple[str]:
        ''' returns the formatted date andtimein a tuple
        '''
        current_time: time = datetime.now()
        formatted_time: str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        _date: str = formatted_time.split()[0]
        _time: str = formatted_time.split()[1]
        return (_date, _time)
        

    # logging methods
    def error(self, msg: str):
        self.__route_output(msg, self.error_filename, self.ERROR)

    def info(self, msg: str):        
        self.__route_output(msg, self.info_filename, self.INFO)

    def warning(self, msg: str):
        self.__route_output(msg, self.warning_filename, self.WARN)

    def debug(self, msg: str, wipe_before_log: bool = False):
        self.__route_output(msg, self.debug_filename), self.DEBUG

    def archive(self, level:int) -> None:
        ''''''
        pass
    def set_archive(self, directory: str) -> bool:
        ''''''
        pass


    '''
    def purge(self):
        # Purge the log files of info.
        pass

    def backup(self):   # Do I need this??
        # backup info and error logs, or both
        pass
    '''
    