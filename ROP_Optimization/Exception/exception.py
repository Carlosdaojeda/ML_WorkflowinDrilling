import sys
from ROP_Optimization.logging.logger import logging

class ROPException(Exception):
    def __init__(self, error_message, error_details):
        # Convierte a string si viene un objeto Exception
        if isinstance(error_message, Exception):
            error_message = str(error_message)

        super().__init__(error_message)
        self.error_message = error_message

        # Extrae traceback
        exc_type, exc_value, exc_tb = error_details.exc_info()
        if exc_tb:
            self.lineno = exc_tb.tb_lineno
            self.file_name = exc_tb.tb_frame.f_code.co_filename
        else:
            self.lineno = None
            self.file_name = None

        # Log automático
        logging.error(self.__str__())

    def __str__(self):
        return (
            f"Error occured in python script name [{self.file_name}] "
            f"line number [{self.lineno}] "
            f"error message [{self.error_message}]"
        )





'''if __name__ == "__main__":
    try:
        logger.info("Enter the try block")
        a = 1 / 0  # Provoca ZeroDivisionError
    except Exception as e:
        raise ROPException(e, sys)'''
