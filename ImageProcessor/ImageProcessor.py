from pathlib import Path

from NeuralNetwork import NeuralNetwork
from Camera import Camera
import PIL


class ImageProcessor:
    """
    The ImageProcessor class is responsible for co-ordincating between the
    classification portion of the codebase and the video streaming part of
    the codebase. There should only ever be one instance of it (more may cause
    memory issues with the Pi).
    """

    def __init__(self, model_path: Path):
        """
        Init function for ImageProcessor. Each processor will have its own NN
        but it cannot have its own camera (for reasons explained in the camera
        class). 
        """
        if model_path is None or not isinstance(model_path, Path):
            raise TypeError("Model path must be a valid path object")
        elif not model_path.exists():
            raise FileNotFoundError("Path for model does not exist")
        print("Creating neural network ... ")
        self.neural_net = NeuralNetwork(model_path)

        if self.neural_net is None:
            raise RuntimeError("Error initializing neural net")

        self.plant_present = False
        self.plant_id = self.neural_net.NO_PLANT
        self.camera = None

    def _assign_camera(self, camera: Camera) -> bool:
        """
        The function that must be used to link a camera object to this
        ImageProcessor object. If the operation is successful then function
        returns true, else returns false.
        """
        if camera is None or not isinstance(camera, Camera):
            raise TypeError("Camera must be a valid Camera type object")

        # Test the camera object to make sure it works properly
        try:
            _ = camera.requestData()
        except RuntimeError:
            return False

        self.camera = camera
        return True
        

    def resetDetected(self):
        """
        Called whenever the client Pi receives a plant reset signal from the
        arduino, this function updates the Image processors current status of
        which plant is present in the enclosure.
        """
        self.plant_id = 0
        img = self.camera.requestData()
        if not isinstance(img, PIL.Image.Image):
            img = self.neural_net.to_pil(img)
        plant_id = self.neural_net.identify_plant(img)
        if plant_id == self.neural_net.NO_PLANT:
            self.plant_present = False
            self.plant_id = self.neural_net.NO_PLANT
        else:
            self.plant_present = True
            self.plant_id = plant_id

    def currentPlant(self) -> int:
        """
        Getter function for current plant
        """
        return self.plant_id

    def plantPresent(self) -> bool:
        """
        Getter function for a plant being present in the enclosure
        """
        return self.plant_present
