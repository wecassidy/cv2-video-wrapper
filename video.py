import cv2

"""
Wrappers around the OpenCV VideoCapture and VideoWriter classes to give
them a more Pythonic interface
"""


class VideoCapture(cv2.VideoCapture):
    """
    Extend cv2.VideoCapture so that it can be used as a context
    manager and an iterator over the frames of the video.

    Context manager
    ---------------

    Ensures release() is called in case an error occurs

    Iterator
    --------

    Returns frames from read() as long as the capture is opened and
    the return value of read is Ture.
    """

    def __init__(self, *args, **kwargs):
        """
        Set up the VideoCapture. All parameters are forwarded to the
        OpenCV VideoCapture object.
        """
        super().__init__(*args, **kwargs)
        self.stoppedIteration = False

    ## Context manager
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        return False

    ## Iterable
    def __iter__(self):
        return self

    def __next__(self):
        if not self.isOpened():
            self.stoppedIteration = True
            raise StopIteration

        ret, frame = self.read()
        if ret and not self.stoppedIteration:
            return frame
        else:
            # Iterators can't restart iteration after raising StopIteration
            self.stoppedIteration = True
            raise StopIteration

    ## Video properties
    def __getattr__(self, name):
        """
        Used to convert
        VideoCapture.get(cv2.CAP_PROP_EXAMPLE_PROPERTY) to
        VideoCapture.example_property.
        """
        propertyName = f"CAP_PROP_{name.upper()}"
        if propertyName in cv2.__dict__:
            return self.get(cv2.__dict__[propertyName])
        else:
            return super().__getattr__(name)

    def __setattr__(self, name, value):
        propertyName = f"CAP_PROP_{name.upper()}"
        if propertyName in cv2.__dict__:
            return self.set(cv2.__dict__[propertyName], value)
        else:
            return super().__setattr__(name, value)

    @property
    def frame_width(self):
        return int(self.get(cv2.CAP_PROP_FRAME_WIDTH))

    @frame_width.setter
    def set_frame_width(self, width):
        return self.set(cv2.CAP_PROP_FRAME_WIDTH, width)

    @property
    def width(self):
        return self.frame_width

    @width.setter
    def set_width(self, width):
        self.frame_width = width

    @property
    def frame_height(self):
        return int(self.get(cv2.CAP_PROP_FRAME_HEIGHT))

    @frame_height.setter
    def set_frame_height(self, height):
        return self.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    @property
    def height(self):
        return self.frame_height

    @height.setter
    def set_height(self, height):
        self.frame_height = height

    @property
    def shape(self):
        return (self.width, self.height)

    @shape.setter
    def set_shape(self, shape):
        self.width, self.height = shape
