

class PixivError(Exception):
    pass


class UnmatchError(PixivError):
    def __init__(self, msg):
        super(UnmatchError, self).__init__()
        self.args = (msg,)