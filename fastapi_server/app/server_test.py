import unittest
from firebase_data_process import *
from suggest import *

class TestCalculator(unittest.TestCase):
    def test_save_data_to_firebase_db(self):
        data = {"1" : 0, "2" : 5, "3" : 0, "4" : 0, "5" : 1, "6" : 0, "7" : 0, "8" : 0,  "9" : 0, "10" : 14, "11" : 0, "12" : 0}

        convert_data = {}

        for i in range(1, 13):
            convert_data[i] = data[str(i)]

        result = suggest(10, 20, convert_data)

        save_data_to_firebase_db(data, result["percentage"], result["pivot_foot_bias"], result["hit_pos"])


if __name__ == '__main__':
    unittest.main()