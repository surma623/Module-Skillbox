
def func():

    var = 1

    def f3():
        par = 2

        if 'var' not in locals():
            raise Exception
        print('var' in locals())

    #f3()

    def f4():
        par = 3
        print(var)
        if 'var' not in locals():
            raise Exception

    f4()


func()