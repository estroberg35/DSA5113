#basic genetic algorithm Python code provided as base code for the DSA/ISE 5113 course
#author: Charles Nicholson
#date: 4/5/2019

#NOTE: You will need to change various parts of this code.  However, please keep the majority of the code intact (e.g., you may revise existing logic/functions and add new logic/functions, but don't completely rewrite the entire base code!)  
#However, I would like all students to have the same problem instance, therefore please do not change anything relating to:
#   random number generation
#   number of items (should be 150)
#   random problem instance
#   weight limit of the knapsack

#------------------------------------------------------------------------------

#Student name: Ethan Stroberg and Cord Reynolds
#Date: 4/25/26

'''
how the genetic algorithm works:
1. start: generate random population of n chromosomes
2. fitness: evaluate th efitness of each chormosome in population
3. new population: create a new population by repeating the following steps until the new population is complete
    a. selection: select two parent chromosomes from a population according to their fitness (the better fitness, the more likely to be selected)
    b. crossover: with crossover probability, cross over the parents to form a new offspring (children).  If no crossover was performed, offspring is an exact copy of parents.
    c. mutation: with a mutation probability, mutate new offspring 
    d. fitness and insertion: place new offspring in a new population
4. replace: use new population for enxt run of algorithm
5. test: if the end condition is satisfied, stop, and return the best solution in current population
6. loop: go to step 2
'''

#need some python libraries
import copy
import math
from random import Random
import numpy as np

#to setup a random number generator, we will specify a "seed" value
seed = 5113
myPRNG = Random(seed)

#to setup a random number generator, we will specify a "seed" value
#need this for the random number generation -- do not change
seed = 51132023
myPRNG = Random(seed)

#to get a random number between 0 and 1, use this:             myPRNG.random()
#to get a random number between lwrBnd and upprBnd, use this:  myPRNG.uniform(lwrBnd,upprBnd)
#to get a random integer between lwrBnd and upprBnd, use this: myPRNG.randint(lwrBnd,upprBnd)

#number of elements in a solution
n = 150

#create an "instance" for the knapsack problem
value = []
for i in range(0,n):
    #value.append(round(myPRNG.expovariate(1/500)+1,1))
    value.append(round(myPRNG.triangular(150,2000,500),1))
    
weights = []
for i in range(0,n):
    weights.append(round(myPRNG.triangular(8,300,95),1))
    
#define max weight for the knapsack
maxWeight = 2500


#change anything you like below this line, but keep the gist of the program ------------------------------------

#monitor the number of solutions evaluated
solutionsChecked = 0


populationSize = 1000 #size of GA population
Generations = 500   #number of GA generations

# each rate is currently implemented
crossOverRate = 0.3  
mutationRate = 0.05
eliteSolutions = 10      


#create an continuous valued chromosome 
def createChromosome(d):   
    #this code as-is expects chromosomes to be stored as a list, e.g., x = []
    #write code to generate chromosomes, most likely want this to be randomly generated
    
    x = [0 for _ in range(n)] #initialize everything to 0....
    curr_weight = 0
    
    done = 0
    while done == 0:
        item_index = myPRNG.randint(0,n-1)
        if x[item_index] == 1:
            continue #already used
        #this would have pushed us over weight limit, don't add items and try no more
        if weights[item_index] + curr_weight > maxWeight:
            done = 1
            continue
        x[item_index] = 1
        curr_weight = weights[item_index] + curr_weight
    return x
    

#create initial population by calling the "createChromosome" function many times and adding each to a list of chromosomes (a.k.a., the "population")
def initializePopulation(): #n is size of population; d is dimensions of chromosome
    
    population = []
    populationFitness = []
    
    for i in range(populationSize):
        population.append(createChromosome(n))
        populationFitness.append(evaluate(population[i]))
        
    tempZip = zip(population, populationFitness)
    popVals = sorted(tempZip, key=lambda tempZip: tempZip[1], reverse = True)
    
    #the return object is a reversed sorted list of tuples: 
    #the first element of the tuple is the chromosome; the second element is the fitness value
    #for example:  popVals[0] is represents the best individual in the population
    #popVals[0] for a 2D problem might be  ([-70.2, 426.1], 483.3)  -- chromosome is the list [-70.2, 426.1] and the fitness is 483.3
    
    return popVals    

#implement a crossover
def crossover(x1,x2):
    
    #with some probability (i.e., crossoverRate) perform breeding via crossover, 
    #i.e. two parents (x1 and x2) should produce two offsrping (offspring1 and offspring2) 
    # --- the first part of offspring1 comes from x1, and the second part of offspring1 comes from x2
    # --- the first part of offspring2 comes from x2, and the second part of offspring2 comes from x1
    
    #if no breeding occurs, then offspring1 and offspring2 can simply be copies of x1 and x2, respectively

    if myPRNG.random() < crossOverRate: # implement crossover rate
        crossover_point = myPRNG.randint(1, n-1) # select a random crossover point
        offspring1 = x1[:crossover_point] + x2[crossover_point:] # create offspring1 by combining the first part of x1 and the second part of x2
        offspring2 = x2[:crossover_point] + x1[crossover_point:] # create offspring2 by combining the first part of x2 and the second part of x1
    else:
        offspring1 = copy.deepcopy(x1) # if no crossover, offspring1 is a copy of x1
        offspring2 = copy.deepcopy(x2) # if no crossover, offspring2 is a copy of x2

    
    return offspring1, offspring2  #two offspring are returned 


#function to compute the weight of chromosome x
def calcWeight(x):
    
    a=np.array(x)
    c=np.array(weights)
    
    totalWeight = np.dot(a,c)    #compute the weight value of the knapsack selection

    return totalWeight   #returns total weight    
    

#function to determine how many items have been selected in a particular chromosome x
def itemsSelected(x):
    
    a=np.array(x)
    return np.sum(a)   #returns total number of items selected 



#function to evaluate a solution x
def evaluate(x):
          
    a=np.array(x)
    b=np.array(value)
    c=np.array(weights)
    
    totalValue = np.dot(a,b)     #compute the value of the knapsack selection
    totalWeight = np.dot(a,c)    #compute the weight of the knapsack selection

    #you will VERY LIKELY need to add some penalties or sometype of modification of the totalvalue to compute the chromosome fitness
    #for instance, you may include penalties if the knapsack weight exceeds the maximum allowed weight

    if totalWeight > maxWeight:
        totalValue = -1000
        totalWeight = -1000

    fitness  = totalValue # fitness will either be the value if a feasible solution or will be -1000 if infeasible, and thus never selected
    global solutionsChecked
    solutionsChecked += 1 #increment the number of solutions evaluated

    return fitness   #returns the chromosome fitness




#performs tournament selection; k chromosomes are selected (with repeats allowed) and the best advances to the mating pool
#function returns the mating pool with size equal to the initial population
def tournamentSelection(pop,k):
    
    #randomly select k chromosomes; the best joins the mating pool
    matingPool = []
    
    while len(matingPool)<populationSize:
        
        ids = [myPRNG.randint(0,populationSize-1) for i in range(k)]
        competingIndividuals = [pop[i][1] for i in ids]
        bestID=ids[competingIndividuals.index(max(competingIndividuals))]
        matingPool.append(pop[bestID][0])

    return matingPool


def rouletteWheel(pop):
    
    matingPool = []
    #create sometype of rouletteWheel selection -- can be based on fitness function or fitness rank
    #(remember the population is always ordered from most fit to least fit, so pop[0] is the fittest chromosome in the population, and pop[populationSize-1] is the least fit!

    # we will use the fitness value for allocation of space on the roulette wheel for each chromosome 
    # (i.e each chromosome gets a slice proportional to its fitness divided by the sum of the population fitness)

    totalFitness = sum([pop[i][1] for i in range(populationSize)]) # [1] is the index of the fitness in pop
    selectionProbs = [pop[i][1]/totalFitness for i in range(populationSize)] # compute the slice size for each chromosome

    while len(matingPool) < populationSize:
         # select a random chromosome based on the probabilities
         # we will generate a random number between 0 and 1, and then start adding up each probability
         # when the cumulative probability exceeds the random number, we select that chromosome for the mating pool
         # logically, when we pass the random number, we are in the slice of the roulette wheel that corresponds to that chromosome, so we choose it
        selected = myPRNG.random() # random number between 0 and 1
        cumulativeProb = 0.0

        for i in range(populationSize):
            cumulativeProb += selectionProbs[i]

            if selected < cumulativeProb:
                matingPool.append(pop[i][0]) # add the selected chromosome to the mating pool
                break
    
    return matingPool
    
    
#function to mutate solutions
def mutate(x):
    
    #create some mutation logic  -- make sure to incorporate "mutationRate" somewhere and dont' do TOO much mutation
    if myPRNG.random() < mutationRate: # mutate the solution accoding to the mutation rate probability
        mutation_point = myPRNG.randint(0, n-1) # select a random mutation point
        x[mutation_point] = 1 - x[mutation_point] # flip the bit at the mutation point (if it's 0, make it 1; if it's 1, make it 0)

    return x
        
#breeding -- uses the "mating pool" and calls "crossover" function    
def breeding(matingPool):
    #the parents will be the first two individuals, then next two, then next two and so on
    
    children = []
    childrenFitness = []
    for i in range(0,populationSize-1,2):
        child1,child2=crossover(matingPool[i],matingPool[i+1])
        
        child1=mutate(child1)
        child2=mutate(child2)
        
        children.append(child1)
        children.append(child2)
        
        childrenFitness.append(evaluate(child1))
        childrenFitness.append(evaluate(child2))
        
    tempZip = zip(children, childrenFitness)
    popVals = sorted(tempZip, key=lambda tempZip: tempZip[1], reverse = True)
        
    #the return object is a sorted list of tuples: 
    #the first element of the tuple is the chromosome; the second element is the fitness value
    #for example:  popVals[0] is represents the best individual in the population
    #popVals[0] for a 2D problem might be  ([-70.2, 426.1], 483.3)  -- chromosome is the list [-70.2, 426.1] and the fitness is 483.3
    
    return popVals


#insertion step
def insert(pop,kids):
    
    #this is not a good solution here... essentially this is replacing the previous generation with the offspring and not implementing any type of elitism
    #at the VERY LEAST evaluate the best solution from "pop" to make sure you are not losing a very good chromosome from last generation
    #maybe want to keep the top 5? 10? solutions from pop -- it's up to you.
    # eliteSolutions is currently 10 --> keep top 10 solutions from pop and add the kids to make the new population
    new_population = pop[:eliteSolutions] + kids[:populationSize-eliteSolutions] # keep the top eliteSolutions from pop and fill the rest with kids
    new_population = sorted(new_population, key=lambda new_population: new_population[1], reverse=True) # sort the new population by fitness in descending order

    return new_population 
    
    
    
#perform a simple summary on the population: returns the best chromosome fitness, the average population fitness, and the variance of the population fitness
def summaryFitness(pop):
    a=np.array(list(zip(*pop))[1])
    return np.max(a), np.mean(a), np.min(a), np.std(a)


#the best solution should always be the first element... 
def bestSolutionInPopulation(pop):
    print ("Best solution: ", pop[0][0])
    print ("Items selected: ", itemsSelected(pop[0][0]))
    print ("Value: ", pop[0][1])
    print ("Weight: ", calcWeight(pop[0][0]))

    
    
def main():
    #GA main code
    Population = initializePopulation()


    #optional: you can output results to a file -- i've commented out all of the file out put for now
    #f = open('out.txt', 'w')  #---uncomment this line to create a file for saving output    


    for j in range(Generations):
                    
        #mates=tournamentSelection(Population,10)  #<--need to replace this with roulette wheel selection, e.g.:  mates=rouletteWheel(Population)
        mates = rouletteWheel(Population)
        Offspring = breeding(mates)
        Population = insert(Population, Offspring)
    
        #end of GA main code
        
        maxVal, meanVal, minVal, stdVal=summaryFitness(Population)          #check out the population at each generation
        print("Iteration: ", j, summaryFitness(Population))                 #print to screen; turn this off for faster results
        
        #f.write(str(minVal) + " " + str(meanVal) + " " + str(varVal) + "\n")  #---uncomment this line to write to  file
        
    #f.close()   #---uncomment this line to close the file for saving output
    
    print (summaryFitness(Population))
    bestSolutionInPopulation(Population)
    print("Generations: ", Generations)
    print("Population Size: ", populationSize)
    print("Crossover Rate: ", crossOverRate)
    print("Mutation Rate: ", mutationRate)
    print("Elitism: ", eliteSolutions)

    

if __name__ == "__main__":
    main()    
    


