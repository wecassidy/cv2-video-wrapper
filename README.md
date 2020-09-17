# VideoCapture

## Context manager

```python
with VideoCapture(0) as v:
    # etc. etc.
```

Automatically release the resources managed by the `VideoCapture`, even if an error occurs.

## Iterable

```python
with VideoCapture(0) as v:
	for frame in v:
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
```

Iterating over a `VideoCapture` gives the frames of the underlying video stream. If a read fails or the video is no longer open, the iterator ends.

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

The various properties accessed with `get(cv2.CAP_PROP_PROPERTY_NAME)` are mapped to `VideoCapture.property_name`. For convenience, `width` and `height` are provided as synonyms for `frame_width` and `frame_height`, respectively; and `shape` behaves like NumPy's shape and returns a `(width, height)` tuple.

## Transparent wrapper

`VideoCapture` subclasses `cv2.VideoCapture` and doesn't override any methods, so it can act as a drop-in replacement for `cv2.VideoCapture` without causing errors or affecting existing behaviour (ideally; this has not been extensively tested).

# VideoWriter

## Context manager

```python
with VideoWriter("file.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 30, (640, 480)) as vw:
	# etc. etc.
```

Automatically release the resources held by the `VideoWriter` even if an error occurs.

## Transparent wrapper

`VideoWriter` subclasses `cv2.VideoWriter` and doesn't override any methods, so it can act as a drop-in replacement for `cv2.VideoWriter` without causing errors or affecting existing behaviour (ideally; this has not been extensively tested).