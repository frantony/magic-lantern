class Logger:
    def __init__(self, path):
        self.path = path

    def __log(self, severity, module, message):
        if(module is None):
            module = "UNK"
        print("[%s] [%s] %s" % (severity, module, message))

    def info(self, module, message):
        self.__log("INFO",module, message)

    def warn(self, module, message):
        self.__log("WARN",module, message)

    def error(self, module, message):
        self.__log("FAIL",module, message)
