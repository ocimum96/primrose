import logging

class Logger:
    log_format = "%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s"
    log_level = logging.DEBUG

    @staticmethod
    def getLogger(loggerName):
        logger = logging.getLogger(loggerName)

        #https://stackoverflow.com/questions/17745914/python-logging-module-is-printing-lines-multiple-times
        if not logger.hasHandlers():
            logger.setLevel(Logger.log_level)
            streamHandler = logging.StreamHandler()
            formatter = logging.Formatter(Logger.log_format)
            streamHandler.setFormatter(formatter)

            logger.addHandler(streamHandler)
        return logger