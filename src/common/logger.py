import logging

class Logging(logging.Logger):
    def __init__(self,
                 name='root',
                 logger_level= 'INFO',
                 file=None,
                 logger_format = " [%(asctime)s]  %(levelname)s %(filename)s [ line:%(lineno)d ] %(message)s"
                 ):
        super().__init__(name)

        self.logger = logging.getLogger(name)
        self.setLevel(logger_level)
        fmt = logging.Formatter(logger_format)
        
        if file:
            file_handler = logging.FileHandler(file,'a','utf-8')
            file_handler.setLevel(logger_level)
            file_handler.setFormatter(fmt)
            self.addHandler(file_handler)

        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setLevel(logger_level)
        self.stream_handler.setFormatter(fmt)
        self.addHandler(self.stream_handler)
