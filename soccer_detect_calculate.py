import cv2
import torch
import math
import numpy as np
import time
import result_data

mps_device = torch.device("mps")
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')
model.to(mps_device)

goal_upper_left_x  = []
goal_upper_left_y  = []
goal_upper_right_x = []
goal_upper_right_y = []
goal_down_left_x  = []
goal_down_left_y  = []
goal_down_right_x = []
goal_down_right_y = []

def soccerDetectAndDraw(img):
    results = model(img)
    df = results.pandas().xyxy[0]

    print(df)

    for data_index in range(len(df)):

        if (float(df.at[data_index, 'confidence']) > 0.4):
            start_point = (int(df.at[data_index, 'xmin']), int(df.at[data_index, 'ymin']))
            end_point = (int(df.at[data_index, 'xmax']), int(df.at[data_index, 'ymax']))

            img = cv2.rectangle(img, start_point, end_point, (255, 255, 0), 2)

    return img
