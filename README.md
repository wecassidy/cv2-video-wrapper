# VideoCapture

## Context manager

```python
with VideoCapture(0) as v:
    # etc. etc.
```

Automatically release the resources managed by the `VideoCapture`, even if an error occurs.

Code at [video.py:35-40](video.py#L35-L40) (`VideoCapture.__enter__` and `VideoCapture.__exit__`).

## Random access

```python
>>> with VideoCapture("video.avi") as v:
...     print(f"Video containts {len(v)} frames")
...     cv2.imwrite("frame_7.png", v[6])
Video contains 203 frames
>>> with VideoCapture(0) as v:
...     len(v)
TypeError: VideoCapture source does not support random access
```

For video sources that support it, allow random access to frames. If the source is a webcam or similar, calling `len` or indexing the video will throw a `TypeError`.

Code at [video.py:43-61](video.py#L43-L61) (`VideoCapture.__len__` and `VideoCapture.__getitem__`)

## Iterable

```python
with VideoCapture(0) as v:
    for frame in v:
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
```

Iterating over a `VideoCapture` gives the frames of the underlying video stream. If a read fails or the video is no longer open, the iterator ends.

Code at [video.py:64-78](video.py#L64-L78) (`VideoCapture.__iter__` and `VideoCapture.__next__`).

## Property access

```python
>>> with VideoCapture(0) as v:
... 	print(v.frame_width)
... 	print(v.shape)
... 	print(v.fps)
640
(640, 480)
30.0
```

The various properties accessed with `get(cv2.CAP_PROP_PROPERTY_NAME)` are mapped to `VideoCapture.property_name`. For convenience, `width` and `height` are provided as synonyms for `frame_width` and `frame_height`, respectively; and `shape` returns a `(height, width)` tuple.

Code at [video.py:81-98](video.py#L81-L98) (`VideoCapture.__getattr__` and `VideoCapture.__setattr__`, with the properties following those two methods handling special cases).

## Transparent wrapper

`VideoCapture` subclasses `cv2.VideoCapture` and doesn't override any methods, so it can act as a drop-in replacement for `cv2.VideoCapture` without causing errors or affecting existing behaviour (ideally; this has not been extensively tested).

# VideoWriter

## Context manager

```python
with VideoWriter("file.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 30, (640, 480)) as vw:
    # etc. etc.
```

Automatically release the resources held by the `VideoWriter` even if an error occurs.

Code at [video.py:146-151](video.py#L146-L151) (`VideoWriter.__enter__` and `VideoWriter.__exit__`).

## Transparent wrapper

`VideoWriter` subclasses `cv2.VideoWriter` and doesn't override any methods, so it can act as a drop-in replacement for `cv2.VideoWriter` without causing errors or affecting existing behaviour (ideally; this has not been extensively tested).
