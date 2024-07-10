class IcancException(Exception):
    def __init__(self, error, message, hint=None):
        super().__init__(error, message)
        self.error = error
        self.message = message
        self.hint = hint

class FoundException(IcancException):
    def __init__(self, entity, id, hint=None):
        super().__init__(
            f"{entity} found",
            f"{id} already exists.",
            hint,
        )

class NotFoundException(IcancException):
    def __init__(self, entity, id, hint=None):
        super().__init__(
            f"{entity} not found",
            f"{id} does not exist.",
            hint,
        )

class UnknownPragmaException(IcancException):
    def __init__(self, pragma, id, hint=None):
        super().__init__(
            f"unknown pragma {pragma}",
            f"unknown pragma at {id}.",
            hint,
        )

class UnknownIncludeException(IcancException):
    def __init__(self, include, id, hint=None):
        super().__init__(
            "include not found",
            f"{include} not found at {id}",
            hint,
        )

class InvalidSourceException(IcancException):
    def __init__(self, entity, id, hint=None):
        super().__init__(
            f"invalid {entity}",
            f"invalid {entity} at {id}",
            hint,
        )
