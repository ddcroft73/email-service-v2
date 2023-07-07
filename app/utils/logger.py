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
"""


class Logger:
    """
    Handles all logging issues. Logs to Screen, file, or both. Can log each type of message to it's own
    file, or log them all to one.
    """

    FILE: int = 0
    SCREEN: int = 1
    BOTH: int = 2

    INFO: int = 0
    ERROR: int = 1
    DEBUG: int = 2
    WARN: int = 3

    log_file_size: str
    timestamp: bool
    error_file_lifespan: int

    def __init__(
        self,
        info_filename: str = None,
        error_filename: str = None,
        warning_filename: str = None,
        default_filename: str = None,  # File if all in one.
        write_seperate_files: bool = False,  # User can opt to write each type of error in its own file, or all in one.
        output_destination: str = FILE,
        debug_mode: bool = False,
    ):
        self.info_filename = info_filename
        self.error_filename = error_filename
        self.warning_filename = warning_filename
        self.default_filename = default_filename
        self.write_seperate_files = write_seperate_files
        self.output_destination = output_destination
        self.debug_mode = debug_mode

        if self.output_destination == self.FILE or self.output_destination == self.BOTH:
            if self.info_filename:
                self.set_info_filename(self.info_filename)
            if self.error_filename:
                self.set_error_filename(self.error_filename)
            if self.warning_filename:
                self.set_warning_filename(self.warning_filename)
            if self.default_filename:
                self.set_default_filename(self.default_filename)

    def __log(self, level: int, message: str):
        # All messages will be written from here.  EX. user invokes logger.info()
        # logger.info() in turnwill call this method that then sends the message to screen, or file or both
        pass

    def __write(self, msg: str, filename: str):
        # Handle writing to disk
        pass

    def __write_screen(self, msg: str):
        pass
    def __set_info_filename(self, info_filename: str):
        pass

    def __set_error_filename(self, error_filename: str):
        pass

    def __set_warning_filename(sefl, warning_filename: str):
        pass

    def __set_default_filename(sefl, default_filename: str):
        pass



    # logging methods
    def error(self, msg: str):
        # Write error logs
        pass

    def info(self, msg: str):
        # take the message, decide where it goes, and then send it to its home

        # write info logs
        pass

    def warning(self, msg: str):
        pass
        # will wipe the files contents before it writes

    def debug(self, msg: str, wipe_before_log: bool = False):
        pass

    def purge(self):
        # Purge the log files of info.
        pass

    def backup(self):   # Do I need this??
        # backup info and error logs, or both
        pass

    