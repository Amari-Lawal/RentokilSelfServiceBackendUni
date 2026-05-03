class RentokilException(Exception):
    """Base exception for Rentokil application"""

    pass


class ConfigurationError(RentokilException):
    """Exception raised for errors in the configuration (missing env vars, etc.)"""

    def __init__(self, message="Configuration error occurred"):
        self.message = message
        super().__init__(self.message)
