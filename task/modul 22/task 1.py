import os


def record_file(abs_path):

    file_name_numbers = open(path, 'r')
    file_name_answer = open('answer.txt', 'w')

    read_file = file_name_numbers.read()
    file_name_answer.write(read_file)

    file_name_numbers.close()
    file_name_answer.close()


file_name = 'numbers.txt'
path = os.path.abspath(file_name)
record_file(path)
