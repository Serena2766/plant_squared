import torch
import torchvision
import torch.nn as nn
from torch.autograd import Variable
from torch import optim
import torch.nn.functional as F
import torchvision.transforms as transforms
from torch.utils.data.sampler import SubsetRandomSampler
from torchvision import datasets, transforms, models
import ipdb
import numpy as np
import torch.optim as optim
import matplotlib.pyplot as plt
import PIL
from pathlib import Path


class NeuralNetwork:
    """
    Class representing the neural network at the center of our plant
    recognition algorithm. It is initialized once at the startup of
    our code and then keeps itself loaded. 
    """
    LABELS = ["1", "2", "3", "4", "5"]
    NO_PLANT = 4
    def __init__(self, model_path: Path):
        """
        Load the proper weights and set some basic operations.

        :param model_path: The path to the file storing the model weights
        """

        if not isinstance(model_path, Path):
            raise TypeError("Model Path should be a Path type object")
        elif not model_path.exists():
            raise FileNotFoundError("Model weights file does not exist")

        self.IMG_SIZE = 224
        self.device = torch.device("cpu") # This will always be CPU on a Pi
        self.model=torch.load(model_path)
        self.model.eval()
        self.to_pil = transforms.ToPILImage()
        self.test_transforms = transforms.Compose(
            [transforms.Resize(self.IMG_SIZE),
             transforms.CenterCrop(self.IMG_SIZE),
             transforms.ToTensor()])


    def identify_plant(self, image: PIL.Image) -> int:
        """
        Predict the output label of a single image. Input must be a PIL image
        so that we can perform transforms on it before passing it into the
        neural network.

        image: Image of plant in PIL image type
        """

        if image is None:
            raise RuntimeError("Passed image is None and cannot be processed")
        elif not isinstance(image, PIL.Image.Image):
            raise TypeError(
                f"Image should be Pillow image type, not {type(image)}")
        image_tensor = self.test_transforms(image).float()
        image_tensor = image_tensor.unsqueeze_(0)
        net_in = Variable(image_tensor)
        net_in = net_in.to(self.device)
        output = self.model(net_in)
        index = output.data.cpu().numpy().argmax()
        return index


    def get_random_images(self, num: int, img_path: Path):
        """
        This function is used during the testing of the neural network to collect
        a random set of images to use for verification of results. 

        :param num: The number of examples to fetch
        """
        data = datasets.ImageFolder(img_path, transform=self.test_transforms)
        classes = data.classes
        indices = list(range(len(data)))
        np.random.shuffle(indices)
        idx = indices[:num]
        sampler = SubsetRandomSampler(idx)
        loader = torch.utils.data.DataLoader(data, 
                    sampler=sampler, batch_size=num)
        dataiter = iter(loader)
        images, labels = dataiter.next()
        return images, labels, classes