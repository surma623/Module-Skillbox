pack = []
decoder = []
bad_pack = 0

number_pack = int(input('Введи кол-во пакетов: '))

for i_pack in range(number_pack):
    print('\nПакет номер', i_pack + 1)
    for i_bit in range(4):
        print(f'{i_bit + 1} бит', end=' ')
        number = int(input())
        pack.append(number)

    if pack.count(-1) <= 1:
        decoder.extend(pack)
    else:
        print('Слишком много ошибок!')
        bad_pack += 1

    pack = []

print('\nПолученное сообщение:', decoder)
print('Кол-во ошибок в сообщении:', decoder.count(-1))
print('Кол-во потерянных пакетов:', bad_pack)


