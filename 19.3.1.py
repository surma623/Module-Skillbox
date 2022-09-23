family_member = {
    "name": "Jane",
    "surname": "Doe",
    "hobbies": ["running", "sky diving", "singing"],
    "age": 35,
    "children": [
        {
            "name": "Alice",
            "age": 6
        },
        {
            "name": "Bob",
            "age": 8
        }
    ]
}

childrens_dict = {}
for child in family_member['children']:
    childrens_dict[child['name']] = child['age']

search_bob = childrens_dict.get('Bob', None)
if search_bob:
    print('Вот Bob!')
else:
    print('Boba нету(')

search_surname = family_member.get("surname", None)
if search_surname:
    print(family_member["surname"])
else:
    print('Nosurname')

