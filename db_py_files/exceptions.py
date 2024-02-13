
class NotSupportedError(Exception):
    """Custom exception for specific scenarios."""
    def __init__(self, message="An error occurred."):
        self.message = message
        super().__init__(self.message)
