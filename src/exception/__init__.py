class MyException(Exception):
    def __init__(self, error):
        super().__init__(f"Error: {error}")