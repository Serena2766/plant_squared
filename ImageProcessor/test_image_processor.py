
from pathlib import Path
from Camera import Camera
from ImageProcessor import ImageProcessor




cam = Camera(True, Path("./data/imgs/plants/1/1-cc-105.jpg"))
img_proc = ImageProcessor(cam,Path(__file__).parent/'plant_model.pth')
print(f"Before: {img_proc.plantPresent()} {img_proc.currentPlant()}")
img_proc.resetDetected()
print(f"After: {img_proc.plantPresent()} {img_proc.currentPlant()}")