from ultralytics import YOLO # type: ignore

# YOLO modelini yükle.
model = YOLO("../models/yolov8s_100epochs_data2.pt")
