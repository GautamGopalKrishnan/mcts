from itertools import combinations_with_replacement, product

ucbs = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
epss = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.15, 0.25, 0.5]

with open('arguments.txt', 'w') as f:
    for e1, e2 in product(epss, epss):
        f.write("--env ConnectFour --tree_policy1 epsilon_greedy --epsilon1 {} --tree_policy2 epsilon_greedy --epsilon2 {} --samples 500\n".format(e1, e2))
    for c1, c2 in product(ucbs, ucbs):
        f.write("--env ConnectFour --tree_policy1 ucb --c1 {} --tree_policy2 ucb --c2 {} --samples 500\n".format(c1, c2))
    for e1, c2 in product(epss, ucbs):
        f.write("--env ConnectFour --tree_policy1 epsilon_greedy --epsilon1 {} --tree_policy2 ucb --c2 {} --samples 500\n".format(e1, c2))

