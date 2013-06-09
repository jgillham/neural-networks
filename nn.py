import time, math, random, pygame, os, sys
from pygame.locals import *

NUMBER_OF_NEURONS = 10
NUMBER_OF_SYNAPSES = 75
pygame.init()
screen = pygame.display.set_mode((640,480))
screen.fill((255,255,255))

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
          
neuronList = []
synapseList = []
def generateNeurons(neuronCount):
     for i in range (0,neuronCount):
          X = int(320+200*math.cos(i*2*math.pi/(neuronCount)))
          Y = int(240+200*math.sin(i*2*math.pi/(neuronCount)))
          color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
          radius = 15
          neuronList.append(neuron(X,Y, color, radius))


def generateRandomSynapses(synapseCount, neuronCount):
     index = 0
     startTime = time.time()
     while (index < synapseCount and time.time()<startTime+2):
          n1 = neuronList[random.randint(0,neuronCount-1)]
          n2 = neuronList[random.randint(0,neuronCount-1)]
          badSynapseFlag = 0
          for s in synapseList:
               if n1 == s.neuron1 and n2 == s.neuron2:
                    badSynapseFlag = 1
               #elif n2 == s.neuron1 and n1 == s.neuron2: #uncomment to allow synapses to be built in both directions
               #     badSynapseFlag = 1
               elif n1 == n2:
                    badSynapseFlag = 1
          if badSynapseFlag == 0:
               synapseList.append(synapse(n1,n2))
               index+=1
     
def drawAll():
     screen.fill((255,255,255))
     for n in range(len(neuronList)):
          neuronList[n].X = int(320+200*math.cos(n*2*math.pi/(len(neuronList))))
          neuronList[n].Y = int(240+200*math.sin(n*2*math.pi/(len(neuronList))))
     for i in range (0,len(synapseList)):
          pygame.draw.line(screen, ((synapseList[i].neuron1.color[0]+synapseList[i].neuron2.color[0])/2,(synapseList[i].neuron1.color[1]+synapseList[i].neuron2.color[1])/2,(synapseList[i].neuron1.color[2]+synapseList[i].neuron2.color[2])/2), (synapseList[i].neuron1.X, synapseList[i].neuron1.Y), (synapseList[i].neuron2.X, synapseList[i].neuron2.Y), 3)

     for i in range (0,len(neuronList)):
          pygame.draw.circle(screen, neuronList[i].color, (neuronList[i].X,neuronList[i].Y), neuronList[i].radius)
          if (neuronList[i].box>neuronList[i].boxThreshold):
               pygame.draw.circle(screen, (255,255,0), (neuronList[i].X,neuronList[i].Y), int(neuronList[i].radius/2))
               for s in synapseList:
                    if s.neuron1 == neuronList[i]:
                         pygame.draw.line(screen, (255,255,0), (s.neuron1.X, s.neuron1.Y), (s.neuron2.X, s.neuron2.Y), 2)
         
          font = pygame.font.Font(None, 18)
          text = font.render(str(round(neuronList[i].box,2)), 1, (10, 10, 10))
          text2 = font.render(str(round(neuronList[i].boxThreshold,2)), 1, (10, 10, 10))
          text3 = font.render("Top number is neuron value", 1, (10, 10, 10))
          text4 = font.render("Bottom number is neuron threshold", 1, (10, 10, 10))
          text5 = font.render("Press Space Bar to step forward", 1, (10, 10, 10))
          textpos = text.get_rect()
          textpos2 = text.get_rect()
          textpos.centerx = neuronList[i].X
          textpos.centery = neuronList[i].Y
          textpos2.centerx = neuronList[i].X
          textpos2.centery = neuronList[i].Y+12
          screen.blit(text, textpos)
          screen.blit(text2, textpos2)
          screen.blit(text3, (0,0))
          screen.blit(text4, (0,12))
          screen.blit(text5, (0,24))
     pygame.display.update()
     
generateNeurons(NUMBER_OF_NEURONS)
generateRandomSynapses(NUMBER_OF_SYNAPSES, NUMBER_OF_NEURONS)
drawAll()

#find neurons attached to argument neuron
#return as a list of neurons
def connections(neuron):
     connectedNeurons = list()
     for s in synapseList:
          if s.neuron1 == neuron:
               connectedNeurons.append((s.neuron2, s.weight)) #tuples of neuron and weight
     return connectedNeurons

while 1:
     for event in pygame.event.get():
          if event.type == QUIT:
               pygame.quit()
               sys.exit()
          elif event.type is pygame.KEYDOWN:
               keyname = pygame.key.name(event.key)
               if keyname == "space":
                    print "executing..."
                    for n in neuronList:
                         if n.time > n.timeThreashold:
                              if n.box > n.boxThreshold:
                                   connectionList = connections(n)#array of tuples with neuron and weight
                                   for n2 in connectionList:
                                             n2[0].inbox += n.fireStrength * n2[1]#fire strength * synapse weight
                                   n.time = 0
                                   n.box = 0
                    for n in neuronList:
                         n.time += 1
                         n.box += n.inbox
                         n.box = n.box*n.boxDrain
                         n.inbox = 0
                    drawAll()
