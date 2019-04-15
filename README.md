### Quipu Simulation ###

This code uses the ABCE economics library to simulate rural economic interactions.

The current working example is "sim_with_log.py"

This simulation creates a spreadsheet that logs transactions between local vendors and "Walmart" (a vendor that does not return money to the community)

The current sim allows for buying food and for buying raw materials

Each day, each vendor eats food. They also buy food, either from inside or outside the community.

Each week, each vendor purchases raw materials from inside or outside.


The parameters for the simulation can be set in sim_params_final.csv
You can set:
- % chance vendors buy food locally
- % chance vendors buy raw materials locally
- Number of vendors
- Avg. starting money for the vendors
- Whether, Quipu, the community currency is used

Right now, the sim is set for 40 days.