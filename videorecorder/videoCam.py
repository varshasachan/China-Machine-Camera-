from webcamvideostream import WebcamVideoStream

class VideoStream:
    class __VideoStream:
        def __init__(self):
            self.stream = WebcamVideoStream(src=0)

        
    instance = None

    def __init__(self, src=0):
        if not VideoStream.instance:
            VideoStream.instance = VideoStream.__VideoStream()

    def start(self):
        # start the threaded video stream
        return self.stream.start()

    def update(self):
        # grab the next frame from the stream
        self.stream.update()

    def read(self):
        # return the current frame
        return self.stream.read()

    def stop(self):
        # stop the thread and release any resources
        self.stream.stop()

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.instance, attr, value)