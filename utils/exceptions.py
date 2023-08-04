def _errMsg(msg: str, e: BaseException):
    return f"{msg}, because: {e}"

class PipelineException(Exception):
    e: BaseException
    msg: str
    
    def __init__(self, msg: str, e: BaseException, *args: object) -> None:
        super().__init__(*args)
        self.msg = msg
        self.e = e

    def __str__(self) -> str:
        return _errMsg(self.msg, self.e)

class KaleException(PipelineException):
    pass

class AmarException(PipelineException):
    pass

class ElliotException(PipelineException):
    top: int

    def __init__(self, top: int, msg: str, e: BaseException, *args: object) -> None:
        super().__init__(msg, e, *args)
        self.top = top

    def __str__(self) -> str:
        return _errMsg(f"on top {self.top}, {self.msg}", self.e)