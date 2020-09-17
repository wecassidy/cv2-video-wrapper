import cv2

"""
Wrappers around the OpenCV VideoCapture and VideoWriter classes to give
them a more Pythonic interface
"""


class VideoCapture:
    """
    Wrapper around cv2.VideoCapture so that it can be used as a
    context manager. The underlying cv2.VideoCapture is accessible
    through VideoCapture.video.
    """

    def __init__(self, *args, **kwargs):
        """
        Set up the VideoCapture. All parameters are forwarded to the
        OpenCV VideoCapture object.
        """
        self.video = cv2.VideoCapture(*args, **kwargs)
        self.stoppedIteration = False

    def read(self):
        return self.video.read()

    ## Context manager
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.video.release()
        return False

    ## Iterable
    def __iter__(self):
        return self

    def __next__(self):
        if not self.video.isOpened():
            self.stoppedIteration = True
            raise StopIteration

        ret, frame = self.video.read()
        if ret and not self.stoppedIteration:
            return frame
        else:
            # Iterators can't restart iteration after raising StopIteration
            self.stoppedIteration = True
            raise StopIteration

    ## Video properties
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
