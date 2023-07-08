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

Yse Celery to monitor the size of the log file directories... If the user has the auto archive flag set to True,
then check every 12 hours to see if the file size has been reached. once it is reached then call the celery task to 
archive the conotents.
"""


class Logger():    
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
    LOG_DIRECTORY: str = './logs'  # When the userspecifies a file name for their logs, They will be put into the logs
                                   # directory by default.Therfore you dont have to think about paths, just give them a
                                   # file name 
    LOG_ARCHIVE_DIRECTORY: str = f'./{LOG_DIRECTORY}/log-archives'
    # set up a default file location incase the user doesnt enter a file loation for any log type,
    # but they select FILE. All logs will go to a common file in the root directory.        
    DEFAULT_LOG_FILE: str = f'./{LOG_DIRECTORY}/{settings.PROJECT_NAME}'
    
    log_file_size: str 
    error_file_lifespan: int
    start_time: str
    start_date: str


    def __init__(
        self,
        info_filename: str=None,
        error_filename: str=None,
        warning_filename: str=None,
        debug_filename: str=None, 
        output_destination: str=FILE,
        default_log_file: str=None,
        archive_log_files: bool=False,
        archive_auto_backup: bool=True,
        log_file_max_size: int=1000
    ):
        # User has the option to cofig the logger on instantiation, or later via Logger.config()
        # If none of these args are used, Then User will get a logger that sends all log entries
        # to a default log file in the projects root directory in a directory under the projects name.
        # Logger will auto archive all logfiles when the total files reaches the max line size.
        self.info_filename = info_filename               #
        self.error_filename = error_filename             #
        self.warning_filename = warning_filename         #  The locations(filename, loc will aleays be ./logs) of each log
        self.debug_filename = debug_filename             #
        self.output_destination = output_destination     # FILE, SCREEN, or BOTH
        self.default_log_file = default_log_file         # Where to put log entries if no file was entered.
        self.archive_log_files = archive_log_files       # True if you want to archive the log files.
        self.archive_auto_backup = archive_auto_backup   # True if you want the log files to be auto archives when they reach the max file size.
        self.log_file_max_size = log_file_max_size       # How long a file can be by # of lines


        if self.archive_log_files:
             self.set_archive(self.LOG_ARCHIVE_DIRECTORY )

        if self.output_destination == self.FILE or self.output_destination == self.BOTH:
            if self.info_filename:
                self.__set_filename(self.info_filename)

            if self.error_filename:
                self.__set_filename(self.error_filename)

            if self.warning_filename:
                self.__set_filename(self.warning_filename)

            if self.debug_filename:
                self.__set_filename(self.debug_filename)

            # This will allow a user to instatntiate the class with minimal args, 
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

        self.start_date, self.start_date = self.date_time_now()
        
        
    def __write_disk(self, msg: str, level: int) -> None:
        fname: str | None = None

        def __write_msg(msg: str, fname: str) -> None:            
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
            pass

        # Did the user enter a name for theis level?
        if fname is None: 
            fname == self.DEFAULT_LOG_FILE

        __write_msg(msg, fname)
                

    def __print_screen(self, msg: str):
        ''' 
        '''
        print(msg)       
    

    def __route_output(self, msg: str, level: int):
        ''' Whenever a log message is invoked, this method will route the output to the proper direction(s)
        '''
        if self.output_destination == self.FILE:
           self.__write_disk(msg, level)

        if self.output_destination == self.SCREEN:
            self.__print_screen(msg)

        if self.output_destination == self.BOTH:
            self.__print_screen(msg)
            self.__write_disk(msg, level)
    



    # logging methods
    def error(self, msg: str, timestamp: bool=False):
        self.__route_output(msg, self.ERROR)

    def info(self, msg: str, timestamp: bool=False):        
        self.__route_output(msg, self.INFO)

    def warning(self, msg: str, timestamp: bool=False):
        self.__route_output(msg, self.WARN)

    def debug(self, msg: str, wipe_before_log: bool=False, timestamp: bool=False):
        self.__route_output(msg,  self.DEBUG)


    
    def __set_filename(self, filename: str):
       ''' This method creates the initial file. If a file already exists, it does nada.
       '''       
       msg: str = f' [ {filename} ] created on {self.start_date} @ {self.start_time}\n\n'

       if Path(filename).exists:
           return       
       with open(filename, 'w') as f:
           f.write(msg)       

    
    def date_time_now(self) -> tuple[str]:
        ''' returns the formatted date and time in a tuple
        '''
        current_time: time = datetime.now()
        formatted_time: str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        _date: str = formatted_time.split()[0]
        _time: str = formatted_time.split()[1]
        return (_date, _time)
        
    def archive(self, level:int) -> None:
        ''' Will take all files from their log locales, and migrate them to the new dir
            specified. 
        '''
        

    def set_archive(self, directory: str, delete_old_archive_dir: bool=True) -> bool:
        ''' 
         Will create a drectory for all logfiles to be archived to. If the user is using this command
         and an archive already exists, then migrate the logs into the new one and delete the old, or not
         Options, Options
        '''        
        Path(directory).mkdir(parents=True, exist_ok=True)


# this instantiation will send all your los to a default location in the project Root

logger = Logger()