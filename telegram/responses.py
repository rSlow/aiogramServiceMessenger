__all__ = (
    "OKResponse",
    "ErrorResponse"
)


class Response(dict):
    OK = "ok"
    ERROR = "error"

    def set_status(self, status):
        self["status"] = status


class OKResponse(Response):
    def __init__(self, **kwargs):
        super().__init__()
        self.set_status(self.OK)
        self.update(kwargs)


class ErrorResponse(Response):
    def __init__(self, error_message):
        super().__init__()
        self.set_status(self.ERROR)
        self["error"] = error_message
