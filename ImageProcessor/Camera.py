from pathlib import Path
import cv2


class Camera:
    """
    With OpenCV you can only have one listener registered to the camera at a
    time, so there can only be one version of this class shared among all
    components that require access.
    """
    IMAGE_RES = 480

    def __init__(self, dummy: bool = False, dummy_img: Path = None):
        """
        This can act as an interface to a physical device or as a dummy object
        during the testing of the ImageProcessor so that it can be performed
        without the peripherals plugged in. 

        :param dummy: Boolean indicating if this is a dummy object or not, only
                      True during testing. Must populate other parameter
        :param dummy_img: The path to the image that the dummy camera object
                          should pass to the caller. Must be present if creating
                          a dummy camera object
        """
        if dummy and not dummy_img:
            raise RuntimeError("Cannot create a dummy camera without image")

        # Initialize and set up camera
        if not dummy:
            self.cam = cv2.VideoCapture(0)
            self.cam.set(3, self.IMAGE_RES)
            self.cam.set(4, self.IMAGE_RES)
            self.video_on = False
            self.img = None
        else:
            if not isinstance(dummy_img, Path):
                raise TypeError("The dummy_img parameter should be Path type")
            if not dummy_img.exists():
                raise FileNotFoundError("Dummy image does not exist")
            self.img = cv2.imread(str(dummy_img.resolve()))

    def requestData(self):
        """
        Behavior of this function depends on the mode of this class. 

        If the class is in dummy mode it will serve up the stored image in raw
        image form. Otherwise it will read a single frame from the camera and
        return it to the caller.
        """
        if self.img is not None:
            return self.img
        else:
            ret_val, img = self.cam.read()
            if not ret_val:  # Camera has said something is wrong
                raise RuntimeError("Camera encountered error :(")
            return img


cv2.destroyAllWindows()
