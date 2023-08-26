import cv2
import torch
import numpy as np
import redis
import json

mps_device = torch.device("mps")
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')
red_server = red_server = redis.Redis(host='127.0.0.1', port=6379)
if torch.backends.mps.is_available():
    print("mps")
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

def draw_shoot_result(img, result):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.5
    font_color = (0, 0, 255)  # BGR 格式的顏色，這裡是紅色
    font_thickness = 2

    cv2.putText(img, str(result), (50,50), font, font_scale, font_color, font_thickness)

def find_intersection(a, b, c, d):
    # 將點轉換為NumPy陣列以便進行向量運算
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    d = np.array(d)
    
    # 計算方向向量
    direction_p1 = b - a
    direction_p2 = d - c
    
    # 使用 NumPy 的 cross 函數計算交叉乘積
    cross_product = np.cross(direction_p1, direction_p2)
    
    # 檢查 cross_product 是否為零，以確定是否平行或共線
    if np.isclose(cross_product, 0):
        return None  # 平行或共線，沒有交點
    
    t = np.cross(c - a, direction_p2) / cross_product
    
    # 使用 t 值找到交點座標
    intersection = a + t * direction_p1
    
    return intersection

def is_ball_in_range(ball, block_1_corner, block_2_corner, block_3_corner, block_4_corner):
    # 1 2
    # 3 4
    if ball.center_x < block_1_corner[0] or ball.center_y < block_1_corner[1]:
        return False
    if ball.center_x > block_2_corner[0] or ball.center_y < block_2_corner[1]:
        return False
    if ball.center_x < block_3_corner[0] or ball.center_y > block_3_corner[1]:
        return False
    if ball.center_x > block_4_corner[0] or ball.center_y > block_4_corner[1]:
        return False
    return True


def detect_ball_local(ball, top_left, top_right, down_left, down_right, top_basis, down_basis, right_basis, left_basis):
    
    # order
    # 1  2  3  4  5
    # 6  7  8  9  10
    # 11 12 13 14 15
    # 16 17 18 19 20

    corner1 = top_left
    corner2 = (top_left[0] + top_basis[0], top_left[1] + top_basis[1])
    corner3 = (top_left[0] + 2 * top_basis[0], top_left[1] + 2 * top_basis[1])
    corner4 = (top_left[0] + 3 * top_basis[0], top_left[1] + 3 * top_basis[1])
    corner5 = top_right
    corner10 = (top_right[0] + right_basis[0], top_right[1] + right_basis[1])
    corner15 = (top_right[0] + 2 * right_basis[0], top_right[1] + 2 * right_basis[1])
    corner20 = down_right
    corner19 = (down_left[0] + 3 * down_basis[0], down_left[1] + 3 * down_basis[1])
    corner18 = (down_left[0] + 2 * down_basis[0], down_left[1] + 2 * down_basis[1])
    corner17 = (down_left[0] + down_basis[0], down_left[1] + down_basis[1])
    corner16 = down_left
    corner11 = (top_left[0] + 2 * left_basis[0], top_left[1] + 2 * left_basis[1])
    corner6 = (top_left[0] + left_basis[0], top_left[1] + left_basis[1])

    corner7 = find_intersection(corner2, corner17, corner6, corner10)
    corner8 = find_intersection(corner3, corner18, corner6, corner10)
    corner9 = find_intersection(corner4, corner19, corner6, corner10)
    corner12 = find_intersection(corner2, corner17, corner11, corner15)
    corner13 = find_intersection(corner3, corner18, corner11, corner15)
    corner14 = find_intersection(corner4, corner19, corner11, corner15)

    if is_ball_in_range(ball, corner1, corner2, corner6, corner7):
        return 1
    
    if is_ball_in_range(ball, corner2, corner3, corner7, corner8):
        return 2
    
    if is_ball_in_range(ball, corner3, corner4, corner8, corner9):
        return 3
    
    if is_ball_in_range(ball, corner4, corner5, corner9, corner10):
        return 4
    
    if is_ball_in_range(ball, corner6, corner7, corner11, corner12):
        return 5
    
    if is_ball_in_range(ball, corner7, corner8, corner12, corner13):
        return 6
    
    if is_ball_in_range(ball, corner8, corner9, corner13, corner14):
        return 7
    
    if is_ball_in_range(ball, corner9, corner10, corner14, corner15):
        return 8
    
    if is_ball_in_range(ball, corner11, corner12, corner16, corner17):
        return 9
    
    if is_ball_in_range(ball, corner12, corner13, corner17, corner18):
        return 10
    
    if is_ball_in_range(ball, corner13, corner14, corner18, corner19):
        return 11
    
    if is_ball_in_range(ball, corner14, corner15, corner19, corner20):
        return 12
    return 13

def record_shoot_status(locate):
    if locate != 13:
        grid_shoot_data_json = red_server.get("grid_shoot_data")
        grid_shoot_data = json.loads(grid_shoot_data_json)
        grid_shoot_data[locate] = grid_shoot_data[str(locate)] + 1
        grid_shoot_data_json = json.dumps(grid_shoot_data)

        shoot_time = int(red_server.get("shoot_time"))

        red_server.set('is_shoot_time', "False")
        red_server.set('shoot_time', shoot_time + 1)
        red_server.set('grid_shoot_data', grid_shoot_data_json)


def soccerDetectAndDraw(img):
    is_shoot_time = red_server.get("is_shoot_time").decode()

    print(is_shoot_time)

    if is_shoot_time == "False":
        return img

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
                is_shoot_time = red_server.get("shoot_time")
                if is_shoot_time:
                    locate = detect_ball_local(detect_object["ball"], top_left, top_right, down_left, down_right, top_basis, down_basis, right_basis, left_basis)
                    record_shoot_status(locate)
    return img
