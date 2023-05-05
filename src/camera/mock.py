from .base import BaseCamera

class MockCamera(BaseCamera):
    '''
    A mocked camera implementation for usage in testing. It does nothing.
    '''

    def available(self):
        return True

    def start(self):
        print('Mock camera start()')

    def stop(self):
        print('Mock camera stop()')