import sys
from networkSecurity.logging import logging

class NetworkSecurityException(Exception):

    def __init__(self,errorMessage,errorDetails:sys):

        self.errorMessage = errorMessage
        _,_,excTb = errorDetails.exc_info()

        self.lineno = excTb.tb_lineno
        self.fileName = excTb.tb_frame.f_code.co_filename

    def __str__(self):
        
        return "Error occurred in python script name [{0}] Line number [{1}] error message [{2}]".format(
            self.fileName, self.lineno, str(self.errorMessage))
