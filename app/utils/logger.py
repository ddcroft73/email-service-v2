from pathlib import Path
from datetime import datetime
from datetime import time
import re
from os.path import join as os_join
from .file_handler import filesys
from config.settings import settings

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
        # to a default log file in the projects root directory under thedirectory 'logs'. and whenever
        # the size reaches 1000lines it will be archived.
        # Any filename not specified will go into the default log file.
        
"""

"""
walkthrough:

1. Logger is instantiated with or wothout the locations for the four log types, and a logger object is created.
   (From here all the necessary log files are created, if they do not already exist. )
2. 
"""


class ScreenPrinter:
    def to_screen(self, message: str, level: int) -> None:
        print(message)


class Logger:
    class DateTime:
        def __init__(self):
            print("DateTime class... created")

        @staticmethod
        def date_time_now() -> tuple[str]:
            """returns the formatted date and time in a tuple"""
            current_time: time = datetime.now()
            formatted_time: str = current_time.strftime("%Y-%m-%d %H:%M:%S")
            _date: str = formatted_time.split()[0]
            _time: str = formatted_time.split()[1]
            return (_date, _time)

    class Archive:
        """
        How the archiving will work:

        The maximum size of a log file is set at 1000 lines. This may need to be adjusted. If the class is instantiated
        with 'archive_log_files = True, then whenever a file reaches the max it will be moved to thearchive and a new one
        will be created in its place.
        1. a call is made to self.archive_logfile()
        2. rename the current logfile according to any logs that are in the archive already.
            - create a rename method eill take in the contents of the archive directory, and said logfile
            - rename the log according to whats already in the archive.
            -
        3. Create a new empty log file in this files inage.
        4. move the newly named file into the archive.

        There must be a way to check periodically the size of the logfiles. Add a new task to celery that will check every
        log, every 12 hours. Ifthe max is reached then themigration can commence.

        Asolutely not. ^^ All I need to do is check before every write action to every logfile. If the size == the limit
        then step away and make the migration. a few milliseconds every 1000 lines should not even be noticed at this point.
        Not for a good while anyway.
        """

        class ArchiveSubDirectories:
            DEBUG_DIR: str = "debug/"
            INFO_DIR: str = "info/"
            WARN_DIR: str = "warn/"
            ERROR_DIR: str = "error/"

            @classmethod
            def to_list(cls) -> list:
                # Get a dictionary of the class attributes
                attributes = vars(cls)
                # Filter the dictionary to only include the str attributes (the directories)
                directories = [
                    value
                    for name, value in attributes.items()
                    if isinstance(value, str) and name != "__module__"
                ]
                return directories

        def __init__(self, archive_directory: str, Level):
            """
            Most of this class is justma skeleton for now.
            """
            self.archive_directory = archive_directory
            self.Level = Level
            self.__create_archive_sub_directories()
            print("Archive class... created")

        def __create_archive_sub_directories(self) -> None:
            """
            Creates the sub directories to house the archived logs.
            If they already exist, nothing is done but a flag is returned to specify
            It exists. If it does not exist, it is created and a flag is returned saying it
            was just created.
            """
            for sub in self.ArchiveSubDirectories.to_list():
                state: str = filesys.mkdir(f"{self.archive_directory}{sub}")
                msg: str = "was " if state == "created" else "already"
                print(f"Sub directory '{sub}' {msg} {state}.")

        def get_line_cnt(self, file_name: str) -> int:
            """
               1. get contents of the file. 
               2. convert to list. 
               3. return the total items in list.
            """
            file_date: list[str] = filesys.get_contents(file_name).split("\n")
            return len(file_date)

        def get_sub_directory(self, level: int) -> str:
            sub_dir: str = ""
            if level == self.Level.INFO:
                sub_dir = self.ArchiveSubDirectories.INFO_DIR

            if level == self.Level.ERROR:
                sub_dir = self.ArchiveSubDirectories.ERROR_DIR

            if level == self.Level.WARN:
                sub_dir = self.ArchiveSubDirectories.WARN_DIR

            if level == self.Level.DEBUG:
                sub_dir = self.ArchiveSubDirectories.DEBUG_DIR

            return sub_dir

        def archive_logfile(self, logfile: str, level: int) -> None:
            """
                Moves the logfile from its old location to a new location after renaming .
                Creates a new logfile in its place and image.
                1. rename the current logfile. 
                2. Move the file to the appropriate archive directory. 
            """

            def get_new_filename(filename: str) -> str:

                def extract_date_time_from_string(input_string: str) -> tuple[str] | str:
                    datetime_pattern = r"\b(\d{4}-\d{2}-\d{2}) @ (\d{2}:\d{2}:\d{2})\b"
                    match = re.search(datetime_pattern, input_string)
                    if match:
                        return match.group(1), match.group(2)
                    else:
                        return "no_date_time"

                # get the first line from the log file.
                date_time_string: str = filesys.get_contents(filename).split("\n")[0]
                date, time = extract_date_time_from_string(date_time_string)
                orig_directory: str = "./" + filename.split("/")[1]
                fname_with_ext: str = filename.split("/")[-1]
                fname_no_ext: str = fname_with_ext.split(".")[0]

                return (
                    f"{orig_directory}/{fname_no_ext}_{date}_{time}.log",
                    f"{fname_no_ext}_{date}_{time}.log",
                )

            # Rename the current logfile.
            new_filename_full, new_filename_only = get_new_filename(logfile)
#           filesys.rename(logfile, new_filename_full)

            sub_dir: str = self.get_sub_directory(level)
            current_location: str = new_filename_full
            archive_location: str = f'{self.archive_directory}{sub_dir}{new_filename_only}'

            # Move it to its appropriate sub directory.
#           filesys.move(current_location, archive_location)

            print(f"\nRenamed: {logfile} to: {new_filename_full}")
            print(f"\nMoved: {current_location} TO: {archive_location}"            )

        def set_archive_directory(self, directory: str) -> None:
            """Will create the main directory for all logfiles to be archived to."""
            try:
                filesys.mkdir(directory)
            except Exception as exc:
                print(f"{str(exc)}")

    INFO_PRE: str = "INFO: "
    DEBUG_PRE: str = "DEBUG: "
    ERROR_PRE: str = "ERROR: "
    WARN_PRE: str = "WARNING: "

    FILE: int = 0
    SCREEN: int = 1
    BOTH: int = 2

    class Level:
        INFO: int = 10
        DEBUG: int = 20
        ERROR: int = 30
        WARN: int = 40
    
    LOG_DIRECTORY: str = settings.LOG_DIRECTORY    
    LOG_ARCHIVE_DIRECTORY: str = settings.LOG_ARCHIVE_DIRECTORY
    DEFAULT_LOG_FILE: str = settings.DEFAULT_LOG_FILE
    '''   
    LOG_DIRECTORY: str = "./logs"  # When the user specifies a file name for their logs, This will be prepended into the logs
    # path by default. Therfore you dont have to think about paths, just give it a file name .
    LOG_ARCHIVE_DIRECTORY: str = f"{LOG_DIRECTORY}/log-archives/"
    DEFAULT_LOG_FILE: str = f"{LOG_DIRECTORY}/app-logs.log"
    '''

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
        self.archive = self.Archive(
            archive_directory=self.LOG_ARCHIVE_DIRECTORY, 
            Level=self.Level
        )
        self.d_and_t = self.DateTime()
        self.prnt = ScreenPrinter()

        self.start_date: str = self.d_and_t.date_time_now()[0]
        self.start_time: str = self.d_and_t.date_time_now()[1]

        self.info_filename = info_filename
        self.error_filename = error_filename
        self.warning_filename = warning_filename
        self.debug_filename = debug_filename
        self.output_destination = output_destination  # FILE, SCREEN, or BOTH
        self.archive_log_files = archive_log_files 
        self.log_file_max_size = 5 #log_file_max_size    # How long a file can be by # of lines        

        self.__handle_file_setup()

    def __handle_file_setup(self) -> None:
        """
        Handles the creation of any user defined logfiles, the Default
        log file, and the vreation of the archive directory to be used when archiving
        excess lof files.
        """
        if self.archive_log_files:
            self.archive.set_archive_directory(self.LOG_ARCHIVE_DIRECTORY)

        if self.output_destination == self.FILE or self.output_destination == self.BOTH:
            file_names = [
                self.info_filename,
                self.error_filename,
                self.warning_filename,
                self.debug_filename,
            ]

            for file_name in file_names:
                if file_name is not None:
                    self.__set_log_filename(os_join(self.LOG_DIRECTORY, file_name))

            if any(filename is None for filename in file_names):
                self.__set_log_filename(self.DEFAULT_LOG_FILE)

    def __save_log(self, message: str, level: int, timestamp: bool) -> None:
        fname: str | None = None

        def add_final_touches(file_name: str, message: str):
            """
            last chance to set the filename, add timestamp if applicablew
            and \n final touches.
            """
            if file_name is None:
                file_name = self.DEFAULT_LOG_FILE
            else:
                file_name = os_join(self.LOG_DIRECTORY, file_name)

            if timestamp:
                date_time: str = f"{self.d_and_t.date_time_now()[0]} {self.d_and_t.date_time_now()[1]}"
                message = f"{message} § [{date_time}]\n"
            else:
                message += "\n"

            return (file_name, message)

        def ready_message(message: str) -> tuple[str]:
            """
            add a prefix to the message string, and reference
            the correct file to write to.
            """
            if level == self.Level.INFO:
                file_name = self.info_filename
                message = self.INFO_PRE + message

            elif level == self.Level.WARN:
                file_name = self.warning_filename
                message = self.WARN_PRE + message

            elif level == self.Level.DEBUG:
                file_name = self.debug_filename
                message = self.DEBUG_PRE + message

            elif level == self.Level.ERROR:
                file_name = self.error_filename
                message = self.ERROR_PRE + message

            return (file_name, message)

        def commit_message(message: str, file_name: str) -> None:
            """
            Handles writing log entries to the corresponding file.
            With the helpof a class created just to deal with the file system
            """
            try:
                filesys.write(file_name, message, "a")

            except FileNotFoundError as e:
                print(f"ERROR: Directory or file not found: {file_name}")

            except PermissionError as e:
                print(f"ERROR: Permission denied: {file_name}")

            except IsADirectoryError as e:
                print(f"ERROR: {file_name} is a directory, not a file")

            except OSError as e:
                print(f"ERROR: OS error occurred: {str(e)}")

            except Exception as e:
                print(
                    "ERROR: There was an error attempting a write action on:\n"
                    f"{fname}\n"
                    "Check path and spelling."
                )

        # Finalize the logfile entry.
        fname, message = ready_message(message=message)
        fname, message = add_final_touches(file_name=fname, message=message)
        #
        # Before Writiing to the file, check its size to see if it's time to archive it.
        #
        if self.archive.get_line_cnt(fname) >= self.log_file_max_size:
            self.archive.archive_logfile(logfile=fname, level=level)
            # create new log file with the original name
            self.__set_log_filename(fname)
        #
        # Write to the logfile
        #
        commit_message(message, fname)


    def __print_screen(self, message: str, level: int) -> None:
        """two guesses..."""
        msg_prefix: str

        if level == self.Level.INFO:
            msg_prefix = self.INFO_PRE

        elif level == self.Level.WARN:
            msg_prefix = self.WARN_PRE

        elif level == self.Level.DEBUG:
            msg_prefix = self.DEBUG_PRE

        elif level == self.Level.ERROR:
            msg_prefix = self.ERROR_PRE

        self.prnt.to_screen(f"{msg_prefix}{message}")

    def __route_output(self, message: str, level: int, timestamp: bool = False) -> None:
        """
        Whenever a log message is invoked, this method will route the output to the proper direction(s)
        """
        if self.output_destination == self.FILE:
            self.__save_log(message, level, timestamp)

        if self.output_destination == self.SCREEN:
            self.__print_screen(message)

        if self.output_destination == self.BOTH:
            self.__print_screen(message, level)
            self.__save_log(message, level, timestamp)


    def error(self, message: str, timestamp: bool = False) -> None:
        self.__route_output(message, self.Level.ERROR, timestamp)

    def info(self, message: str, timestamp: bool = False) -> None:
        self.__route_output(message, self.Level.INFO, timestamp)

    def warning(self, message: str, timestamp: bool = False) -> None:
        self.__route_output(message, self.Level.WARN, timestamp)

    def debug(self, message: str, timestamp: bool = False) -> None:
        self.__route_output(message, self.Level.DEBUG, timestamp)

    def __set_log_filename(self, file_name: str) -> None:
        """This method creates the initial file. If a file already exists, it does nada.
        Sets up the logfile.
        """
        message: str = (
            f" [ {file_name} ] created on {self.start_date} @ {self.start_time}\n\n"
        )

        if Path(file_name).exists():
            return

        try:
            filesys.write(file_name, message, "w")

        except FileNotFoundError as e:
            print(f"ERROR: Directory or file not found: {file_name}")

        except PermissionError as e:
            print(f"ERROR: Permission denied: {file_name}")

        except IsADirectoryError as e:
            print(f"ERROR: {file_name} is a directory, not a file")

        except OSError as e:
            print(f"ERROR: OS error occurred: {str(e)}")

        except Exception as e:
            print(
                "ERROR: There was an error attempting a write action on:\n"
                f"{file_name}\n"
                "Check path and spelling."
            )


logger = Logger(
    info_filename="INFO_log.log",
    debug_filename="DEbUG_log.log",
    error_filename=None,
    warning_filename=None,
    output_destination=Logger.FILE,
    archive_log_files=True,
    log_file_max_size=1000,
)
