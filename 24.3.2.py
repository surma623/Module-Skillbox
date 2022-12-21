class Family:
    family_name = 'Common family'
    family_funds = 100000
    having_a_house = False

    def display_info(self):
        print('Surname of the family: {0}\nFamily funds: {1}\nHaving a house: {2}'.format(
            self.family_name,
            self.family_funds,
            self.having_a_house)
        )

    def earn_money(self, amount):
        self.family_funds += amount
        print('Earned {0} money! Current value: {1}'.format(amount, self.family_funds))

    def buy_a_house(self, house_price, discount=0):
        house_price -= house_price * discount / 100
        if self.family_funds >= house_price:
            self.family_funds -= house_price
            print('House purchased! Current money: {}'.format(self.family_funds))
        else:
            print('Not enough money!')


family = Family()
family.display_info()

print('\nTry to buy a house')
family.buy_a_house(10 ** 6)

family.earn_money(800000)

print('\nTry to buy a house')
family.buy_a_house(10 ** 6, 10)


