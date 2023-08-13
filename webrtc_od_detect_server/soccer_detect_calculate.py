import cv2
import torch
import math

mps_device = torch.device("mps")
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')
model.to(mps_device)

class DetectionObject():
    def __init__(self):
        self.confidence = None
        self.x_min = None
        self.x_max = None
        self.y_min = None
        self.y_max = None  
        self.center_x = None
        self.center_y = None

    def set_data(self, confidence, x_min, x_max, y_min, y_max):
        self.confidence = confidence
        self.x_min = int(x_min)
        self.x_max = int(x_max)
        self.y_min = int(y_min)
        self.y_max = int(y_max)
        self.center_x = int((self.x_max + self.x_min) / 2)
        self.center_y = int((self.y_max + self.y_min) / 2)

def draw_four_corner(img, top_left, top_right, down_left, down_right):
    radius = 5
    color = (0, 0, 255)
    thickness = -1

    cv2.circle(img, top_left, radius, color, thickness)
    cv2.circle(img, top_right, radius, color, thickness)
    cv2.circle(img, down_left, radius, color, thickness)
    cv2.circle(img, down_right, radius, color, thickness)

    return img

def draw_skelation(img, top_left, top_right, down_left, down_right):
    color = (0, 255, 0) 
    thickness = 2 
        
    cv2.line (img, top_left, top_right, color, thickness)
    cv2.line (img, top_right, down_right, color, thickness)
    cv2.line (img, down_right, down_left, color, thickness)
    cv2.line (img, down_left, top_left, color, thickness)

    return img

def draw_split_line(img, top_left, down_left, top_right, top_basis, down_basis, left_basis, right_basis):
    color = (0, 255, 0) 
    thickness = 2 
    
    for x in range(1, 4):
            start = (top_left[0] + x * top_basis[0], top_left[1] + x * top_basis[1])
            end = (down_left[0] + x * down_basis[0], down_left[1] + x * down_basis[1])

            cv2.line (img, start, end, color, thickness)
        
    for y in range(1, 3):
        start = (top_left[0] + y * left_basis[0], top_left[1] + y * left_basis[1])
        end = (top_right[0] + y * right_basis[0], top_right[1] + y * right_basis[1])

        cv2.line (img, start, end, color, thickness)
    
    return img

def detect_ball_local(img, ball, top_left, top_right, down_left, top_basis, down_basis, right_basis, left_basis):
    distance_left = left_basis[0] ** 2 + left_basis[1] ** 2
    distance_right = right_basis[0] ** 2 + right_basis[1] ** 2 

    if distance_left > distance_right:
        hor_origin_point = top_left
        hor_basis = left_basis
    else:
        hor_origin_point = top_right
        hor_basis = right_basis
    
    distance_top = top_basis[0] ** 2 + top_basis[1] ** 2
    distance_down = down_basis[0] ** 2 + down_basis[1] ** 2 

    if distance_top > distance_down:
        vertical_origin_point = top_left
        vertical_basis = top_basis
    else:
        vertical_origin_point = down_left
        vertical_basis = down_basis

    hor_pos = 4
    vertical_pos = 5

    for hor_index in range(1, 4):
        if hor_origin_point[0] + (hor_index - 1) * hor_basis[0] < ball.center_x and ball.center_x < hor_origin_point[0] + hor_index * hor_basis[0] \
        and hor_origin_point[1] + (hor_index - 1) * hor_basis[1] < ball.center_y and ball.center_y < hor_origin_point[1] + hor_index * hor_basis[1]:
            hor_pos = hor_index - 1 
            break

    for vertical_index in range(1, 5):
        if vertical_origin_point[0] + (vertical_index - 1) * vertical_basis[0] < ball.center_x and ball.center_x < vertical_origin_point[0] + vertical_index * vertical_basis[0] \
        and vertical_origin_point[1] + (vertical_index - 1) * vertical_basis[1] < ball.center_y and ball.center_y < vertical_origin_point[1] + vertical_index * vertical_basis[1]:
            vertical_pos = vertical_index - 1
            break
    
    shoot_pos = hor_pos * 4 + vertical_pos + 1

    org = (50, 50)
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    fontScale = 1
    
    color = (255, 0, 0)
    
    thickness = 2
    
    # Using cv2.putText() method
    img = cv2.putText(img, str(shoot_pos), org, font, 
                    fontScale, color, thickness, cv2.LINE_AA)



def soccerDetectAndDraw(img):
    results = model(img)
    df = results.pandas().xyxy[0]

    detect_object = {
        "goal" : DetectionObject(),
        "ball" : DetectionObject(),
        "top_left" : DetectionObject(),
        "top_right" : DetectionObject(),
        "down_left" : DetectionObject(),
        'down_right' : DetectionObject()
    }

    for od_data_index in range(len(df)):
        object_name = df.loc[od_data_index, "name"]
        object_confidence = df.loc[od_data_index, "confidence"]
        if detect_object[object_name].confidence == None or float(object_confidence) > detect_object[object_name].confidence:
            detect_object[object_name].set_data(    float(df.loc[od_data_index, "confidence"]),
                                                    df.loc[od_data_index, "xmin"],
                                                    df.loc[od_data_index, "xmax"],
                                                    df.loc[od_data_index, "ymin"],
                                                    df.loc[od_data_index, "ymax"],
                                                )
    if detect_object["goal"].confidence != None:
        if detect_object["top_left"].confidence != None and \
            abs(detect_object["top_left"].center_x - detect_object["goal"].x_min) < 10 and \
            abs(detect_object["top_left"].center_y - detect_object["goal"].y_min) < 10:
            
            top_left = (detect_object["top_left"].center_x, detect_object["top_left"].center_y)
        else:
            top_left = (detect_object["goal"].x_min, detect_object["goal"].y_min)
        
        if detect_object["top_right"].confidence != None and \
            abs(detect_object["top_right"].center_x - detect_object["goal"].x_max) < 10 and \
            abs(detect_object["top_right"].center_y - detect_object["goal"].y_min) < 10:

            top_right = (detect_object["top_right"].center_x, detect_object["top_right"].center_y)
        else:
            top_right = (detect_object["goal"].x_max, detect_object["goal"].y_min)
        
        if detect_object["down_left"].confidence != None and \
            abs(detect_object["down_left"].center_x - detect_object["goal"].x_min) < 10 and \
            abs(detect_object["down_left"].center_y - detect_object["goal"].y_max) < 10:

            down_left = (detect_object["down_left"].center_x, detect_object["down_left"].center_y)
        else:
            down_left = (detect_object["goal"].x_min, detect_object["goal"].y_max)
        
        if detect_object["down_right"].confidence != None and \
            abs(detect_object["down_right"].center_x - detect_object["goal"].x_max) < 10 and \
            abs(detect_object["down_right"].center_y - detect_object["goal"].y_max) < 10:

            down_right = (detect_object["down_right"].center_x, detect_object["down_right"].center_y)
        else:
            down_right = (detect_object["goal"].x_max, detect_object["goal"].y_max)

        draw_four_corner(img, top_left, top_right, down_left, down_right)

        draw_skelation(img, top_left, top_right, down_left, down_right)

        top_basis = (int((top_right[0] - top_left[0]) / 4), int((top_right[1] - top_left[1]) / 4))
        down_basis = (int((down_right[0] - down_left[0]) / 4), int((down_right[1] - down_left[1]) / 4))
        left_basis = (int((down_left[0] - top_left[0]) / 3), int((down_left[1] - top_left[1]) / 3))
        right_basis = (int((down_right[0] - top_right[0]) / 3), int((down_right[1] - top_right[1]) / 3))

        draw_split_line(img, top_left, down_left, top_right, top_basis, down_basis, left_basis, right_basis)

        if detect_object["ball"].confidence != None:
            ball_height = detect_object["ball"].y_max - detect_object["ball"].y_min
            goal_height_right = down_right[1] - top_right[1]
            goal_height_left = down_left[1] - top_left[1]

            if goal_height_left / ball_height > 10 or goal_height_right / ball_height > 10:
                detect_ball_local(img, detect_object["ball"], top_left, top_right, down_left, top_basis, down_basis, right_basis, left_basis)

    return img