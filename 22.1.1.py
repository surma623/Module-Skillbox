import os

file = 'admin.bat.'


abs_path = os.path.abspath(os.path.join('..', file))
rel_path = os.path.join('tasks not check', 'tasks', file)

print('Абсолютный путь до файла', abs_path)
print('Относительный путь до файла', rel_path)

