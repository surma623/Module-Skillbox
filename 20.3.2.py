server_data = {
    "server": {
        "host": "127.0.0.1",
        "port": "10"
    },

    "configuration": {
        "access": "true",
        "login": "Ivan",
        "password": "qwerty"
    }
}

for i_dict, i_values in server_data.items():
    print(i_dict, ':')

    for j_key, j_val in i_values.items():
        print('\t{j_key}:{j_val}'.format(
            j_key=j_key,
            j_val=j_val
        ))
