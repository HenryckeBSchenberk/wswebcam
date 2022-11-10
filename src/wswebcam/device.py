from cv2 import VideoCapture
from threading import Thread, Event
from sys import platform

class Camera:
    """
    This camera class is a wrapper for the cv2.VideoCapture class with a thread to update the frame.
    It also has a __enter__ and __exit__ method to be used with the 'with' statement.

    If not using the 'with' statement, you must call the stop() method to release the camera.

    When a new instance is created, it starts a thread to update the frame. If the camera is not found, it raises an exception.
    
    Example:
        with Camera(0) as camera:
            status, frame = camera.read()
            if status:
                cv2.imshow('frame', frame)
                cv2.waitKey(0)
        
        # or

        camera = Camera(0)
        status, frame = camera.read()
        if status:
            cv2.imshow('frame', frame)
            cv2.waitKey(0)

        camera.stop()


    """
    def __init__(self, source) -> None:
        self.stopped = Event()
        self.prefix = '' if platform.startswith('win') else '/dev/video'
        self.camera = VideoCapture(self.prefix+str(source))
        self.status, self.frame = self.camera.read()
        self.thread = Thread(target=self.update, args=(), daemon=True)
        self.thread.start()
        if not self.status:
            raise Exception("Camera not found")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def read(self):
        """
        Returns the status and the frame as a tuple
        """
        return (self.status, self.frame)

    def update(self):
        """
        This method is called in a thread to update the frame
        """
        while not self.stopped.is_set():
            self.status, self.frame = self.camera.read()
            if not self.status:
                print("Camera not found")
                
    def stop(self):
        self.stopped.set()
        self.thread.join(5)
        self.camera.release()