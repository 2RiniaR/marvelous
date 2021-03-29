from abc import *


class Logger:
    __metaclass__ = ABCMeta

    @abstractmethod
    def write_row(self, msg):
        raise NotImplementedError()

    @abstractmethod
    def write_debug(self, msg):
        raise NotImplementedError()

    @abstractmethod
    def write_trace(self, msg):
        raise NotImplementedError()

    @abstractmethod
    def write_info(self, msg):
        raise NotImplementedError()

    @abstractmethod
    def write_warning(self, msg):
        raise NotImplementedError()

    @abstractmethod
    def write_error(self, msg):
        raise NotImplementedError()

    @abstractmethod
    def write_fatal(self, msg):
        raise NotImplementedError()
