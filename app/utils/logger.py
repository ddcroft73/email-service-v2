from pathlib import Path
from datetime import datetime
from datetime import time
from os.path import join as os_join

#
# "simple" Custom Logger class.
#
#  It's like Python Logger(not as robust), but it works without having to be perfect. If I ask it to log something it does it
#  and I don't have to dig through docs to figure out why my INFO logger is working.. somewhat, but my ERROR
#  logger is not. Or Why my INFO lofs are now going to the Celery log this time, and the screen the next.
#
#   I am not going to write this with different log levels(sortof).. basically, If it says log it, log it.
#  The type of message will be determined by the method called and where it is placed in the code.


"""
Add the ability to archive logs once they reach a certain size. 
Add a method so the user can set the archive directory.
Make sure there is a default for this

Use Celery to monitor the size of the log file directories... If the user has the auto archive flag set to True,
then check every 12 hours to see if the file size has been reached. once it is reached then call the celery task to 
archive the contents.

# User will config the logger on instantiation, 
        # If none of these args are used, Then User will get a logger that sends all log entries
        # to a default log file in the projects root directory under thedirectory 'logs'.
        # Any filename not specified will go into the default log file.
        
"""


class Logger:
    
    class DateTime():
        def __init__(self ):
            print("DateTime class... created")
            
        @staticmethod
        def date_time_now() -> tuple[str]:
            """returns the formatted date and time in a tuple"""
            current_time: time = datetime.now()
            formatted_time: str = current_time.strftime("%Y-%m-%d %H:%M:%S")
            _date: str = formatted_time.split()[0]
            _time: str = formatted_time.split()[1]
            return (_date, _time)


    class Archive():
        """
            How the archiving will work:

            The maximum size of a log file is set at 1000 lines. This may need to be adjusted. If the class is instantiated
            with 'archive_log_files = True, then whenever a file reaches the max it will be moved to thearchive and a new one
            will be created. 

            There must be a way to check periodically the size of the logfiles. Add a new task to celery that will check every
            log, every 12 hours. Ifthe max is reached then themigration can commence.
        """

        def __init__(self ):
            print("Archive class... created")                    
        
        def archive(
            self, level: int
        ) -> None:
            """
              Will take all files from their log locales, and migrate them to the new dir
              specified.
            """

        def migrate_archive(
            self,
        ) -> None:
            pass

        def set_archive_directory(
            self, directory: str, delete_old_archive_dir: bool = True
        ) -> bool:
            """
              Will create a directory for all logfiles to be archived to. If the user is using this command
              and an archive already exists, then migrate the logs into the new one and delete the old, or not
              Options, Options
            """
            Path(directory).mkdir(parents=True, exist_ok=True)


    INFO_PRE: str = "INFO: "
    DEBUG_PRE: str = "DEBUG: "
    ERROR_PRE: str = "ERROR: "
    WARN_PRE: str = "WARNING: "

    FILE: int = 0
    SCREEN: int = 1
    BOTH: int = 2

    INFO: int = 10
    DEBUG: int = 20
    ERROR: int = 30
    WARN: int = 40

    LOG_DIRECTORY: str = "./logs"  # When the user specifies a file name for their logs, This will be prepended into the logs
    # path by default. Therfore you dont have to think about paths, just give it a file name .
    LOG_ARCHIVE_DIRECTORY: str = f"{LOG_DIRECTORY}/log-archives"
    DEFAULT_LOG_FILE: str = f"{LOG_DIRECTORY}/app-logs.log"

    archive: Archive
    dandT: DateTime

    def __init__(
        self,
        info_filename: str = None,
        error_filename: str = None,
        warning_filename: str = None,
        debug_filename: str = None,
        output_destination: str = FILE,
        archive_log_files: bool = True,
        log_file_max_size: int = 1000,
    ) -> None:
        
        self.archive = self.Archive()
        self.dandT = self.DateTime()

        self.start_date: str = self.dandT.date_time_now()[0]
        self.start_time: str = self.dandT.date_time_now()[1]

        self.info_filename = info_filename  
        self.error_filename = error_filename  
        self.warning_filename = warning_filename       #  The locations(filename, loc will aleays be ./logs) of each log
        self.debug_filename = debug_filename  
        self.output_destination = output_destination   # FILE, SCREEN, or BOTH
        self.archive_log_files =  archive_log_files    # True if you want to archive the log files.
        self.log_file_max_size =  log_file_max_size    # How long a file can be by # of lines
        
        # set-up archive storage
        if self.archive_log_files:
            self.archive.set_archive_directory(self.LOG_ARCHIVE_DIRECTORY)

        # setup any custom log filenames
        if self.output_destination == self.FILE or self.output_destination == self.BOTH:
            if self.output_destination == self.FILE or self.output_destination == self.BOTH:
                filenames = [self.info_filename, self.error_filename, self.warning_filename, self.debug_filename]
                for filename in filenames:
                    if filename is not None:
                        self.__set_log_filename(os_join(self.LOG_DIRECTORY, filename))

                # setup default log for any that did not get created.
                if all(filename is None for filename in filenames):
                    self.__set_log_filename(self.DEFAULT_LOG_FILE)

           

    def __write_disk(
        self, msg: str, level: int, timestamp: bool
    ) -> None:                
        
        fname: str|None = None
        
        def add_final_touches(file_name: str, message: str):
            '''
            last chance to set the filename, add timestamp if applicablew
            and \n final touches.
            '''
            if file_name is None:
                file_name = self.DEFAULT_LOG_FILE
            else:
                file_name = os_join(self.LOG_DIRECTORY, file_name)
                
            if timestamp:
                date_time: str = f"{self.dandT.date_time_now()[0]} {self.dandT.date_time_now()[1]}"
                message = f"{message} - [{date_time}]\n"
            else:
                message += "\n"

            return (
                file_name, 
                message
            )
        
        def ready_message(message: str) -> tuple[str]:
            '''
              add a prefix to the message string, and reference
              the correct file to write to.
            '''
            if level == self.INFO:
                file_name = self.info_filename
                message = self.INFO_PRE + message

            elif level == self.WARN:
                file_name = self.warning_filename
                message = self.WARN_PRE + message

            elif level == self.DEBUG:
                file_name = self.debug_filename
                message = self.DEBUG_PRE + message

            elif level == self.ERROR:
                file_name = self.error_filename
                message = self.ERROR_PRE + message

            return (
                file_name, message    
            )


        def commit_message(msg: str, fname: str) -> None:
            try:
                with open(fname, "a") as f:
                    f.write(msg)

            except FileNotFoundError as err:
                print(f"Some how {fname} did not get created.\n{err}")
            except:
                print(
                    "ERROR: There was an error attempting a write action on:\n"
                   f"{fname}\n"
                    "Check path and spelling."
                )


        fname, msg = ready_message(message=msg)       
        fname, msg = add_final_touches(
            file_name=fname, 
            message=msg
        )
        commit_message(msg, fname)
        


    def __print_screen(self, msg: str, level: int) -> None:
        """two guesses..."""
        msg_prefix: str
        if level == self.INFO:
            msg_prefix = self.INFO_PRE

        elif level == self.WARN:
            msg_prefix = self.WARN_PRE

        elif level == self.DEBUG:
            msg_prefix = self.DEBUG_PRE

        elif level == self.ERROR:
            msg_prefix = self.ERROR_PRE
        else:
             raise ValueError(f"Invalid log level: {level}")

        print(msg_prefix, msg)

    def __route_output(self, msg: str, level: int, timestamp: bool = False):
        """Whenever a log message is invoked, this method will route the output to the proper direction(s)"""
        if self.output_destination == self.FILE:
            self.__write_disk(msg, level, timestamp)

        if self.output_destination == self.SCREEN:
            self.__print_screen(msg)

        if self.output_destination == self.BOTH:
            self.__print_screen(msg, level)
            self.__write_disk(msg, level, timestamp)


    def error(self, msg: str, timestamp: bool = False) -> None:
        self.__route_output(msg, self.ERROR, timestamp)

    def info(self, msg: str, timestamp: bool = False) -> None:
        self.__route_output(msg, self.INFO, timestamp)

    def warning(self, msg: str, timestamp: bool = False) -> None:
        self.__route_output(msg, self.WARN, timestamp)

    # My logic is flawed here: Figure out how to implement the 'wipe' flag.
    def debug(self, msg: str, wipe_before_log: bool = False, timestamp: bool = False) -> None:
        self.__route_output(msg, self.DEBUG, timestamp)

    def __set_log_filename(self, filename: str) -> None:
        """This method creates the initial file. If a file already exists, it does nada."""
        msg: str = ""f" [ {filename} ] created on {self.start_date} @ {self.start_time}\n\n"

        if Path(filename).exists():
            return

        try:
            with open(filename, "w") as f:
                f.write(msg)
        except:
            print(f"ERROR: Error creating logfile: {filename}")
                
    

logger = Logger(
    info_filename="INFO_log.log",
    debug_filename=None,
    error_filename=None,
    warning_filename=None,
    output_destination=Logger.FILE,
    archive_log_files=True,
    log_file_max_size=1000
)
