import cv2
import torch
import math
import numpy as np

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

def detectObject(df, image):
    horn_points = []
    goal_area = []
    boal_area = []
    for i in range(len(df)):
        if df.at[i, 'name'] == 'soccer' and float(df.at[i, 'confidence']) > 0.4:
            boal_area = detectSoccer(df, i, image)

        elif df.at[i, 'name'] == 'soccer-goal':
            goal_area = detectGoal(df, i, image)

        elif df.at[i, 'name'] == 'horn':
            horn_area = get_coordinate(df, i)

            horn_points.append(horn_area)
    return boal_area, goal_area, horn_points

def detectSoccer(df, i, image):
    boal_area = get_coordinate(df, i)
    start_point = (boal_area[0], boal_area[2])
    end_point = (boal_area[1], boal_area[3])
    cv2.rectangle(image, start_point, end_point, (255, 0, 0), 3)

    distance = 168.596 / (boal_area[3] - boal_area[2]) 

    cv2.putText(image, str(distance), (boal_area[0], boal_area[2]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3, cv2.LINE_AA)

    return boal_area

def detectGoal(df, i, image):
    goal_area = get_coordinate(df, i)
                                
    distance = 1820.24 / (goal_area[3] - goal_area[2]) 

    cv2.putText(image, str(distance), (goal_area[0], goal_area[2]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA)

    return goal_area

def getCenter(boal_area):
    return [(boal_area[1] + boal_area[0]) / 2, (boal_area[3] + boal_area[2]) / 2]

def get_coordinate(df, i):
  x_min = int(df.at[i, 'xmin'])
  x_max = int(df.at[i, 'xmax'])
  y_min = int(df.at[i, 'ymin'])
  y_max = int(df.at[i, 'ymax'])

  coordinate = [x_min, x_max, y_min, y_max]

  return coordinate


def get_coordinate(df, i):
  x_min = int(df.at[i, 'xmin'])
  x_max = int(df.at[i, 'xmax'])
  y_min = int(df.at[i, 'ymin'])
  y_max = int(df.at[i, 'ymax'])

  coordinate = [x_min, x_max, y_min, y_max]

  return coordinate


# goal_area[0]:xmin goal_area[1]:xmax goal_area[2]:ymin goal_area[3]:ymax
def in_goal_area(horn_point, goal_area): 
  horn_x_min = horn_point[0]
  horn_x_max = horn_point[1]
  horn_y_min = horn_point[2]
  horn_y_max = horn_point[3]

  goal_x_min = goal_area[0]
  goal_x_max = goal_area[1]
  goal_y_min = goal_area[2]
  goal_y_max = goal_area[3]

  horn_points = [[horn_x_min, horn_y_min], [horn_x_min, horn_y_max], [horn_x_max, horn_y_min], [horn_x_max, horn_y_max]]

  for horn_point in horn_points:
    in_x_range = goal_x_min < horn_point[0] and horn_point[0] < goal_x_max
    in_y_range = goal_y_min < horn_point[1] and horn_point[1] < goal_y_max
    if in_x_range and in_y_range:
      return True

  return False
 


def find_closest_point(horn_point, goal_points):
    distances = []
    for goal_point in goal_points:
        distances.append(math.sqrt((horn_point[0] - goal_point[0])**2 + (horn_point[1] - goal_point[1])**2))
    return distances.index(min(distances))

def find_center(horn_point):
  return [int((horn_point[0] + horn_point[1]) / 2), int((horn_point[2] + horn_point[3]) / 2)]

def split_line(point1, point2, part_num):
  points = []

  x_length = int((point2[0] - point1[0]) / part_num)
  y_length = int((point2[1] - point1[1]) / part_num)

  for i in range(1, part_num):
    points.append([point1[0] + i * x_length, point1[1] + i * y_length])
  return points

def create_white_image(frame_height, frame_width):
  shape = (frame_height, frame_width, 3)

  origin_img = np.zeros(shape, np.uint8)
  origin_img.fill(255)
  return origin_img


def rating(boal_area, goal_area, image):   
    if boal_area and goal_area: 
        rate = (goal_area[3] - goal_area[2]) / (boal_area[1] - boal_area[0])
        rate_string = "rate:" + str(rate)
        cv2.putText(image, rate_string, (goal_area[0] - 50, goal_area[2] - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3, cv2.LINE_AA)
        return rate

def getGoalPoints(goal_area):
    goal_upper_left  = [goal_area[0], goal_area[2]]
    goal_upper_right = [goal_area[1], goal_area[2]]
    goal_down_left   = [goal_area[0], goal_area[3]]
    goal_down_right  = [goal_area[1], goal_area[3]]
    return [goal_upper_left, goal_upper_right, goal_down_left, goal_down_right]

def getHorns(horn_point, goalX, goalY):
    horn = find_center(horn_point)
    goalX.append(horn[0])
    goalY.append(horn[1])
    return horn

# need split
def getAllHornsCoordinates(horn_points, goal_area, image):
    goal_points = getGoalPoints(goal_area)
    check_point = []
    for horn_point in horn_points:
        if in_goal_area(horn_point, goal_area):
            cv2.circle(image, find_center(horn_point), 10, (255, 255), 10)
            i = find_closest_point(find_center(horn_point), goal_points)
            if i == 0:
                upper_left = getHorns(horn_point, goal_upper_left_x, goal_upper_left_y)
                check_point.append(0)
            if i == 1:
                upper_right = getHorns(horn_point, goal_upper_right_x, goal_upper_right_y)
                check_point.append(1)
            if i == 2:
                down_left = getHorns(horn_point, goal_down_left_x, goal_down_left_y)
                check_point.append(2)
            if i == 3:
                down_right = getHorns(horn_point, goal_down_right_x, goal_down_right_y)
                check_point.append(3)

    if 0 not in check_point:
        if goal_upper_left_x:
            upper_left = [int(np.mean(goal_upper_left_x)), int(np.mean(goal_upper_left_y))]
        else:
            upper_left = goal_points[0]
    if 1 not in check_point:
        if goal_upper_right_x:
            upper_right = [int(np.mean(goal_upper_right_x)), int(np.mean(goal_upper_right_y))]
        else:
            upper_right = goal_points[1]
    if 2 not in check_point:
        if goal_down_left_x:
            down_left = [int(np.mean(goal_down_left_x)), int(np.mean(goal_down_left_y))]
        else:
            down_left = goal_points[2]
    if 3 not in check_point:
        if goal_down_right_x:
            down_right = [int(np.mean(goal_down_right_x)), int(np.mean(goal_down_right_y))]
        else:
            down_right = goal_points[3]

    return upper_left, upper_right, down_left, down_right

def drawBoarderLines(image, upper_left, upper_right, down_left, down_right):
    cv2.line(image, upper_left, upper_right, (0, 0, 255), 5)
    cv2.line(image, upper_right, down_right, (0, 0, 255), 5)
    cv2.line(image, down_right, down_left, (0, 0, 255), 5)
    cv2.line(image, down_left, upper_left, (0, 0, 255), 5)

def splitGoalArea(image, hor_up, hor_down, straight_left, straight_right):
    for x in range(3):
        cv2.line(image, hor_up[x], hor_down[x], (0, 0, 255), 5)
    
    for y in range(2):
        cv2.line(image, straight_left[y], straight_right[y], (0, 0, 255), 5)

def checkGoalIn(xmin, ymin, xmax, ymax, boal_center):
    checkX = False
    checkY = False
    if xmin <= boal_center[0] <= xmax:
        checkX = True
    if ymin <= boal_center[1] <= ymax:
        checkY = True
    return checkX and checkY

def getLength(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def judge_boal_shot_at_which_square(coordinate_x, coordinate_y):
    if 0 <= coordinate_x <= 0.25:
        square = 1
    elif 0.25 <= coordinate_x <= 0.5:
        square = 2
    elif 0.5 <= coordinate_x <= 0.75:
        square = 3
    elif 0.75 <= coordinate_x <= 1:
        square = 4
    
    if 0.33 <= coordinate_y <= 0.66:
        square += 4
    if 0.66 <= coordinate_y <= 1:
        square += 8
    
    return square

def calculate_score(square, targets):
    if square in targets:
        return 100

    seventy_targets = set()
    up_down_targets  = set()

    for target in targets:
        if target % 4 == 0:                             # right bound
            seventy_targets.update([target, target - 1])
        elif target % 4 == 1:                           # left bound
            seventy_targets.update([target, target + 1])
        else:
            seventy_targets.update([target - 1, target, target + 1])
     
    for target in seventy_targets:
        if target - 4 > 0:
            up_down_targets.update([target - 4])
        if target + 4 < 13:
            up_down_targets.update([target + 4])
    
    seventy_targets.update(up_down_targets)

    if square in seventy_targets:
        return 70
    
    return 40
