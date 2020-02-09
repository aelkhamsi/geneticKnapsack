import random
import sys
import numpy as np
import math

#### THE KNAPSACK PROBLEM ####
# Given a set of items, each with a weight and a value
# Determine the number of each item to include in a collection so that:
# - the total weight is less than or equal to a given limit
# - the total value is as large as possible


class GenKnapsack:

    def __init__(self, capacity, values, weights, n_iter=100, p=500, r=0.6, m=0.01, ):
        """
        P: population
        fitness_treshold: termination criterion
        p: size of the population
        r: fraction of the population to be replaced by Crossover at each step
        m: mutation rate
        """
        self.n_iter = n_iter
        self.p = p
        self.r = r
        self.m = m

        self.capacity = capacity
        self.values = values
        self.weights = weights

    def init(self):
        """
        Initially, we build hypothesis that are valid solutions (their weight
        don't exceed the capacity of the backpack) in order to help our
        algorithm find the optimal solution.

        If we start with random hypothesis, and if the number of elements is big,
        the algorithm may not even find a valid solution.
        """
        self.P = []
        for i in range(self.p):
            # for j in range(len(self.values)):
            #     h += str(random.randint(0, 1)) #30%


            h = '0' * len(self.values)
            new_h = h
            fitness = self.fitness(h)

            while(fitness >= 0):
                h = new_h
                j = random.randint(0, len(self.values) - 1)
                new_h = new_h[:j] + '1' + new_h[j+1:]
                fitness = self.fitness(new_h)

            self.P.append(h)

    # def fitness(self, hypothesis):
    #     score = 0
    #     weight = 0
    #     for i in range(len(hypothesis)):
    #         weight += int(hypothesis[i]) * self.weights[i]
    #         if (weight <= self.capacity):
    #             score += int(hypothesis[i]) * self.values[i]
    #         else:
    #             excess = weight - self.capacity
    #             score += int(hypothesis[i]) * self.values[i] * (self.weights[i] - excess / self.values[i])
    #             score -= int(hypothesis[i]) * self.values[i] * (excess / self.values[i])
    #
    #          # if (weight <= self.capacity) else -10 * int(hypothesis[i]) * self.values[i]
    #     return score

    def fitness(self, hypothesis):
        weight = 0
        score = 0
        for i in range(len(hypothesis)):
            weight += int(hypothesis[i]) * self.weights[i]
            score += int(hypothesis[i]) * self.values[i]
        return score if weight <= self.capacity else -1 * score

    def evaluate(self):
        """ Returns a list indexed by P (the population) that represents the
        probabilities for each hypothesis to be selected
        """

        eval = []
        # max = -1 * sys.maxsize - 1
        # min = sys.maxsize
        sumVal = 0
        for i in range(self.p):
            val = self.fitness(self.P[i])
            # if (val < min):
            #     min = val
            # if (val > max):
            #     max = val
            val = val if val >= 0 else 0.5 #ReLU (remix)
            sumVal += val
            eval.append(val)
        for i in range(self.p):
            eval[i] = eval[i] / sumVal
        return eval

    def select(self, eval):
        """ selects (1 - r)p members of P to add to the new generation """
        selection = np.random.choice(self.P, math.floor( (1-self.r)*self.p ), replace=False, p=eval)
        return selection.tolist()


    #
    def singlepointCrossover(self, eval): # Single-point crossover
        """ select (r * p)/2 members of P. For each pair (h1, h2), produce two offspring
        by crossover. add offspring to the new generation
        """
        offspring = []
        crossPop = np.random.choice(self.P, math.floor( self.r*self.p ), replace=False, p=eval)
        for i in range(0, len(crossPop)-1):
            finish = False
            for j in range(i+1, len(crossPop)):
                crossPoint = random.randint(1, len(self.values)-1)
                h = ''
                h += crossPop[i][0:crossPoint]
                h += crossPop[j][crossPoint:]
                offspring.append(h)
                if (len(offspring) >= math.floor( self.r*self.p )):
                    finish = True
                    break
            if (finish):
                break
        return offspring

    def uniformCrossover(self, eval): # Uniform crossover
        """ select (r * p)/2 members of P. For each pair (h1, h2), produce two offspring
        by crossover. add offspring to the new generation
        """
        offspring = []
        crossPop = np.random.choice(self.P, math.floor( self.r*self.p ), replace=False, p=eval)
        for i in range(0, len(crossPop)-1):
            finish = False
            for j in range(i+1, len(crossPop)):
                h = ''
                for k in range(len(self.values)):
                    rand = random.randint(0, 1)
                    if (rand):
                        h += crossPop[i][k]
                    else:
                        h += crossPop[j][k]
                offspring.append(h)
                if (len(offspring) >= math.floor( self.r*self.p )):
                    finish = True
                    break
            if (finish):
                break
        return offspring

    #
    def mutate(self, Ps): #Single-point mutation
        """ choose m percent of the members of the new generation (uniformally).
        For each, invert one randomly selected bit """
        mutationPop =  np.random.choice(range(0, self.p), math.floor(self.m * self.p), replace=False) #indexes of the mutation population
        for i in range(len(mutationPop)):
            mutationPoint = random.randint(0, len(self.values)-1)
            if (Ps[i][mutationPoint] == '0'):
                Ps[i] = Ps[i][0:mutationPoint] + '1' + Ps[i][mutationPoint+1:]
            else:
                Ps[i] = Ps[i][0:mutationPoint] + '0' + Ps[i][mutationPoint+1:]


    def run(self):
        self.desc()
        self.init()
        eval = self.evaluate()
        iteration = 0
        while (iteration <= self.n_iter):
            Ps = [] #new generation
            Ps += self.select(eval)
            Ps += self.uniformCrossover(eval)
            self.mutate(Ps)
            self.P = Ps[:]
            eval = self.evaluate()
            iteration += 1

        maxEval = 0
        winner = None
        for i in range(len(eval)):
            if (eval[i] >= maxEval):
                maxEval = eval[i]
                winner = self.P[i]

        #Results
        print("Solution: " + winner)
        print("Score: " + str(self.fitness(winner)))
        return self.fitness(winner)


    def desc(self): # banner + info
        banner = """
                  _  __                                 _
  __ _  ___ _ __ | |/ /_ __   __ _ _ __  ___  __ _  ___| | __
 / _` |/ _ \ '_ \| ' /| '_ \ / _` | '_ \/ __|/ _` |/ __| |/ /
| (_| |  __/ | | | . \| | | | (_| | |_) \__ \ (_| | (__|   <
 \__, |\___|_| |_|_|\_\_| |_|\__,_| .__/|___/\__,_|\___|_|\_\
"""
        print(banner)
        print(" |___/                            |_|")
        print("\n\n")
        print("Number of iterations: ", self.n_iter)
        print("Size of the population: ", self.p)
        print("Crossover ratio: ", self.r)
        print("Mutation rate: ", self.m, "\n")
