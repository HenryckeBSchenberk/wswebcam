from numpy import ndarray, frombuffer, uint8
from base64 import b64encode, b64decode
from cv2 import imencode, imdecode

def encode(image):
    """
    Convert a numpy array to a base64 string.
    """
    if isinstance(image, ndarray):
        image_jpg = imencode('.jpg', image)[1]
        encoded_64 = b64encode(image_jpg)
        encoded_utf8 = encoded_64.decode()
        return encoded_utf8
    return image

def decode(string, dtype=uint8):
    """
    Decode a base64 string to a numpy array.
    """
    original_json = b64decode(string)
    array = frombuffer(original_json, dtype=uint8)
    return imdecode(array, flags=1)

class Frame:
    """
    Store an data as base64 string and as numpy array.
    """
    def __init__(self, data):
        self.data = data
        self.array = decode(data)
        self.bytes = encode(data)
