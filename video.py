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

    ## Random access
    def __len__(self):
        l = self.frame_count
        if l < 0:
            raise TypeError("VideoCapture source does not support random access")
        return int(self.frame_count)

    def __getitem__(self, i):
        if 0 <= i < len(self):
            self.set(cv2.CAP_PROP_POS_FRAMES, i)
        elif -len(self) <= i < 0:
            self.set(cv2.CAP_PROP_POS_FRAMES, len(self) + i)
        else:
            raise IndexError(f"index {i} out of range")

        ret, frame = self.read()
        if ret:
            return frame
        else:
            raise RuntimeError(f"Couldn't read frame {i}")

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


class VideoWriter(cv2.VideoWriter):
    """
    Extend cv2.VideoWriter to provide a context manager.
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        return False


# Test: stream video from a webcam to window
if __name__ == "__main__":
    with VideoCapture(0) as webcam:
        for frame in webcam:
            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    cv2.destroyAllWindows()
