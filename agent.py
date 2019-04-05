
import abcEconomics as abce

class Agent(abce.Agent):
    def init(self,family_name,money,food,other=None):
        self.family_name = family_name
        self.create('money', money)
        self.create('food', food)
        self.create('other', other)

    def buy_goods(self,agent_id,good):
        if good == 1:
            self.buy(('agent', agent_id), good='other', quantity=1, price=100)
        else:
            self.buy(('agent', agent_id), good='food', quantity=1, price=10)

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

    def return_quantity_of_good(self):
        return self['food']

    def return_curr_money(self):
        return self['money']

# Params: int num_agents (N) , array size N names, 
# array size N good_1, array size N good 2

# Returns: Array Nx4 with agent parameters built
def build_agent_parameters(num_agents, names, good1_name, good_1, 
    good2_name, good_2, good3_name, good3, good4_name, good4):
    
    key_name = ['family_name'] * num_agents
    key_good1 = [good1_name] * num_agents
    key_good2 = [good2_name] * num_agents
    key_good3 = [good3_name] * num_agents
    key_good4 = [good4_name] * num_agents

    agent_params = {}
    agent_list = []
    for x in range(num_agents):
        agent_params = {key_name[x]: names[x], key_good1[x]: good_1[x], 
                            key_good2[x]: good_2[x], key_good3[x]: good3[x],
                            key_good3[x]: good4[x]}

        agent_list.append(agent_params)

    return agent_list


