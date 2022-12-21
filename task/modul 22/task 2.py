import os


def get_list_strings(strings_lst, file):

    path = os.path.abspath(file)
    file_zen = open(path, 'r')

    for i_line in file_zen:
        strings_lst.append(i_line)

    file_zen.close()

    return strings_lst


def display_reverse_order_strings(lst_zen):

    for index in range(len(lst_zen) - 1, -1, -1):

        if index == len(lst_zen) - 1:
            print(lst_zen[index], end='\n' * 2)
        else:
            print(lst_zen[index])


strings_list = list()
file_name = 'zen.txt'


list_zen = get_list_strings(strings_list, file_name)
display_reverse_order_strings(list_zen)






