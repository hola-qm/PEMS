#Class Walmart

# Exists as an foreign member of the
# community where it just sells goods but doesn't reinvest
# in the community
import abcEconomics as abce


class Walmart(abce.Agent):
    def init(self,family_name,money,food):
        self.family_name = family_name
        self.create('money', money)
        self.create('food', food)

    # 0 = food, 1 = clothes, 2 = plumbing
    def sell_goods(self,good):
        if good == 1:
            for offer in self.get_offers('food'):
                if offer.price >= 0 and self['food'] > 0:
                    self.accept(offer)
                    return offer.price * offer.quantity
                else:
                    return -1
        else:
            for offer in self.get_offers('other'):
                if offer.price >= 0 and self['other'] > 0:
                    self.accept(offer)
                    return offer.price * offer.quantity
                else:
                    return -1

    def print_possessions(self):
        print((self.possessions()))


    def get_name(self):
       return self.family_name