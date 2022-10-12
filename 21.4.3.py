def create_dict(data, template=None):

    template = dict()

    if isinstance(data, dict):
        return data
    elif isinstance(data, (int, float, str)):
        template[data] = data
        return template
    else:
        return None


def data_preparation(old_list):

    new_list = []

    for element in old_list:
        if create_dict(element):
            new_list.append(create_dict(element))

    return new_list


data = ['sad', {'sds': 23}, {43}, [12, 42, 1], 2323]

data = data_preparation(data)

print(data)