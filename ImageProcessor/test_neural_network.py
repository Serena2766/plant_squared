from NeuralNetwork import NeuralNetwork

import matplotlib.pyplot as plt
from tqdm import tqdm
from pathlib import Path


def test_acc_95():
    net = NeuralNetwork(Path('plant_model.pth'))
    TEST_DATA_DIR = Path('/home/xmay/Documents/3010ML/data/imgs/plants')
    images, labels, classes = net.get_random_images(1000, TEST_DATA_DIR)
    res = []
    print("\nVerifying accuracy is above 95%. Test n = 1000")
    for ii in tqdm(range(len(images))):
        image = net.to_pil(images[ii])
        index = net.identify_plant(image)
        res.append(labels[ii].eq(index).item())
    assert(sum(res)/len(res) >= 0.95)


def test_display_results():
    net = NeuralNetwork(Path('plant_model.pth'))
    TEST_DATA_DIR = Path('/home/xmay/Documents/3010ML/data/imgs/plants')
    images, labels, classes = net.get_random_images(5, TEST_DATA_DIR)
    fig=plt.figure(figsize=(10,10))
    for ii in range(len(images)):
        image = net.to_pil(images[ii])
        index = net.identify_plant(image)
        sub = fig.add_subplot(1, len(images), ii+1)
        res = int(labels[ii]) == index
        sub.set_title(str(classes[index]) + ":" + str(res))
        plt.axis('off')
        plt.imshow(image)
    plt.show()