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
#Date: 5/9/26

'''Homework 8 genetic algorithm -- Schwefel Minimization Problem'''

#need some python libraries
import copy
import math
from random import Random
import numpy as np
import matplotlib.pyplot as plt # imported another library for plotting, i don't know how else to plot things

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

'''this is now a schweffel minimization problem, not a knapsack problem, so there are some changes we need to make to the problem instance'''
lowerBound = -500
upperBound = 500

#change anything you like below this line, but keep the gist of the program ------------------------------------
''' use these values for 2D approximate optimal solution for this program'''
n = 2 # number of dimensions 
populationSize = 500 #size of GA population
Generations = 1000   #number of GA generations

crossOverRate = 0.3 
mutationRate = 0.03 
eliteSolutions = 20 

''' use these values for 2D 8 chromosome solution for problem 1c'''
# n = 2 # number of dimensions 
# populationSize = 8 #size of GA population
# Generations = 200   #number of GA generations

# crossOverRate = 0.5 
# mutationRate = 0.1 
# eliteSolutions = 1 

''' use these values for the 200D approximate optimal solution for problem 1d'''
# n = 200 # number of dimensions 
# populationSize = 1000 #size of GA population
# Generations = 10000   #number of GA generations

# crossOverRate = 0.6
# mutationRate = 0.02
# eliteSolutions = 20
#-----------------------------------------------------------------------------------------------------------------


#create a chromosome with a continuous value, not 0 and 1 like the knapsack
def createChromosome(d):   

    x = [myPRNG.uniform(lowerBound, upperBound) for _ in range(d)] 
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
        # we set a random value weight, which will determine how much of each parent goes into the offspring
        weight = myPRNG.random() 
        offspring1 = [weight*x1[i] + (1-weight)*x2[i] for i in range(n)] 
        offspring2 = [weight*x2[i] + (1-weight)*x1[i] for i in range(n)]
    else:
        offspring1 = copy.deepcopy(x1) # if no crossover, offspring1 is a copy of x1
        offspring2 = copy.deepcopy(x2) # if no crossover, offspring2 is a copy of x2

    
    return offspring1, offspring2  #two offspring are returned 


#function to evaluate a solution x
def evaluate(x):          
      val = 0
      d = len(x)
      for i in range(d):
            val = val + x[i]*math.sin(math.sqrt(abs(x[i])))
                                        
      val = 418.9829*d - val         
                    
      return -val # we return negative because our GA will want to maximize fitness, so by making it negative it will later choose the minimum solution as the best solution and not the maximum    


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
    for i in range(len(x)): # for each gene in the chromosome, more than just one gene can be mutated
        if myPRNG.random() < mutationRate:
            # do a random small change in coordinates
            x[i] += myPRNG.uniform(-10, 10)
            
            # keep the global bounds (upper and lower bounds)
            x[i] = max(lowerBound, min(upperBound, x[i])) 
    
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
    print ("Value: ", -pop[0][1]) # multiply by -1 so the real value is what is displayed at the end, recall we made them negative so the GA would work


def plot_population(pop, title):
    x_vals = [ind[0][0] for ind in pop]
    y_vals = [ind[0][1] for ind in pop]

    # create schweffel countour plot
    X = np.linspace(-500, 500, 1000)
    Y = np.linspace(-500, 500, 1000)
    X, Y = np.meshgrid(X, Y)

    Z = 418.982887*n - (X*np.sin(np.sqrt(np.abs(X))) + Y*np.sin(np.sqrt(np.abs(Y))))

    plt.figure()
    plt.contourf(X, Y, Z, levels=50) # note, this color contour is normalized, where 1 is the max and 0 is the min, but it shows the schwefel function
    plt.scatter(x_vals, y_vals, color='r')
    plt.title(title)
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.colorbar(label="Normalized Schwefel Value")
    plt.savefig(f"/Users/ethan1/Desktop/vs_code/DSA5113/HW8/{title}.png")  # save the plot as a PNG file
    
def main():
    #GA main code
    Population = initializePopulation()

    # plot the initial chromosomes in the population

    plot_population(Population, "Initial Population")

    #optional: you can output results to a file -- i've commented out all of the file out put for now
    #f = open('out.txt', 'w')  #---uncomment this line to create a file for saving output    


    for j in range(Generations):
                    
        mates=rouletteWheel(Population) 
        Offspring = breeding(mates)
        Population = insert(Population, Offspring)
    
        #end of GA main code
        if j == 0: # this is the first generation, we want to plot this too
            plot_population(Population, "First Generation")
        if j == Generations-1: # final gen, lets see what we have
            plot_population(Population, "Final Population")
        maxVal, meanVal, minVal, stdVal=summaryFitness(Population)          #check out the population at each generation
        print("Iteration: ", j, summaryFitness(Population))                 #print to screen; turn this off for faster results
        
        #f.write(str(minVal) + " " + str(meanVal) + " " + str(varVal) + "\n")  #---uncomment this line to write to  file
        
    #f.close()   #---uncomment this line to close the file for saving output
    
    print (summaryFitness(Population))
    bestSolutionInPopulation(Population)
    

if __name__ == "__main__":
    main()    
    


