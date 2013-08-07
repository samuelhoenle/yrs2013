'''Virus spreading simulation using movement of people as given by fake.py

Format is 
{id: {time : position}}

'''
#Options
fin = 'movement-50.dat'

###
from sets import Set
import pickle, random
from collections import defaultdict

ms = pickle.load(open(fin))

class Simulation(object):
	def __init__(self, movement):
		#self.movement = movement
		#Create a blank node for each position and initialise queue with initial positions
		self.locations = {x: Location() for x in movement}
		self.queue = defaultdict(list, {0: [People(v, x.iteritems()) for v,x in movement.items()]})
		self.stage = 0
		self.people = self.queue[0]
	def step(self):
		#empty queue for the step and move people
		for person in self.queue[self.stage]:
			try:
				new_time, new_location = person.movement.next()
				person.move(self.locations[person.nextLocation])
				self.queue[new_time].append(person)
				person.nextLocation = new_location
			except StopIteration:
				# No more movement from that person
				print str(person.name) + " end of cycle"
		#carry out infection on each locatio.add
		for cell in self.locations.itervalues():
			cell.infect()
		self.stage+=1
	
	#utility functions
	def infected(self): return [person.name for person in self.queue[0] if person.infected]
	def positions(self):
		for name, location in self.locations.iteritems():
			inf = 'I' if  any(map(lambda x: x.infected, location.contents)) else ''
			print inf + ' ' + str(name) + ' - ' + ','.join(map(lambda x: str(x.name), location.contents))		
			

#possible position 
class Location(object):
	def __init__(self):
		self.contents = []
		self.infected = 0
	
	#trigger infection event on all present people
	def infect(self):
		if self.infected:
			for x in self.contents: x.infect()
	
	#person entering location
	def into(self, p):
		self.contents.append(p)
		if p.infected: self.infected += 1
		
	#person leaving location
	def leave(self, p):
		self.contents.remove(p)
		if p.infected: self.infected -= 1
	
#person class
class People(object):
	def __init__(self, name, move):
		self.name = name
		self.infectcount = 0
		self.infected = False
		self.location = None
		time, location = move.next()
		self.nextLocation = location
		#iterator of movement locations and times	
		self.movement = move
	def infect(self):
		#infection logic
		if self.infectcount == 10: self.infected = True
		elif self.infectcount > 5 and random.random() > 0.5: self.infected = True
		self.infectcount += 1
	
	def move(self, new):
		if self.location: self.location.leave(self)
		self.infectcount = 0
		self.location = new
		new.into(self)

s = Simulation(ms)
