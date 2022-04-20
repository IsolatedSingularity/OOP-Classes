#Importing Modules
import math
from random import randint
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

#Matplot settings
plt.ion() # enable interactive mode (continue graphing without having to close the window)
plt.show() # show the plot

#Defining Class Instances

#Sign of position of elevator
def sign(x):
    # return the sign of x (0 if x is 0).
    if x > 0: # x positive
        return 1
    elif x < 0: # x negative
        return -1
    else: # x zero
        return 0

#Parameters of elevator
class Point3D():
    def __init__(self, x, y, z): # class constructor
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
    
    def __eq__(self, other): # comparison
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __str__(self): # string representation
        return '<{}, {}, {}>'.format(self.x, self.y, self.z)
    
    def add(self, other): # add two points together
        return Point3D(self.x+other.x, self.y+other.y, self.z+other.z)
    
    def distance(self, other): # get distance between two points
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)
    
    def get_direction_vector(self, other):
        # return a vector of 1, 0 or -1 in each dimension corresponding to
        # the direction you would have to move from the self point to get to the other point.
        return Point3D(sign(other.x-self.x), sign(other.y-self.y), sign(other.z-self.z))
    
    def aslist(self): # Return the Point2D object as a list of three numbers.
        return [self.x, self.y, self.z]

def get_random_point(x0, x1, y0, y1, z0, z1):
    # return a Point3D object with random coordinates within the given x,y,z intervals.
    return Point3D(randint(x0, x1), randint(y0, y1), randint(z0, z1))

#Population being picked up and dropped off by evelator
class Person:
    def __init__(self, nameOfPerson, currentPosition, destinationPosition):
        self.name = nameOfPerson # the name of the person 
        self.cur_pos = currentPosition # the current position of the person (a Point3D obect)
        self.dst_pos = destinationPosition # the destination position of the person (a Point3D obect)
        self.arrived = False # whether or not the person has arrived at their destination, set to default as False (or else they wouldn't need the elevator) 
                             
        pass
    
    def arrive_at_destination(self):
        self.cur_pos = self.dst_pos
        self.arrived = True
        
    def __str__(self): # string representation
        return "Name:" + self.name + "; cur: " + str(self.cur_pos) + "; dst:" + str(self.dst_pos)

#Ambient space of elevator with population in it
class Factory:
    def __init__(self, factory_size, people, elevator): # class constructor
        self.factory_size = factory_size
        self.people = people
        self.elevator = elevator
        
        self.axes = plt.axes(projection='3d')
    
    def run(self):
        
        #Iterating through each person (object) in the list of people, i.e. the 'people' attribute of the Factory class
        for person in self.people:
            #Proceeds if and only if (iff) there is atleast one person in the elevator 
            if person in self.elevator.people_in_elevator:
                #Proceeds iff the person's destination is the current room
                if self.elevator.cur_pos == person.dst_pos:
                    #The person needs to be dropped off in the room (their destination)
                   self.elevator.person_leaves(person)
            #Else: there is atleast one person in the same room as the elevator and needs to be picked up
            else:
                #Proceeds iff that person needs to be picked up, has not already arrived at their destination room, and if the person is at the same room as the elevator 
                if (not person.arrived) and (person not in self.elevator.people_in_elevator) and (self.elevator.cur_pos == person.cur_pos):
                    #The person need to be picked up
                    self.elevator.person_enters(person)
        # Move the elevator.
        if not self.is_finished():
            self.elevator.move(self.people)
    
    def show(self): # display the grid
        self.axes.clear() # clear the previous window contents
        
        # set the axis bounds
        self.axes.set_xlim(0, factory_size.x)
        self.axes.set_ylim(0, factory_size.y)
        self.axes.set_zlim(0, factory_size.z)
        self.axes.set_xticks(list(range(factory_size.x+1)))
        self.axes.set_yticks(list(range(factory_size.y+1)))
        self.axes.set_zticks(list(range(factory_size.z+1)))
        
        # show a blue dot for each person not yet in the elevator / not yet arrived at their destination
        xs, ys, zs = [], [], []
        for person in self.people:
            if not person.arrived and person not in self.elevator.people_in_elevator:
                xs.append(person.cur_pos.x)
                ys.append(person.cur_pos.y)
                zs.append(person.cur_pos.z)
        self.axes.scatter3D(xs, ys, zs, color='blue')
        
        # show a red dot for the destinations of the people currently in the elevator
        edxs, edys, edzs = [], [], []
        for person in self.people:
            if person in self.elevator.people_in_elevator:
                edxs.append(person.dst_pos.x)
                edys.append(person.dst_pos.y)
                edzs.append(person.dst_pos.z)
        self.axes.scatter3D(edxs, edys, edzs, color='red')
        
        # show a green dot for the elevator itself
        self.axes.scatter3D([self.elevator.cur_pos.x], [self.elevator.cur_pos.y], [self.elevator.cur_pos.z], color='green')
        
        plt.draw()
        plt.pause(0.5)
    
    def is_finished(self):
        return all(person.arrived for person in self.people)
    
#Elevator itself
class Wonkavator:
    def __init__(self, factory_size): # class constructor
        self.cur_pos = Point3D(0, 0, 0)
        self.factory_size = factory_size
        self.people_in_elevator = [] # the list of people currently in the elevator
        
    def move(self, people): # move the elevator
        # get the direction in which to move      
        direction = self.choose_direction(people)
        
        # check if the direction is correct
        if any(not isinstance(d, int) for d in direction.aslist()):
            raise ValueError("Direction values must be integers.")
        if any(abs(d) > 1 for d in direction.aslist()):
            raise ValueError("Directions can only be 0 or 1 in any dimension.")
        if all(d == 0 for d in direction.aslist()):
            raise ValueError("The elevator cannot stay still (direction is 0 in all dimensions).")
        if any(d < 0 or d > s for d, s in zip(self.cur_pos.add(direction).aslist(), self.factory_size.aslist())):
            raise ValueError("The elevator cannot move outside the bounds of the grid.")
        
        # move the elevator in the correct direction
        self.cur_pos = self.cur_pos.add(direction)
        
    def choose_direction(self, people):
        '''Please add a clear description for the function here. Please make reference to the parameters, the returned value (if any) and the functionality of the function. 
        ''' 
        if len(self.people_in_elevator) == 0: #proceeds through the condition if and only if (iff) the elevator is empty (the 'self.people_in_elevator' attribute of Wonkavator class list is empty)
            closest_dist = math.inf #defines the closest distance from the elevator to a nearby person as positive infinity, this is meant to be used as a point of reference for all future distances to be compared to
            for person in people: #iterates over every person in the provided list of people in the building (the list being the 'people' parameter in the choose_direction method, originally from Factory class)
                if not person.arrived and person not in self.people_in_elevator: #proceeds iff the current person in the building isn't at their destination, nor are they in the elevator
                    dist = person.cur_pos.distance(self.cur_pos) #computes the distance between the current person's position ('person.cur_pos') and the elevator's current position ('self.cur_pos')
                    if dist < closest_dist: #proceeds iff the distance between the current person's position and the elevator's current position is less than currently defined closest distance variable 'closest_dist' (currently set as positive infinity) 
                        closest_dist = dist #replaces the original definition of 'closest_dist' with 'dist' (distance between current person and elevator) as dist is now the closest distance (compared to positive infinity)
                        direction = self.cur_pos.get_direction_vector(person.cur_pos) #computes the direction the elevator will travel to pick up the nearby person
        else: #proceeds iff the above condition failed, i.e. the elevator is not empty
            closest_dist = math.inf #once again, defining our point of reference at positive infinity
            for person in self.people_in_elevator: #iterating through the people in the now non-empty elevator
                dist = person.dst_pos.distance(self.cur_pos) #computing the distance between the elevator's current position ('self.cur_pos', which is also simultaneously the current person's current position) and the current person's destination position ('person.dst_pos')
                if dist < closest_dist: #proceeds iff the distance between the elevator and the current person's position is less than 'closest_dist' (positive infinity)
                    closest_dist = dist #replaces the original definition of 'closest_dist' with 'dist' since the distance between the elevator and the current person's destination is now the closest distance (compared to positive infinity)
                    direction = self.cur_pos.get_direction_vector(person.dst_pos) #computes the direction the elevator will travel to drop the person off
        return direction #returns the direction vector, either telling the elevator where to move to pick the nearest person up, or to drop off the current person
      
    def person_enters(self, person): # person arrives in elevator
        if person.arrived:
            raise Exception("A person can only enter the elevator if they have not yet reached their destination.")
        
        self.people_in_elevator.append(person) # add them to the list
    
    def person_leaves(self, person): # person departs elevator
        if person.dst_pos != elevator.cur_pos:
            raise Exception("A person can only leave the elevator if the elevator has reached their destination point.")
        
        person.arrive_at_destination() # let the person know they have arrived
        self.people_in_elevator.remove(person) # remove them from the list

if __name__ == '__main__':    
    factory_size = Point3D(5, 5, 5)
    
    # create the people objects
    people = []
    for name in ["Candice", "Arnav", "Belle", "Cecily", "Faizah", "Nabila", "Tariq", "Benn"]:
        cur = get_random_point(0, factory_size.x-1, 0, factory_size.y-1, 0, factory_size.z-1)
        dst = get_random_point(0, factory_size.x-1, 0, factory_size.y-1, 0, factory_size.z-1)
        people.append(Person(name, cur, dst))
    
    # create the elevator
    elevator = Wonkavator(factory_size)
    
    # create the factory
    factory = Factory(factory_size, people, elevator)
    
    while True:
        factory.run()
        factory.show()
        
        # check if everyone has arrived at their destinations
        if factory.is_finished():
            break
    
    print("Everyone has arrived.")
