rem @echo off
conda activate yolov4-gpu & python detect_video.py --weights ./checkpoints/yolov4-416 --size 416 --model yolov4 --video ./data/video/00017.mp4 --output ./detections/00017.avi -crop
pause