class ImgData(object):
    def __init__(self, title,  pid, r18, view, praise, collection, height=-1, width=-1):
        self.title = title,
        self.pid = pid,
        self.r18 = r18
        self.height = height
        self.width = width
        self.view = view
        self.praise = praise
        self.collection = collection

    def __dict__(self):
        return {
            'title': self.title,
            'pid': self.pid,
            'r18': self.r18,
            'view': self.view,
            'praise': self.praise,
            'collection': self.collection,
            'height': self.height,
            'width': self.width,
        }
