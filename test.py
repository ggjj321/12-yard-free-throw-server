import numpy as np

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

# 測試
a = (1, 1)
b = (4, 5)
c = (2, 0)
d = (6, 3)
intersection = find_intersection(a, b, c, d)
if intersection is not None:
    print("交點座標:", intersection)
else:
    print("沒有交點。")

