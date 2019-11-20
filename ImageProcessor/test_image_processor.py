
from pathlib import Path
from Camera import Camera
from ImageProcessor import ImageProcessor


def test_init_good_camera():
    """
    Test of initialization of ImageProcessor with a good camera object
    """
    cam = Camera()
    img_proc = ImageProcessor(Path(__file__).parent/'plant_model.pth')
    img_proc._assign_camera(cam)
    assert isinstance(img_proc, ImageProcessor)
    assert isinstance(img_proc.camera, Camera)


def test_init_bad_camera():
    """
    Test of initialization of ImageProcessor with a bad camera object.
    Test fails if the _assign_camera() function fails to realize that
    the camera object is not good.
    """
    img_proc = ImageProcessor(Path(__file__).parent/'plant_model.pth')
    try:
        img_proc._assign_camera(None)
        assert False
    except TypeError:
        assert True


def test_init_file_not_exists():
    """
    Tests wether or not the ImageProcessor reacts properly to a
    non existent and/or malformed file object
    """
    try:
        img_proc = ImageProcessor(Path(__file__).parent/'FAKEFILE')
        assert False
    except FileNotFoundError:
        assert True

    try:
        img_proc = ImageProcessor(None)
        assert False
    except TypeError:
        assert True


def test_current_plant():    
    """
    Test of initialization of ImageProcessor with a fake camera object
    """
    cam = Camera(dummy=True, dummy_img=Path(__file__).parent /\
                 "data/imgs/plants/1/1-cc-0.jpg")
    img_proc = ImageProcessor(Path(__file__).parent/'plant_model.pth')
    img_proc._assign_camera(cam)
    assert img_proc.currentPlant() == img_proc.neural_net.NO_PLANT
    assert img_proc.plantPresent() == False


def test_add_plant_1():
    cam = Camera(dummy=True, dummy_img=Path(__file__).parent /\
                 "data/imgs/plants/1/1-cc-0.jpg")
    img_proc = ImageProcessor(Path(__file__).parent/'plant_model.pth')
    img_proc._assign_camera(cam)
    # Before it switches should be nothing present
    assert img_proc.currentPlant() == img_proc.neural_net.NO_PLANT
    assert img_proc.plantPresent() == False
    img_proc.resetDetected()    
    assert img_proc.currentPlant() == 0
    assert img_proc.plantPresent() == True

def test_add_plant_2():
    cam = Camera(dummy=True, dummy_img=Path(__file__).parent /\
                 "data/imgs/plants/2/2-ze-0.jpg")
    img_proc = ImageProcessor(Path(__file__).parent/'plant_model.pth')
    img_proc._assign_camera(cam)
    # Before it switches should be nothing present
    assert img_proc.currentPlant() == img_proc.neural_net.NO_PLANT
    assert img_proc.plantPresent() == False
    img_proc.resetDetected()    
    assert img_proc.currentPlant() == 1
    assert img_proc.plantPresent() == True

def test_add_plant_3():
    cam = Camera(dummy=True, dummy_img=Path(__file__).parent /\
                 "data/imgs/plants/3/3-ha-0.jpg")
    img_proc = ImageProcessor(Path(__file__).parent/'plant_model.pth')
    img_proc._assign_camera(cam)
    # Before it switches should be nothing present
    assert img_proc.currentPlant() == img_proc.neural_net.NO_PLANT
    assert img_proc.plantPresent() == False
    img_proc.resetDetected()    
    assert img_proc.currentPlant() == 2
    assert img_proc.plantPresent() == True

def test_add_plant_4():
    cam = Camera(dummy=True, dummy_img=Path(__file__).parent /\
                 "data/imgs/plants/4/4-fa-1.jpg")
    img_proc = ImageProcessor(Path(__file__).parent/'plant_model.pth')
    img_proc._assign_camera(cam)
    # Before it switches should be nothing present
    assert img_proc.currentPlant() == img_proc.neural_net.NO_PLANT
    assert img_proc.plantPresent() == False
    img_proc.resetDetected()    
    assert img_proc.currentPlant() == 3
    assert img_proc.plantPresent() == True


def test_remove_plant_1():
    cam = Camera(dummy=True, dummy_img=Path(__file__).parent /\
                 "data/imgs/plants/1/1-cc-132.jpg")
    img_proc = ImageProcessor(Path(__file__).parent/'plant_model.pth')
    img_proc._assign_camera(cam)
    
    img_proc.resetDetected()    
    assert img_proc.currentPlant() == 0
    assert img_proc.plantPresent() == True

    cam = Camera(dummy=True, dummy_img=Path(__file__).parent /\
                 "data/imgs/plants/5/5-no-10.jpg")
    img_proc._assign_camera(cam)
    img_proc.resetDetected() 
    assert img_proc.currentPlant() == img_proc.neural_net.NO_PLANT
    assert img_proc.plantPresent() == False


def test_remove_plant_2():
    cam = Camera(dummy=True, dummy_img=Path(__file__).parent /\
                 "data/imgs/plants/2/2-ze-222.jpg")
    img_proc = ImageProcessor(Path(__file__).parent/'plant_model.pth')
    img_proc._assign_camera(cam)
    
    img_proc.resetDetected()    
    assert img_proc.currentPlant() == 1
    assert img_proc.plantPresent() == True

    cam = Camera(dummy=True, dummy_img=Path(__file__).parent /\
                 "data/imgs/plants/5/5-no-443.jpg")
    img_proc._assign_camera(cam)
    img_proc.resetDetected() 
    assert img_proc.currentPlant() == img_proc.neural_net.NO_PLANT
    assert img_proc.plantPresent() == False


def test_remove_plant_3():
    cam = Camera(dummy=True, dummy_img=Path(__file__).parent /\
                 "data/imgs/plants/3/3-ha-189.jpg")
    img_proc = ImageProcessor(Path(__file__).parent/'plant_model.pth')
    img_proc._assign_camera(cam)
    
    img_proc.resetDetected()    
    assert img_proc.currentPlant() == 2
    assert img_proc.plantPresent() == True

    cam = Camera(dummy=True, dummy_img=Path(__file__).parent /\
                 "data/imgs/plants/5/5-no-99.jpg")
    img_proc._assign_camera(cam)
    img_proc.resetDetected() 
    assert img_proc.currentPlant() == img_proc.neural_net.NO_PLANT
    assert img_proc.plantPresent() == False



def test_remove_plant_4():
    cam = Camera(dummy=True, dummy_img=Path(__file__).parent /\
                 "data/imgs/plants/4/4-fa-1.jpg")
    img_proc = ImageProcessor(Path(__file__).parent/'plant_model.pth')
    img_proc._assign_camera(cam)
    
    img_proc.resetDetected()    
    assert img_proc.currentPlant() == 3
    assert img_proc.plantPresent() == True

    cam = Camera(dummy=True, dummy_img=Path(__file__).parent /\
                 "data/imgs/plants/5/5-no-4.jpg")
    img_proc._assign_camera(cam)
    img_proc.resetDetected() 
    assert img_proc.currentPlant() == img_proc.neural_net.NO_PLANT
    assert img_proc.plantPresent() == False




