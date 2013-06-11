import time, math, random, pygame, os, sys
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((640,480))

CREATURE_COUNT = 20
NEURON_COUNT = 20
SECONDS_PER_CREATURE = 0.05
STEPS_PER_SIMULATION = 10
CHANCE_OF_MUTATION = 0.01
AMMOUNT_OF_MUTATION = 2
SECONDS_TO_RUN = 1

class creature:
     def __init__(self, noOfNeurons):
          self.error = 0
          self.neuronList = list()
          self.synapseList = list()
          for n in range(noOfNeurons):
               X = int(320+200*math.cos(n*2*math.pi/(noOfNeurons)))
               Y = int(240+200*math.sin(n*2*math.pi/(noOfNeurons)))
               if (n == 0):
                    color = (0,random.randint(0,255),0)
               elif (n == 1):
                    color = (random.randint(0,255),0,0)
               else:
                    color = (random.randint(0,200),random.randint(0,200),random.randint(0,255))
               radius = 15
               self.neuronList.append(neuron(X,Y, color, radius))
          for n in self.neuronList:
               for l in self.neuronList:
                    self.synapseList.append(synapse(n,l))

class neuron:
     def __init__(self, X, Y, color, radius):
          self.X = X
          self.Y = Y
          self.boxThreshold = random.random()
          self.inbox = random.random()
          self.box = random.random()
          self.color = color
          self.radius = radius
          self.time = 0
          self.timeThreashold = random.randint(0,4)
          self.fireStrength = random.random()
          self.boxDrain = random.random()

class synapse:
     def __init__(self, N1, N2):
          self.neuron1 = N1
          self.neuron2 = N2
          self.weight = random.random()

def drawCreature(creature):
     screen.fill((255,255,255))
     for n in creature.neuronList:
          n.X = int(320+200*math.cos(creature.neuronList.index(n)*2*math.pi/(len(creature.neuronList))))
          n.Y = int(240+200*math.sin(creature.neuronList.index(n)*2*math.pi/(len(creature.neuronList))))

     for s in creature.synapseList:
          pygame.draw.line(screen, (0,0,0), (s.neuron1.X, s.neuron1.Y), (s.neuron2.X, s.neuron2.Y), 1)

     for n in creature.neuronList:
          if (n.box>n.boxThreshold):
               newColor = (int((n.color[0]+255)/2),int((n.color[1]+255)/2),int((n.color[2]+255)/2))
               pygame.draw.circle(screen, newColor, (n.X,n.Y), n.radius)
          else:
               pygame.draw.circle(screen, n.color, (n.X,n.Y), n.radius)

          font = pygame.font.Font(None, 18)
          text1 = font.render(str(round(n.box,2)), 1, (10, 10, 10))
          text2 = font.render(str(round(n.boxThreshold,2)), 1, (10, 10, 10))
          text3 = font.render("Top number is neuron value", 1, (10, 10, 10))
          text4 = font.render("Bottom number is neuron threshold", 1, (10, 10, 10))
          textpos1 = text.get_rect()
          textpos2 = text.get_rect()
          textpos1.centerx = n.X
          textpos1.centery = n.Y
          textpos2.centerx = n.X
          textpos2.centery = n.Y+12
          screen.blit(text1, textpos1)
          screen.blit(text2, textpos2)
          screen.blit(text3, (0,0))
          screen.blit(text4, (0,12))
     pygame.display.update()

def stepCreature(creature):
     for n in creature.neuronList:
          #if n.time > n.timeThreashold:     '''add this in to have neurons require a reuptake time between fires'''
               #if n.box > n.boxThreshold:   '''add this in to have neurons fire instead of run constantly'''
          sList = findSynapses(creature,n)
          for s in sList:
               s.neuron2.inbox += n.fireStrength * n.box * s.weight
          n.time = 0
          n.box = 0
     for n in creature.neuronList:
          n.time += 1
          n.box += n.inbox
          n.box = n.box * n.boxDrain
          n.inbox = 0
     return creature

def findSynapses (creature, neuron):
     sList = list()
     for s in creature.synapseList:
          if (s.neuron1 == neuron) :
               sList.append(s)
     return sList

def simulateCreature (creature, noOfSteps, inputNeuron, inputValue, outputNeuron, outputValue):
     creature.error = 0
     for step in range(noOfSteps):
          creature.neuronList[inputNeuron].box = inputValue
          creature = stepCreature(creature)
     creature.error += abs(outputValue - creature.neuronList[outputNeuron].box)
     creature.neuronList[inputNeuron].box = inputValue
     return creature

def trainPopulation(population, inputDataSet, outputDataSet): #data sets are array of the same length
     for c in population:
          for i in range(len(inputDataSet)):
               inD = inputDataSet[i]
               outD = inputDataSet[i]
               c = simulateCreature(c, STEPS_PER_SIMULATION, 0, inD, 1, outD)
     return population

def mate (mother, father):
     child = creature(len(mother.neuronList))
     n = child.neuronList
     m = mother.neuronList
     f = father.neuronList
     for i in range(len(child.neuronList)):
          n[i].boxThreshold   = random.choice( [m[i].boxThreshold,   f[i].boxThreshold]   )
          n[i].fireStrength   = random.choice( [m[i].fireStrength,   f[i].fireStrength]   )
          n[i].boxDrain       = random.choice( [m[i].boxDrain,       f[i].boxDrain]       )
          n[i].timeThreashold = random.choice( [m[i].timeThreashold, f[i].timeThreashold] )

     s = child.synapseList
     m = mother.synapseList
     f = father.synapseList
     for i in range(len(child.synapseList)):
          s[i].weight = random.choice( [m[i].weight, f[i].weight] )

     return child

def mutatePopulation (population, chanceOfMutation, ammountOfMutation):
     for c in population:
          for n in c.neuronList:
               if (random.random() <= chanceOfMutation):
                    n.boxThreshold *= ammountOfMutation * random.random()
               if (random.random() <= chanceOfMutation):
                    n.fireStrength *= ammountOfMutation * random.random()
               if (random.random() <= chanceOfMutation):
                    n.boxDrain *= ammountOfMutation * random.random()
               if (random.random() <= chanceOfMutation):
                    n.timeThreashold += random.randint(-1,1)
          for s in c.synapseList:
               if (random.random() <= chanceOfMutation):
                    s.weight *= ammountOfMutation * random.random()
     return population


def generateStartingPopulation():
     population = list()
     for c in range( CREATURE_COUNT ):
          population.append( creature( NEURON_COUNT ) )
     return population

def getAvgErrorOfPopulation(population):
     summation = 0
     populationCount = len(population)
     for c in population:
          summation += c.error
     avgError = summation / populationCount
     return avgError

def pruneUnfitCreatures(population, avgError):
     for c in population:
          if (c.error > avgError):
            population.remove(c)
     return population

def repopulate(population):
     p = list(population)
     while (len(population) < CREATURE_COUNT):
          mother = random.choice( p )
          father = random.choice( p )
          if not (mother == father):
            population.append( mate( mother , father ) )
     return population

#create a list of creatures
population = generateStartingPopulation()
inputDataSet = [1]
outputDataSet = [1]
stopTime = time.time()+SECONDS_TO_RUN

while time.time()<stopTime:
     #mutate all properties of all creatures in population with CHANCE_OF_MUTATION
     popultion = mutatePopulation( population, CHANCE_OF_MUTATION, AMMOUNT_OF_MUTATION )
     #train all creatures on a data set
     population = trainPopulation(population, inputDataSet, outputDataSet)
     #find average error in population
     averageError = getAvgErrorOfPopulation(population)
     #remove creatures from population with below average error
     population = pruneUnfitCreatures(population, averageError)
     #crossbreed randomly chosen parents from the remaining population and append them to population until at CREATURE_COUNT
     population = repopulate(population)

     for event in pygame.event.get():
          if event.type == QUIT:
               pygame.quit()
               sys.exit()

          '''
          elif event.type is pygame.KEYDOWN:
               keyname = pygame.key.name(event.key)
               if keyname == "space":
                    print "space"
                    draw
          '''

bestCreature = population[0]
for c in population:
     if (c.error < bestCreature.error):
          bestCreature = c
for step in range(10):
          bestCreature.neuronList[0].box = inputDataSet[0]
          bestCreature = stepCreature(creature)
drawCreature(bestCreature)
