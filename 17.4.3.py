import random

nums = [48, -10, 9, 38, 17, 50, -5, 43, 46, 12, 15, 18, 19]

num_a = random.randint(1, 5)
num_b = random.randint(6, 10)
nums[num_a:num_b] = []


print(nums)