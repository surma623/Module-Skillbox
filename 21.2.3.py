
def find_key(key, struct):

    if key in struct:
        return struct[key]

    for sub_struct in struct.values():
        if isinstance(sub_struct, dict):
            result = find_key(key, sub_struct)
            if result:
                break
    else:
        result = None

    return result

site = {
    'html': {
        'head': {
            'title': 'Мой сайт'
        },
        'body': {
            'h2': 'Здесь будет мой заголовок',
            'div': 'Тут, наверное, какой-то блок',
            'p': 'А вот здесь новый абзац'
        }
    }
}


search_key = input('Искомый ключ: ')

total_result = find_key(search_key, site)

if total_result:
    print(total_result)
else:
    print('Такого ключа в структуре сайта нет.')