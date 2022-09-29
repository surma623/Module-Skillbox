import math


def calculate_area_cylinder(rad, hei):

    side_area = 2 * math.pi * rad * hei
    area_circle = math.pi * rad ** 2
    full_area_cylinder = side_area + 2 * area_circle

    return side_area, full_area_cylinder


radius = int(input('Введите радиус: '))
height = int(input('Введите высоту: '))

result_side_area, result_full_cylinder  = calculate_area_cylinder(radius, height)

print('Площадь боковой поверхности целиндра равна {}'.format(round(result_side_area, 2)))
print('Полная площадь целиндра равна {}'.format(round(result_full_cylinder, 2)))