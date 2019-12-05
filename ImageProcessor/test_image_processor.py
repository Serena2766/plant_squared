
from pathlib import Path
from Camera import Camera
from ImageProcessor import ImageProcessor


def test_init_good_camera():
    """
    Test of initialization of ImageProcessor with a good camera object
    """
    print("\n")
    print("Trying to find camera")
    try:
        cam = Camera()
        assert(False)
    except:
        print("No physical camera found, using software camera")
        cam = Camera(dummy=True, dummy_img=Path(__file__).parent /\
                    "data/imgs/plants/1/1-cc-0.jpg")
    img_proc = ImageProcessor(Path(__file__).parent/'plant_model.pth')
    img_proc._assign_camera(cam)
    assert isinstance(img_proc, ImageProcessor)
    assert isinstance(img_proc.camera, Camera)
    print("Camera successfully bound to image processor")
    print("\n")


def test_init_bad_camera():
    """
    Test of initialization of ImageProcessor with a bad camera object.
    Test fails if the _assign_camera() function fails to realize that
    the camera object is not good.
    """
    print("\n")
    img_proc = ImageProcessor(Path(__file__).parent/'plant_model.pth')
    try:
        print("Trying to assign bad camera object to processor")
        img_proc._assign_camera(None)
        assert False
    except TypeError:
        print("Assignment failed successfuly")
        assert True
    print("\n")


def test_init_file_not_exists():
    """
    Tests wether or not the ImageProcessor reacts properly to a
    non existent and/or malformed file object
    """
    print("\n")
    try:
        print("Trying to make image processor with invalid model file")
        img_proc = ImageProcessor(Path(__file__).parent/'FAKEFILE')
        assert False
    except FileNotFoundError:
        assert True

    try:
        print("Trying to create image processor with None as path")
        img_proc = ImageProcessor(None)
        assert False
    except TypeError:
        assert True
    print("\n")


def test_current_plant():
    print("\n")    
    """
    Test of initialization of ImageProcessor with a fake camera object
    """
    print("Making fake camera")
    cam = Camera(dummy=True, dummy_img=Path(__file__).parent /\
                 "data/imgs/plants/1/1-cc-0.jpg")
    img_proc = ImageProcessor(Path(__file__).parent/'plant_model.pth')
    img_proc._assign_camera(cam)
    assert img_proc.currentPlant() == img_proc.neural_net.NO_PLANT
    assert img_proc.plantPresent() == False
    print("\n")


def test_add_plant_1():
    print("\n")
    print("Creating fake camera with plant image")
    cam = Camera(dummy=True, dummy_img=Path(__file__).parent /\
                 "data/imgs/plants/1/1-cc-0.jpg")
    img_proc = ImageProcessor(Path(__file__).parent/'plant_model.pth')
    img_proc._assign_camera(cam)
    # Before it switches should be nothing present)
    assert img_proc.currentPlant() == img_proc.neural_net.NO_PLANT
    assert img_proc.plantPresent() == False
    print("No plant before update")
    img_proc.resetDetected()    
    assert img_proc.currentPlant() == 0
    assert img_proc.plantPresent() == True
    print(f"Plant {img_proc.currentPlant()} detected after update")
    print("\n")

def test_add_plant_2():
    print("\n")
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
    print(f"Plant {img_proc.currentPlant()} detected after update")
    print("\n")

def test_add_plant_3():
    print("\n")
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
    
    print(f"Plant {img_proc.currentPlant()} detected after update")
    print("\n")

def test_add_plant_4():
    print("\n")
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
    print(f"Plant {img_proc.currentPlant()} detected after update")
    print("\n")


def test_remove_plant_1():
    print("\n")
    cam = Camera(dummy=True, dummy_img=Path(__file__).parent /\
                 "data/imgs/plants/1/1-cc-132.jpg")
    img_proc = ImageProcessor(Path(__file__).parent/'plant_model.pth')
    img_proc._assign_camera(cam)
    
    img_proc.resetDetected()    
    assert img_proc.currentPlant() == 0
    assert img_proc.plantPresent() == True
    print(f"Plant detected {img_proc.plantPresent()} before removal")

    cam = Camera(dummy=True, dummy_img=Path(__file__).parent /\
                 "data/imgs/plants/5/5-no-10.jpg")
    img_proc._assign_camera(cam)
    img_proc.resetDetected() 
    assert img_proc.currentPlant() == img_proc.neural_net.NO_PLANT
    assert img_proc.plantPresent() == False
    print(f"Plant detected {img_proc.plantPresent()} after update")


def test_remove_plant_2():
    print("\n")
    cam = Camera(dummy=True, dummy_img=Path(__file__).parent /\
                 "data/imgs/plants/2/2-ze-222.jpg")
    img_proc = ImageProcessor(Path(__file__).parent/'plant_model.pth')
    img_proc._assign_camera(cam)
    
    img_proc.resetDetected()    
    assert img_proc.currentPlant() == 1
    assert img_proc.plantPresent() == True
    print(f"Plant detected {img_proc.plantPresent()} before removal")

    cam = Camera(dummy=True, dummy_img=Path(__file__).parent /\
                 "data/imgs/plants/5/5-no-443.jpg")
    img_proc._assign_camera(cam)
    img_proc.resetDetected() 
    assert img_proc.currentPlant() == img_proc.neural_net.NO_PLANT
    assert img_proc.plantPresent() == False
    print(f"Plant detected {img_proc.plantPresent()} after update")
    print("\n")


def test_remove_plant_3():
    print("\n")
    cam = Camera(dummy=True, dummy_img=Path(__file__).parent /\
                 "data/imgs/plants/3/3-ha-189.jpg")
    img_proc = ImageProcessor(Path(__file__).parent/'plant_model.pth')
    img_proc._assign_camera(cam)
    
    img_proc.resetDetected()    
    assert img_proc.currentPlant() == 2
    assert img_proc.plantPresent() == True
    print(f"Plant detected {img_proc.plantPresent()} before removal")

    cam = Camera(dummy=True, dummy_img=Path(__file__).parent /\
                 "data/imgs/plants/5/5-no-99.jpg")
    img_proc._assign_camera(cam)
    img_proc.resetDetected() 
    assert img_proc.currentPlant() == img_proc.neural_net.NO_PLANT
    assert img_proc.plantPresent() == False
    print(f"Plant detected {img_proc.plantPresent()} after update") 
    print("\n")


def test_remove_plant_4():
    print("\n")
    cam = Camera(dummy=True, dummy_img=Path(__file__).parent /\
                 "data/imgs/plants/4/4-fa-1.jpg")
    img_proc = ImageProcessor(Path(__file__).parent/'plant_model.pth')
    img_proc._assign_camera(cam)
    
    img_proc.resetDetected()    
    assert img_proc.currentPlant() == 3
    assert img_proc.plantPresent() == True
    print(f"Plant detected {img_proc.plantPresent()} before removal")

    cam = Camera(dummy=True, dummy_img=Path(__file__).parent /\
                 "data/imgs/plants/5/5-no-4.jpg")
    img_proc._assign_camera(cam)
    img_proc.resetDetected() 
    assert img_proc.currentPlant() == img_proc.neural_net.NO_PLANT
    assert img_proc.plantPresent() == False
    print(f"Plant detected {img_proc.plantPresent()} after update") 
    print("\n")



