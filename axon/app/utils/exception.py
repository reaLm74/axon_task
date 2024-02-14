class OrderException(Exception):
    pass


class ProductNotExist(OrderException):
    pass


class ErrorCodeAttached(OrderException):
    pass


class ErrorCodeUsed(OrderException):
    def __init__(self, data):
        self.data = data


class BatchNone(OrderException):
    pass


class BatchClosed(OrderException):
    pass


class TaskNotFound(OrderException):
    pass
