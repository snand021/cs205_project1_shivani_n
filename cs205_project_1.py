import heapq #Referenced this when using heapq:  https://docs.python.org/3/library/heapq.html  
#from queue import Queue #didnt use
import time #Referenced this when using timer:  https://realpython.com/python-timer/  

#I also used my previous knowledge of this class and my cs170 project 1 code as a template. I will attach the link to the github on my report. 
#In general I used this python documentation:
#(https://docs.python.org/3/tutorial/index.html ) 
#(https://www.python-engineer.com/courses/advancedpython/01-lists/ ) I referenced other tutorials on this website as well.



goalState = [1,2,3,4,5,6,7,8,9,0,0,0,0] #4 blanks and 1 is the sergeant

#test
#default = [1,2,3,4,5,6,7,8,9,0,0,0,0] #goal state to see if program runs
#default = [0,2,3,4,5,6,7,8,9,1,0,0,0] #original
default = [0,2,3,4,5,7,6,8,9,1,0,0,0] #testing swapped adjacent pairs

#random states
#default = [0,1,2,3,4,5,6,7,8,9,0,0,0] #random 1 - tested TRUE 0.0035 sec, depth 9, expanded nodes: 9, mql: 25

#default = [1,2,3,4,5,6,7,0,9,8,0,0,0] #random 2 - tested True 0.0137 sec, dep 12, expanded: 228, mql: 425
#default = [1,2,3,4,5,6,0,7,8,9,0,0,0] #random 3 - tested True 0.0026 sec, depth 3, expanded nodes: 3, mql: 10
#default = [0,1,4,0,7,3,9,2,5,8,0,0,6] #random 4 - tested True 56.8235, dep 70, en: 1603565, mql: 836844
#default = [9,8,7,6,5,4,3,2,1,0,0,0,0] #random 5 - tested FALSE - exceeded 2 hour time limit
#default = [4,9,7,5,2,0,1,0,0,3,0,6,8] #random 6 - tested FALSE - exceeded 2 hour time limit
# default =[0,0,0,0,1,2,3,4,5,6,7,8,9] #random 7 - tested True 13.2307, dep 61, en: 364384, mql: 230214
#default = [2,4,6,8,0,0,0,0,1,3,5,7,9] #random 8 - tested True 475.8562, dep: 85, en: 6884526, mql: 2597912
#default = [5,6,3,2,0,7,0,9,4,0,1,0,8] #random 9 - tested FALSE - exceeded 2 hour time limit
#default = [0,0,0,9,8,7,6,5,4,3,2,1,0] #random 10 - tested FALSE - exceeded 2 hour time limit


#have a map of all the neighbors of each spot so we know all possible moves for each postiion
neighbors = {
    0:[1], #is actually position 1 in the image
    1:[0,2], 
    2:[1,3], 
    3:[2,4,10], 
    4:[3,5],
    5:[4,6,11],
    6:[5,7],
    7:[6,8,12],
    8:[7,9],
    9:[8],
    10:[3],
    11:[5],
    12:[7]

}

'''
trying different goal states:

    
'''

#Node class reference: https://www.educative.io/answers/how-to-solve-the-8-puzzle-problem-using-the-a-star-algorithm 
class Node:
    def __init__(self, puzzle, root = None, depth = 0, parent = None,  heur = 0):
        self.puzzle = puzzle #current puzzle
        if(parent == None):
            self.root = self #set root to current node
        else:
            self.root = parent.root #else use parent's root
        self.depth = depth #depth/level of the tree
        self.parent = parent #parent/previous state of puzzle
        self.heur = heur #heurisitc value for the node
      
    def __lt__(self, other): #function that compares nodes, also min queue works with smallest values first
        return (self.depth + self.heur) < (other.depth + other.heur)


#CHANGED to: find all the blanks instead of just one blank
def findblank(puzzle) : #finds 0
    blanks = []
    for i in range(len(puzzle)):
        if(puzzle[i]==0):
            blanks.append(i)
    return blanks #returns list of all positions of blanks

#CHANGED
#Took inspiration/got idea from this: https://stackoverflow.com/questions/17873384/how-to-deep-copy-a-list      
def copyPuzzle(puzzle): #to make a copy of the puzzle
    copy =[]
    for i in puzzle:
        copy.append(i)
    return copy


#Used this link to understand the function: https://www.educative.io/answers/how-to-solve-the-8-puzzle-problem-using-the-a-star-algorithm 


#CHANGED
def generateChild(node, searchName):
   puzzle = node.puzzle #current state of the puzzle were looking at
   blanks = findblank(puzzle) #find all the blanks in the puzzle (all possible spots we can move to)
   children=[]
   '''
   logic 
   1. look for blanks
   2. for every blank, look at its neighbors and see if theres a man there
   3. if man is there, then move that man into the blank

   each child state only represents one move
   '''
   #for every blank, look at the positions connected to it and if connected pos, has a man, move that man into the blank
   for b in blanks:
       for n in neighbors[b]: #for every neighbor of the blank
           if(puzzle[n] != 0): #if there is a man in the neighbor position, move that man into the blank and create a child node with that new puzzle state
               newPuzzle = copyPuzzle(puzzle) #make a copy of the puzzle to change. we need og puzzle for other child nodes
               
               #swap
               newPuzzle[b] = newPuzzle[n] #moves man into blank spot
               newPuzzle[n] = 0 #makes old spot blank

               #create child node with new puzzle state, depth+1 (means its in the next level of the tree), parent is the current node, and heurisitics is calculated with the new puzzle state
               childNode = Node (puzzle = newPuzzle, depth = node.depth + 1, parent = node, heur = heuristics(newPuzzle, searchName))
               children.append(childNode) #adds new possible move to list of children
   return children
   

    
    
    #Old NOTES from TA office hours (previous class)
    #pop the one with the least cost in the q
    #will insert all 4 children in the priority q
    #check while q is not empty when you search priority q
    # i am deisgning the priority q that sorts the weight paraemter using heur

        


#From Project 1 Instructions #CHANGED
def select_and_init_algorithm(puzzle):
    algorithm = input("Select algorithm. (1) for Uniform Cost Search, (2) for the Misplaced Tile Heuristic, ""or (3) the Manhattan Distance Heuristic." + '\n')
    if algorithm == "1":
        generalSearch(puzzle, "uniform") #for uniform, the default heuristic is 0
    elif algorithm == "2":
        generalSearch(puzzle, "misplaced tile")
    elif(algorithm == "3"):
        generalSearch(puzzle, "manhattan distance")
    else:
        print("Invalid input")


#From Project 1 Instructions #CHANGED 
def main():
    puzzle_mode = input("Welcome to 9 Men in a Trench Solver. Type '1' to use a default puzzle, or '2' to create your own."+ '\n')
    if puzzle_mode == "1":
        select_and_init_algorithm(init_default_puzzle_mode()) #algorithm
    if puzzle_mode == "2":
        print("Enter your puzzle, using a zero to represent the blanks. " + "Please only enter puzzles. Enter the puzzle demilimiting " +"the numbers with a space. RET only when finished." + '\n')
        trench = input("Enter the trench state: ")
        trench = trench.split() #split the input string into a list of strings
        for i in range(len(trench)):
            trench[i] = int(trench[i])
        user_puzzle = trench  # 
        select_and_init_algorithm(user_puzzle)
    return 


#From Project 1 Instructions #CHANGED 
def init_default_puzzle_mode():
    selected_difficulty = input("You wish to use a default puzzle. Press 0." + '\n')
    if selected_difficulty == "0":
        print("Difficulty of 'Default' selected.")
        return default

    

#From Project 1 Instructions #CHANGED 
def print_puzzle(puzzle):
    print("Bottom trench:", puzzle[0:10])
    print("Top holes:")
    print("10:", puzzle[10], "11:", puzzle[11], "12:", puzzle[12])
    print('\n')


#CHANGED to 1D list instead of 2D
#Referenced following links: 
# Link: https://docs.python.org/3/tutorial/datastructures.html 
#Link: https://www.w3schools.com/python/python_dictionaries.asp 
#Link:https://stackoverflow.com/questions/16318757/calculating-manhattan-distance-in-python-in-an-8-puzzle-game 
#Link:https://www.geeksforgeeks.org/python-create-dictionary-of-tuples/?ref=ml_lbp 
#Link:https://www.geeksforgeeks.org/python-sorting-a-dictionary-of-tuples/?ref=ml_lbp
#Link:https://www.python-engineer.com/courses/advancedpython/02-tuples/ 

def mapping(goalState): #general function to create dictionary so you can map the values and find out where all the numbers are
    chart = {} #create empty dict - chart that will store location of all tiles currently
    for i in range(len(goalState)):
        if goalState[i] != 0: #dont count the blanks, only map the correct positions of the men
            chart[goalState[i]] = i #1D chart
    return chart
#tile value/number -> key, goal position (i,j) -> value 

#CHANGED
#For manhattan, I referenced the following and the slides as well:
#Link: https://docs.python.org/3/tutorial/datastructures.html 
#Link: https://www.w3schools.com/python/python_dictionaries.asp 
#Link:https://stackoverflow.com/questions/16318757/calculating-manhattan-distance-in-python-in-an-8-puzzle-game 
def heuristics(puzzle, heurName): #returns heuristic
    
    if heurName == "misplaced tile": #is there a man here, and is that man in the wrong place? if so , add 1 to count
        count = 0
        for i in range(len(goalState)): #num of rows
           if puzzle[i] != 0 and puzzle[i] != goalState[i]:#check if goalstate placement is equal to puzzle; ignore 0 because its a blank and we don't care which exact 0 goes in each place
                    count += 1
        return count
    
    elif heurName == "manhattan distance": #need to find shortest distance to goal position for each tile, and add all the ones that arent in the goal position
        trench_hole = {10:3, 11:5, 12:7} #mapping of trench hole positions to their corresponding row numbers (i) in the 1D list (their real pos)
        positions = mapping(goalState)
        distance = 0
        for i in range(len(puzzle)): #goes through entire trench/puzzle
            chosen = puzzle[i] #gets solider at curr index
            if chosen != 0: #if its a man and not a blank
                #if tile is in the hole, use the hole's real position instead
                real_pos = trench_hole.get(i,i) #look up i  in dict, if not there, use i as default

                if i in trench_hole:
                    distance += 1 #if the tile is in the hole, add 1 to the distance because it has to get out of the hole first before it can move to its goal position
                goal_pos = positions[chosen] #find the goal position of the tile we are looking at
                distance += abs(real_pos - goal_pos)

        return distance
    
    elif heurName == "uniform":
        return 0 #for uniform
    else:
        raise ValueError("Invalid Heurisitic Name")


#Notes from TA:
#general search
#empty q-> intialize first node
#while q is not empty, pop front of the q which will return a node (after popping see if the popped node is a goal state or not)
#generate child nodes -> insert in q after getting heuristics
#make a general search function, have the function take in the heurisitc and puzzle
#use heapq since it maintains smallest element/lowest priority at top


#CHANGED
#Referenced this link to understand queues: Link: https://www.geeksforgeeks.org/queue-in-python/#google_vignette 
#Referenced this to understand sets: https://docs.python.org/3/library/stdtypes.html#set 
#More links I referenced (for tuples and such):
#Link: https://www.w3schools.com/python/python_tuples.asp
#Link: https://www.geeksforgeeks.org/python-convert-list-of-lists-to-tuple-of-tuples/ 
#Link: https://docs.python.org/3/tutorial/datastructures.html 
#Link: https://stackoverflow.com/questions/2174124/why-do-we-need-tuples-in-python-or-any-immutable-data-type 
#Link: https://builtin.com/software-engineering-perspectives/python-tuples-vs-lists#:~:text=Tuples%20are%20immutable%20objects%20and,list%20syntax%20uses%20square%20brackets. 

def generalSearch(initialState, heurName):
    nodes = [] #make empty Queue

    starting = time.perf_counter()

    root = (Node(puzzle = initialState, depth = 0, parent = None, heur=heuristics(initialState, heurName)))
    heapq.heappush(nodes, (root.depth + root.heur, root)) #tuple we are using: (cost/priority, node)
    #root.depth + root.heur -> determines which node gets expanded first with using heuristics function
    #Notes: g(n) + h(n) = f(n), smallest f(n) is expanded


    #DOUBLE CHECK U ARE USING MIN HEAP -> yes you are using minheap
    Ongoing = True

    #repeated puzzle states
    visited = set()
    #TESTING
    #count1 = 0
    maxQlen = 0 #find len of the max queue (GRAPH)
    expandedCount = 0 #to find num of expanded nodes (GRAPH)


    while Ongoing: #check heap size instead
        #TESTING
        #print("ongoing")
        if not nodes: #if nodes is empty
            print("Queue empty")
            Ongoing = False
            return Ongoing
        
        maxQlen = max(len(nodes), maxQlen) #find the max length of the queue (GRAPH)
        fnval, node = heapq.heappop(nodes) #remove cheapest node and store the node and its cost
        #TESTING        
        #count1 += 1
        #print(f"count: {count1}")
    
        #convert list of lists into tuple of tuples so i can put it in a set
        #tuples - less memory and faster access
        nodeTuple = tuple(node.puzzle)

        #convert to tuple so you can compare to other tuples
        goalTuple = tuple(goalState)

       
        if(nodeTuple == goalTuple): #if puzzle is at goal state, we are finished
            depth = node.depth #depth of final node
            correctPath = []
            while node: #create a path and reverse it so you can print in correct order
                correctPath.append(node)
                node = node.parent
            correctPath.reverse()
            for i in correctPath:
                print(f"The best state to expand with g(n) = {i.depth} and h(n) = {i.heur} is...")
                print_puzzle(i.puzzle)
            ending = time.perf_counter()

            totalTime = (ending - starting) #caclulate duration
            totalTime = round(totalTime, 4) #round to 5th place
            print(f"Time to Run: {totalTime} seconds")
            print(f"Depth: {depth}")
            print(f"Number of expanded nodes: {expandedCount}")
            print(f"Max Queue Length: {maxQlen}")
            print("Goal Reached!")
            return node

        if nodeTuple in visited:
            #TESTING
            #print("nodeTuple is in visited")
            continue
        
        visited.add(nodeTuple) #updated visited set, was puzzle check before
        #TESTING
        #print("generating child for count", count1)
        expandedCount += 1
        children =  generateChild(node, heurName) #get children notes by expanding/generating childs
        #TESTING
        #print('got here for pusihing children in the queue')
        #print(len(children))
        #add the child nodes to the queue after turning them into hashable tuples
        for i in children:
            if i is not None:
                state = tuple(i.puzzle)
                #TESTING
                #print(f"state:{state} visited: {visited}")
                if state not in visited:
                    # visited.add(state) -> wrong(fixed it.)
                    heapq.heappush(nodes, (i.depth + i.heur, i))
                
        
    return None

    #NOTES
    #keep track of depth
    #keep track of time it takes to run for the graphs       
        
        







if __name__ =="__main__":
    main()