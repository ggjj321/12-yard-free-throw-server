import unittest
from soccer_detect_calculate import DetectionObject, is_ball_in_range, find_intersection, detect_ball_local, record_shoot_status
from suggest_calculator import suggest

import redis
import json

class TestCalculator(unittest.TestCase):

    def test_ball_locall_1(self):
        test_ball = DetectionObject()
        test_ball.set_data(0.99, 25, 75, 25, 75)

        top_left = (0, 0)
        top_right = (400, 0)
        down_left = (0, 300)
        down_right = (400, 300)

        top_basis = (int((top_right[0] - top_left[0]) / 4), int((top_right[1] - top_left[1]) / 4))
        down_basis = (int((down_right[0] - down_left[0]) / 4), int((down_right[1] - down_left[1]) / 4))
        left_basis = (int((down_left[0] - top_left[0]) / 3), int((down_left[1] - top_left[1]) / 3))
        right_basis = (int((down_right[0] - top_right[0]) / 3), int((down_right[1] - top_right[1]) / 3))

        result = detect_ball_local(test_ball, top_left, top_right, down_left, down_right, top_basis, down_basis, right_basis, left_basis)
        self.assertEqual(result, 1)
    
    def test_ball_locall_1(self):
        test_ball = DetectionObject()
        test_ball.set_data(0.99, 25, 75, 25, 75)

        top_left = (0, 0)
        top_right = (400, 0)
        down_left = (0, 300)
        down_right = (400, 300)

        top_basis = (int((top_right[0] - top_left[0]) / 4), int((top_right[1] - top_left[1]) / 4))
        down_basis = (int((down_right[0] - down_left[0]) / 4), int((down_right[1] - down_left[1]) / 4))
        left_basis = (int((down_left[0] - top_left[0]) / 3), int((down_left[1] - top_left[1]) / 3))
        right_basis = (int((down_right[0] - top_right[0]) / 3), int((down_right[1] - top_right[1]) / 3))

        result = detect_ball_local(test_ball, top_left, top_right, down_left, down_right, top_basis, down_basis, right_basis, left_basis)
        self.assertEqual(result, 1)

    def test_is_ball_in_range_safe(self):
        test_ball = DetectionObject()
        test_ball.set_data(0.99, 25, 75, 25, 75)

        block1_1_corner = (0, 0)
        block1_2_corner = (100, 0)
        block1_3_corner = (0, 100)
        block1_4_corner = (100, 100)

        result = is_ball_in_range(test_ball, block1_1_corner, block1_2_corner, block1_3_corner, block1_4_corner)
        self.assertEqual(result, True)
    
    def test_is_ball_in_range_out(self):
        test_ball1 = DetectionObject()
        test_ball1.center_x = 0
        test_ball1.center_y = 0

        block1_1_corner = (50, 50)
        block1_2_corner = (150, 50)
        block1_3_corner = (50, 150)
        block1_4_corner = (150, 150)

        result = is_ball_in_range(test_ball1, block1_1_corner, block1_2_corner, block1_3_corner, block1_4_corner)
        self.assertEqual(result, False)

        test_ball2 = DetectionObject()
        test_ball2.center_x = 75
        test_ball2.center_y = 0

        result = is_ball_in_range(test_ball2, block1_1_corner, block1_2_corner, block1_3_corner, block1_4_corner)
        self.assertEqual(result, False)

        test_ball3 = DetectionObject()
        test_ball3.center_x = 200
        test_ball3.center_y = 0

        result = is_ball_in_range(test_ball3, block1_1_corner, block1_2_corner, block1_3_corner, block1_4_corner)
        self.assertEqual(result, False)

        test_ball4 = DetectionObject()
        test_ball4.center_x = 200
        test_ball4.center_y = 100

        result = is_ball_in_range(test_ball4, block1_1_corner, block1_2_corner, block1_3_corner, block1_4_corner)
        self.assertEqual(result, False)

        test_ball5 = DetectionObject()
        test_ball5.center_x = 200
        test_ball5.center_y = 200

        result = is_ball_in_range(test_ball5, block1_1_corner, block1_2_corner, block1_3_corner, block1_4_corner)
        self.assertEqual(result, False)

        test_ball6 = DetectionObject()
        test_ball6.center_x = 200
        test_ball6.center_y = 100

        result = is_ball_in_range(test_ball6, block1_1_corner, block1_2_corner, block1_3_corner, block1_4_corner)
        self.assertEqual(result, False)

        test_ball7 = DetectionObject()
        test_ball7.center_x = 200
        test_ball7.center_y = 0

        result = is_ball_in_range(test_ball7, block1_1_corner, block1_2_corner, block1_3_corner, block1_4_corner)
        self.assertEqual(result, False)

        test_ball8 = DetectionObject()
        test_ball8.center_x = 100
        test_ball8.center_y = 0

        result = is_ball_in_range(test_ball7, block1_1_corner, block1_2_corner, block1_3_corner, block1_4_corner)
        self.assertEqual(result, False)

    def test_find_intersection_1(self):
        result = find_intersection(1, 0, 1, 2, 0, 1, 2, 1)
        self.assertEqual(result, (1, 1))
    
    def test_find_intersection_2(self):
        result = find_intersection(0, 0, 2, 2, 2, 0, 0, 2)
        self.assertEqual(result, (1, 1))

    def test_record_shoot_status(self):
        red_server = redis.Redis(host='127.0.0.1', port=6379)
        grid_shoot_data = {}
        for grid_index in range(12):
            grid_shoot_data[str(grid_index)] = 0
        red_server.set('shoot_time', 0)
        red_server.set('is_shoot_time', "True")

        grid_shoot_data_json = json.dumps(grid_shoot_data)        
        red_server.set("grid_shoot_data", grid_shoot_data_json)
        
        record_shoot_status(5)
        self.assertEqual(int(red_server.get('shoot_time')), 1)
        self.assertEqual(red_server.get('is_shoot_time').decode(), "False")
        grid_shoot_data_json = red_server.get("grid_shoot_data")

        grid_shoot_data = json.loads(grid_shoot_data_json)
        self.assertEqual(grid_shoot_data, {'0' : 0, '1' : 0, '2' : 0, '3' : 0, '4' : 0, '5' : 1, '6' : 0, '7' : 0,
                                           '8' : 0,  '9' : 0, '10' :0, '11' : 0})

    def test_suggest(self):
        target = 12
        total_shoot_time  = 10
        shoot_data = {}
        result = suggest(target, total_shoot_time, shoot_data)
        self.assertEqual(result, {"percentage" : 0, "pivot_foot_bias" : "right", "hit_pos" : "up"})

if __name__ == '__main__':
    unittest.main()
