import os

my_dir = 'Skillbox'


abs_path = os.path.abspath(os.path.join('..', '..', '..',  my_dir))
print(abs_path)

print('\n Содержимое директории:', my_dir)
for i_elem in os.listdir(abs_path):
    file = os.path.abspath(i_elem)
    print(file)