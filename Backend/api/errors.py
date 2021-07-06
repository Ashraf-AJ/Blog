class UnauthorizedError(Exception):
    def __init__(self, message, status_code=401):
        self.context = {"status_code": status_code}
        super().__init__(message)


class ForbiddenError(Exception):
    def __init__(self, message, status_code=403):
        self.context = {"status_code": status_code}
        super().__init__(message)
