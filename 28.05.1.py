

class File:
    def __init__(self, name, mode):
        self.name = name
        self.mode = mode
        self.file = None

    def __enter__(self):
        try:
            self.file = open(self.name, self.mode, encoding='UTF-8')
        except FileNotFoundError:
            print('Такого файла нет! Для работы в режиме записи, файл должен быть создан заранее')
        else:
            return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file is None:
            pass
        else:
            self.file.close()


with File('exampl.txt', "w") as file:
    if file is None:
        pass
    else:
        file.write('Привет')



