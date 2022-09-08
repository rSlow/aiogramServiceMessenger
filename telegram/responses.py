__all__ = (
    "OKResponse",
    "ErrorResponse"
)


class Response:
    OK = "ok"
    ERROR = "error"

    def __init__(self):
        self.response_dict = {}

    @property
    def as_response(self):
        return self.response_dict


class OKResponse(Response):
    def __init__(self, **kwargs):
        super().__init__()
        self.response_dict = {
            "status": self.OK
        }
        self.response_dict.update(kwargs)


class ErrorResponse(Response):
    def __init__(self, error_message):
        super().__init__()
        self.response_dict = {
            "status": self.OK,
            "error": error_message
        }
