# Genetic Algorithm for the Knapsack Problem

## Problem

The knapsack problem is a problem in combinatorial optimization: Given a set of items, each with a weight and a value, determine the number of each item to include in a collection so that the total weight is less than or equal to a given limit and the total value is as large as possible.

## Command

To launch the genetic algorithm for solving knapsack problem, you should choose between the instances of the problem, then set different parameters as follow:

    python3 main.py [n_obj] [n_iter] [n_pop] [r] [m]

* **n_obj**                 :  number of items (must be in [10, 20, 100, 1000])
* **n_iter** (default: 200) :  number of generations
* **n_pop**      (default: 200) :  number of hypothesis in a generation
* **r**      (default: 0.6) :  crossover rate
* **m**      (default: 0.01):  mutation rate

## Genetic Algorithm

The implemented algorithm is a metaheuristic inspired by the process of natural selection that belongs to the larger class of evolutionary algorithms.
The general structure of the algorithm is the following.
    
    P = initialization()
    
    while (generation <= max_generations):
            Ps = [] #new generation
            Ps += selection(eval)
            Ps += crossover(eval)
            mutation(Ps)
            
            P = Ps
            eval = evaluation(P)
            generation += 1

* **Initialization**: The initial solutions are chosen randomly among the set of valid solutions. If we choose the initial solutions totally randomly, our algorithm may not even find a valid solution if the number of items is high.
* **Selection**: A portion of the existing population is selected to breed a new generation. Individual solutions are selected through a fitness-based process, where fitter solutions (as measured by a fitness function) are typically more likely to be selected.
* **Crossover**: A pair of "parent" solutions is selected for breeding from the pool selected previously. A new solution is created which typically shares many of the characteristics of its "parents".
  * **Single-point Crossover**: A point on both parents' chromosomes is picked randomly, and designated a 'crossover point'. Bits to the right of that point are swapped between the two parent chromosomes.
  * **Uniform Crossover**: Each bit is chosen from either parent with equal probability.
* **Mutation**: One or more gene values in a chromosome are altered from their initial states.

## Results

* **Number of items = 10**
  * **Mutation rate = 0.01**: Precision of **89 %**
  * **Mutation rate = 0.1**: Precision of **94 %**
  * **Mutation rate = 0.2**: Precision of **98 %**
* **Number of items = 100**
  * **Mutation rate = 0.01**: Precision of **53 %**
  * **Mutation rate = 0.1**: Precision of **60 %**
  * **Mutation rate = 0.2**: Precision of **67 %**
