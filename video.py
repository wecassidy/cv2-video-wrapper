import cv2


class VideoReader:
    """Wrapper around cv2.VideoCapture so that it can be used as a context manager"""

    def __init__(self, filename):
        self.video = cv2.VideoCapture(filename)
        self.stoppedIteration = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.video.release()
        return False

    def __iter__(self):
        return self

    def __next__(self):
        if not self.video.isOpened():
            self.stoppedIteration = True
            raise StopIteration

        ret, frame = self.read()
        if ret and not self.stoppedIteration:
            return frame
        else:
            # Iterators can't restart iteration after raising StopIteration
            self.stoppedIteration = True
            raise StopIteration

    def read(self):
        return self.video.read()

    @property
    def fps(self):
        return self.video.get(cv2.CAP_PROP_FPS)

    @property
    def width(self):
        return int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))

    @property
    def height(self):
        return int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    @property
    def shape(self):
        return (self.width, self.height)
