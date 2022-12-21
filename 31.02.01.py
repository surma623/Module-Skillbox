import re

text = 'How much wood would a woodchuck chuck if a woodchuck could chuck wood?'


result = re.match(r'wo', text)

print('Поиск в начале строки по шаблону', result)

print('=' * 40)

result = re.search(r'wo', text)

print('Поиск в строке по шаблону', result)
print(result.group(0))
print(result.start())
print(result.end())

print('=' * 40)

result = re.findall(r'wo', text)
print(result)

print('=' * 40)

result = re.sub(r'wo', 'ЗАМЕНА', text)
print(result)

print('=' * 40)




