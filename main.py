from GenKnapsack import GenKnapsack
import sys

N_ITER = 200
P = 200
R = 0.6
M = 0.01

# def parser(filepath):
    # def is_integer(s):
    #     try:
    #         int(s)
    #         return True
    #     except ValueError:
    #         return False
#     arguments = []
#     def is_integer(s):
#         try:
#             int(s)
#             return True
#         except ValueError:
#             return False
#
#     fp = open(filepath, 'r')
#     line = fp.readline()
#     while (line):
#         line = line.replace("\n", "").split(": ")[1]
#         if (is_integer(line)): #integer
#             arguments.append(int(line))
#         else: #list of integers
#             line = list(map(int, line[1:len(line)-1].split(", ")))
#             arguments.append(line)
#         line = fp.readline()
#     fp.close()
#     return arguments


def parser(filename):
    with open("instances/" + filename, "r") as fp :
        #capacity
        capacity = int(fp.readline().split(" ")[1])

        #values & weights
        values = []
        weights = []
        line = fp.readline()
        while(line):
            line = line.replace("\n", "").split(" ")
            values.append(int(line[0]))
            weights.append(int(line[1]))
            line = fp.readline()

    with open("optimum/" + filename, "r") as fp :
        optimalScore = int(fp.readline())

    return (capacity, values, weights, optimalScore)


def main(filename):
    (capacity, values, weights, optimalScore) = parser(filename)
    knapsack = GenKnapsack (
        capacity,
        values,
        weights,
        n_iter=N_ITER,
        p=P,
        r=R,
        m=M
    )
    knapsack.run()
    print("Optimal Score: ", optimalScore)


errorMessage = """
usage:  python3 main.py [n_obj] [n_iter] [n_pop] [r] [m]

n_obj                 :  number of items (must be in [10, 20, 100, 1000])
n_iter (default: 200) :  number of generations
p      (default: 200) :  number of hypothesis in a generation
r      (default: 0.6) :  crossover rate
m      (default: 0.01):  mutation rate

For example:
    python3 main.py 20
"""

if __name__ == "__main__":
    #Choose filename
    # flag=False
    # while(not flag):
    #     print("""\nPlease choose an instance from the list below: \n
    #     knap_10   (instance of 10 objects)
    #     knap_20   (...)
    #     knap_100
    #     knap_1000 \n""")
    #     filename = input("> ")
    #     tmp = filename.split("_")
    #     if (tmp[0] == "knap" and tmp[1] in ['10', '20', '100', '1000']):
    #         flag=True
    try:
        num_objects = sys.argv[1]

    except Exception as e:
        print(errorMessage)

    else:
        try:
            N_ITER = int(sys.argv[2])
        except Exception as e:
            pass

        try:
            P = int(sys.argv[3])
        except Exception as e:
            pass

        try:
            R = float(sys.argv[4])
        except Exception as e:
            print("error R")

        try:
            M = float(sys.argv[5])
        except Exception as e:
            print("error M")

        if str(num_objects) not in ['10', '20', '100', '1000']:
            print(errorMessage)
        else:
            main("knap_" + str(num_objects))
