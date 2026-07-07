"""
src/exception/__init__.py
 
Step 15 of the project flow.
Custom exception class that captures the file name and line number
where an error occurred, so every `raise MyException(e, sys) from e`
across the pipeline gives a precise, debuggable traceback.
"""
import sys
 
 
def error_message_detail(error: Exception, error_detail: sys) -> str:
    """
    Extracts detailed error information including file name,
    line number, and the error message.
 
    :param error: The exception that occurred.
    :param error_detail: The sys module used to get exception details.
    :return: A formatted error message string.
    """
    _, _, exc_tb = error_detail.exc_info()
 
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
 
    error_message = (
        f"Error occurred in python script: [{file_name}] "
        f"at line number [{line_number}]: {str(error)}"
    )
 
    return error_message
 
 
class MyException(Exception):
    """
    Custom exception class for handling errors in the pipeline.
    """
 
    def __init__(self, error_message: str, error_detail: sys):
        """
        Initializes MyException with a detailed error message.
 
        :param error_message: The error message (usually str(e)).
        :param error_detail: The sys module to extract traceback details.
        """
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail)
 
    def __str__(self) -> str:
        return self.error_message
 