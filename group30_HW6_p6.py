#basic hill climbing search provided as base code for the DSA/ISE 5113 course
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
#Date: 4/4/26


# STOCHASTIC HILL CLIMBING

#need some python libraries
import copy
from random import Random   #need this for the random number generation -- do not change
import numpy as np


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
    value.append(round(myPRNG.triangular(5,1000,200),1))
    
weights = []
for i in range(0,n):
    weights.append(round(myPRNG.triangular(10,200,60),1))
    
#define max weight for the knapsack
maxWeight = 2500

#change anything you like below this line ------------------------------------

#monitor the number of solutions evaluated
solutionsChecked = 0

#function to evaluate a solution x
def evaluate(x):
          
    a=np.array(x)
    b=np.array(value)
    c=np.array(weights)
    
    totalValue = np.dot(a,b)     #compute the value of the knapsack selection
    totalWeight = np.dot(a,c)    #compute the weight value of the knapsack selection
    
    if totalWeight > maxWeight:
        print ("Infeasible solution... removing items until feasible...")  
        # weight removal method: if the solution is infeasible, start removing items with the lowest value/weight ratio until we are below the weight limit
        value_weight_ratio = b/c
        sorted_indices = np.argsort(value_weight_ratio) # sort the indices of the items based on their value/weight ratio
        for i in sorted_indices:
            if totalWeight <= maxWeight: # for when we get to later stages of the loop and are below the weight limit -- we can stop removing items
                break
            if a[i] == 1: # if the item is currently included in the knapsack
                a[i] = 0 # remove the item from the knapsack
                totalValue -= b[i] # update the total value
                totalWeight -= c[i] # update the total weight
      
    x[:] = a.astype(int).tolist()
    return [totalValue, totalWeight]   #returns a list of both total value and total weight
          
       
#here is a simple function to create a neighborhood
#1-flip neighborhood of solution x         
def neighborhood(x):
        
    nbrhood = []     
    
    for i in range(0,n):
        nbrhood.append(x[:])
        if nbrhood[i][i] == 1:
            nbrhood[i][i] = 0
        else:
            nbrhood[i][i] = 1
      
    return nbrhood
          
# another possible neighborhood function is to randomly flip 2 bits instead of 1 bit
# in this instance, the neighborhood of a solution x would be all solutions that can be reached by flipping 2 bits in the solution vector x


#create the initial solution STRATEGY 1
# this strategy involves randomly selecting items until we reach the weight limit
def initial_solution():
    x = []   #i recommend creating the solution as a list
    curr_weight = 0
    
    for i in range(n):
        # start randomly generatign which items to select
        if curr_weight + weights[i] <= maxWeight:
            choice = myPRNG.randint(0,1) # using our seed, will generate the same sequence of random 0's and 1's each time for reproducibility

            ######################## IF YOU WANT TRULY RANDOM NUMBERS, COMMENT OUT THE ABOVE LINE AND USE THE LINE BELOW INSTEAD ########################
            #choice = np.random.randint(0,2) # recall np.random.randint() is inclusive to the lower bound but exclusive to the upper bound, so (0,2) will give either 0 or 1

            x.append(choice)
            if choice == 1:
                curr_weight += weights[i]
        else:
            x.append(0) # if we reach the weight limit, mark all other intems as not included in the knapsack
    return x

#create the initial solution STRATEGY 2
# this strategy sets a weight threshold and only selects items that weigh less than that threshold until we reach the weight limit
# def initial_solution():
#     x = []   #i recommend creating the solution as a list
#     curr_weight = 0
#     threshold = 60 # we set the weight threshold to 60 because it is the mode (most commonly assigned weight)

#     for i in range(n):
#         if weights[i] < threshold and curr_weight + weights[i] <= maxWeight:
#             x.append(1) # if the item is below the threshold and we are below the limit, include it in the knapsack
#             curr_weight += weights[i]
#         else:
#             x.append(0) # if the item is not below the threshold or we are above the limit, do not include it in the knapsack
#     return x

# this is a helper function to create weighted random indexes using myPRNG
def weighted_index(weights):
    total = sum(weights)
    r = myPRNG.random() * total # get a random number between 0 and the total of the weights
    running = 0.0
    for i, w in enumerate(weights):
        running += w # keep a running total of the weights as we iterate through the list
        if r <= running: # once the random number is less than or equal to the running total, we have found our weighted index and can return it
            return i
    return len(weights) - 1 # in case of any rounding issues, return the last index of the weights list


#varaible to record the number of solutions evaluated
solutionsChecked = 0

x_curr = initial_solution()  #x_curr will hold the current solution 
x_best = x_curr[:]           #x_best will hold the best solution 
f_curr = evaluate(x_curr)    #f_curr will hold the evaluation of the current soluton 
f_best = f_curr[:]


#begin local search overall logic ----------------
done = 0
    
while done == 0:
    
    Neighborhood = neighborhood(x_curr)
    
    improving_neighbors = []   # store all improving neighbors in this list as tuples of (solution, evaluation)
    
    for s in Neighborhood:
        solutionsChecked += 1
        
        s_candidate = s[:] # make a copy of the neighbor solution to evaluate
        f_s = evaluate(s_candidate) # evaluate the neighbor solution

        improvement = f_s[0] - f_curr[0]

        if improvement > 0:
            improving_neighbors.append((s_candidate, f_s, improvement)) # if the neighbor solution is better than the current solution, add it to the list of improving neighbors as a tuple of (solution, evaluation)
    
    # if no improving neighbors -- set done to 1 and end the loop
    if not improving_neighbors:
        done = 1

    else: # we found at least one improving neighbor, so we will pick a random improving neighbor to move to 
        # we will assign probabilistic weights by improvement size
        weights_prob = [item[2] for item in improving_neighbors]

        # pick a random improving neighbor
        random_index = weighted_index(weights_prob) # pick a random index from the list of improving neighbors based on probabilistic weights
        x_curr, f_curr, improvement_filler = improving_neighbors[random_index] # move to that random improving neighbor and update the current solution and evaluation
        # we can ignore the improvement_filler var, it was useful for weighting based on improvement but is now useless

        x_curr = x_curr[:] # make a copy of the solution to avoid any potential issues with references
        f_curr = f_curr[:] # make a copy of the evaluation to avoid any potential issues with references
        
        # update the best solution and evaluation if curr is better than the previous best
        if f_curr[0] > f_best[0]:
            x_best = x_curr[:]
            f_best = f_curr[:]
        
        print("\nTotal number of solutions checked:", solutionsChecked)
        print("Best value found so far:", f_best)        
    
print ("\nFinal number of solutions checked: ", solutionsChecked)
print ("Best value found: ", f_best[0])
print ("Weight is: ", f_best[1])
print ("Total number of items selected: ", np.sum(x_best))
print ("Best solution: ", x_best)
