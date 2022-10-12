
def calculate_num(nums):

    if not nums:
        return 0

    else:
        sum_num = calculate_num(nums[1:])
        sum_num = sum_num + nums[0]

        return sum_num


numbers_list = [2, 3, 8, 11, 4, 6]
print(calculate_num(numbers_list))