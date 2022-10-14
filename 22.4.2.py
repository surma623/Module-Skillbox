import os


def rewrite_data(directory, result):

    for i_elem in os.listdir(directory):
        path = os.path.join(directory, i_elem)
        print(path)
        if os.path.isfile(path) and i_elem.endswith('.py'):
            cur_file = open(path, 'r', encoding='utf-8')

            for i_line in cur_file:
                result.write(i_line)

            result.write("\n " * 2 + "*" * 40 + "\n " * 2)

            cur_file.close()

        elif os.path.isdir(path):
            rewrite_data(path, result)

    return result


dir_name = 'Python_Basic'
dir_path = os.path.abspath(os.path.join('..', '..', 'practical lessons',  dir_name))


result_file = open('scripts.txt', 'a')

rewrite_data(dir_path, result_file)

result_file.close()