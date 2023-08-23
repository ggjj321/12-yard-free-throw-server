def print_data(data):
  for i in range(1, 13):
    print(data[i], end="")
    if i % 4 == 0:
      print()

def row_group():
  return [1,2,3,4], [5,6,7,8], [9,10,11,12]

def col_shoot_count(data, col):
  count = 0

  return count

def sum_of_col(data, arr):
  count = 0
  for ele in arr:
    for key in data:
      if key % 4 == ele:
        count += data[key]
  return count

def sum_of_row(data, arr):
  count = top = mid = bot = 0
  for key in data:
    if 1 <= key <= 4:
      top += data[key]
    elif 5 <= key <= 8:
      mid += data[key]
    elif 9 <= key <= 12:
      bot += data[key]
  for ele in arr:
    if ele == 1:
      count += top
    elif ele == 2:
      count += mid
    elif ele == 3:
      count += bot
  return count

def suggest(target, total_shoot_time, data):
    percentage = 0
    pivot_foot_bias = "right"
    hit_pos = "up"

    #get shooting accuracy

    percentage = data[target] / total_shoot_time

    if percentage >= 0.9:
      return {"percentage" : percentage, "pivot_foot_bias" : "超過90%的命中率繼續保持", "hit_pos" : ""}

    #get left right suggestion

    if target % 4 == 1:
      if sum_of_col(data, [1, 2]) <= sum_of_col(data, [3, 0]):
        pivot_foot_bias = "支撐腳腳尖往左移"
      else:
        if sum_of_col(data, [1]) / total_shoot_time > 0.8:
          pivot_foot_bias = "射門方向大致正確，將支撐腳對準目標方向提高準確度"
        else:
          if sum_of_col(data, [1]) < sum_of_col(data, [2, 3, 0]):
            pivot_foot_bias = "支撐腳腳尖往左移"
          elif sum_of_col(data, [1]) == sum_of_col(data, [2, 3, 0]):
            pivot_foot_bias = "支撐腳腳尖往左移一點"
          else:
            pivot_foot_bias = "方向正確但切記不要太往左邊偏動"

    elif target % 4 == 2:
      if sum_of_col(data, [3, 0]) > sum_of_col(data, [1, 2]):
        pivot_foot_bias = "支撐腳腳尖往左移一點"
      else:
        if sum_of_col(data, [2]) / total_shoot_time > 0.8:
          pivot_foot_bias = "射門方向大致正確，將支撐腳對準目標方向提高準確度"
        else:
          if sum_of_col(data, [1]) > sum_of_col(data, [3, 0]):
            pivot_foot_bias = "支撐腳腳尖往右移一點"
          elif sum_of_col(data, [1]) == sum_of_col(data, [3, 0]):
            pivot_foot_bias = "支撐腳對準目標並且擺動時往目標帶動球"
          else:
            pivot_foot_bias = "支撐腳腳尖往左移一點"

    elif target % 4 == 3:
      if sum_of_col(data, [3, 0]) < sum_of_col(data, [1, 2]):
        pivot_foot_bias = "支撐腳腳尖往右移一點"
      else:
        if sum_of_col(data, [3]) / total_shoot_time > 0.8:
          pivot_foot_bias = "射門方向大致正確，將支撐腳對準目標方向提高準確度"
        else:
          if sum_of_col(data, [0]) > sum_of_col(data, [1, 2]):
            pivot_foot_bias = "支撐腳腳尖往左移一點"
          elif sum_of_col(data, [0]) == sum_of_col(data, [1, 1]):
            pivot_foot_bias = "支撐腳對準目標並且擺動時往目標帶動球"
          else:
            pivot_foot_bias = "支撐腳腳尖往右移一點"

    elif target % 4 == 0:
      if sum_of_col(data, [1, 2]) >= sum_of_col(data, [3, 0]):
        pivot_foot_bias = "支撐腳腳尖往右移"
      else:
        if sum_of_col(data, [0]) / total_shoot_time > 0.8:
          pivot_foot_bias = "射門方向大致正確，將支撐腳對準目標方向提高準確度"
        else:
          if sum_of_col(data, [0]) < sum_of_col(data, [1, 2, 3]):
            pivot_foot_bias = "支撐腳腳尖往右移"
          elif sum_of_col(data, [1]) == sum_of_col(data, [3, 0]):
            pivot_foot_bias = "支撐腳腳尖往右移一點"
          else:
            pivot_foot_bias = "方向正確但切記不要太往右邊移動"

    #get top down suggestion

    top, mid, bot = row_group()
    if target in top:
      if sum_of_row(data, [1]) / total_shoot_time == 1:
        hit_pos = "高度完全正確"
      elif sum_of_row(data, [1]) / total_shoot_time >= 0.7:
        hit_pos = "高度大致正確，射門時大腿往上帶動求以此擊中目標高度"
      else:
        hit_pos = "擊球點再往下移並且大腿帶動球的幅度可以再高一些"

    elif target in mid:
      if sum_of_row(data, [2]) / total_shoot_time == 1:
        hit_pos = "高度完全正確"
      elif sum_of_row(data, [2]) / total_shoot_time >= 0.7:
        hit_pos = "高度大致正確，射門時大腿往上帶動求以此擊中目標高度"
      else:
        if sum_of_row(data, [1]) > sum_of_row(data, [3]):
          hit_pos = "擊球點往下移一些"
        elif sum_of_row(data, [1]) == sum_of_row(data, [3]):
          hit_pos = "踢擊球的中心往下偏一點的地方"
        else:
          hit_pos = "擊球點往上移一些"
    elif target in bot:
      if sum_of_row(data, [3]) / total_shoot_time == 1:
        hit_pos = "高度完全正確"
      elif sum_of_row(data, [3]) / total_shoot_time >= 0.7:
        hit_pos = "高度大致正確，射門時大腿擺動不用往上帶動球"
      else:
        hit_pos = "擊球點再往下移並且大腿不用帶動球往上"

    return {"percentage" : percentage, "pivot_foot_bias" : pivot_foot_bias, "hit_pos" : hit_pos}
