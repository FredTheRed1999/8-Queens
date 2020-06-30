import random
import numpy as np

#Generate 8 chromosome gene with randomness
def generateChromosome(nQ):
	x=list(np.arange(8))
	random.shuffle(x)
	return x

#Score the Population
def fitness(chromosome):
	"""
	We can take fitness to be the minimum number of conflicts between the Queens.ie
    For an n queen problem the max fitness is nCr as repeats are possible = n! / r! * (n - r)!, for an 8 queen
    gives us 28 

    So fitness will be 28 - number of conflicts

    ->Row/Columnar Clashes
    ->Diagonal Clashes
	"""
	horizontal_collisions = sum([chromosome.count(queen)-1 for queen in chromosome])/2
	diagonal_collisions = 0
	n = len(chromosome)
	left_diagonal = [0] * 2*n
	right_diagonal = [0] * 2*n
	for i in range(n):
		left_diagonal[i + chromosome[i] - 1] += 1
		right_diagonal[len(chromosome) - i + chromosome[i] - 2] += 1

	diagonal_collisions = 0
	for i in range(2*n-1):
		counter = 0
		if left_diagonal[i] > 1:
			counter += left_diagonal[i]-1
		if right_diagonal[i] > 1:
			counter += right_diagonal[i]-1
		diagonal_collisions += counter / (n-abs(i-n+1))
    
	return int(28 - (horizontal_collisions + diagonal_collisions))

def fitness_probability(chromosome):
	return fitness(chromosome)/28


def random_pick(population, probabilities):
    populationWithProbabilty = zip(population, probabilities)
    total = sum(w for c, w in populationWithProbabilty)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(population, probabilities):
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"



def crossover(parent1,parent2):
	#Taking a random position and then taking from first parent before that position and from second parent the rest
	c=random.randint(0,len(parent1)-1)
	child=parent1[:c]+parent2[c:]
	return child


def mutation(chromosome):
	#Adding a little mutation helps us to improve genetic material in generations and prevents stagnation.
	x=random.randint(0,len(chromosome)-1)
	chromosome[x]= random.randint(0,7)
	return chromosome


def genetic_repooling(population,mutation_rate,fitness1=28):
	mutation_rate=mutation_rate
	new_population=[]
	probabilities=[fitness_probability(x) for x in population]
	for i in range(len(population)):
		parent1=random_pick(population,probabilities)
		parent2=random_pick(population,probabilities)
		child=crossover(parent1,parent2)
		if random.random()< mutation_rate:
			child=mutation(child)
		print('New chromosome is: {} Fitness for chromosome:{}'.format(child,fitness(child)))
		new_population.append(child)
		if fitness(child)==28:
			print("Found the Perfect case {}".format(child))
			print(child)
			break
	return new_population		



if __name__ == "__main__":
	#number of queens
	nq=8
	#number of initial sequence
	n_seq=110 
	population = [generateChromosome(nq) for _ in range(n_seq)]
	generation = 1

	while not 28 in [fitness(x) for x in population]:
		print("=== Generation {} ===".format(generation))
		population = genetic_repooling(population, 0.04,28)
		print("Maximum fitness = {}".format(max([fitness(n) for n in population])))
		generation += 1
