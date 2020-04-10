from Chromosome import Chromosome,generateARandomPermutation
from random import random,randint
from math import sqrt

class GA:
    def __init__(self,path):
        self.__path = path
        self.__param = self.__readData()
        self.__population = self.__initPopulation()

    def __fitnessCalculator(self, repr):
        fitness=0.0
        for i in range(0,len(repr)-1):
            fitness+=self.__param['mat'][repr[i]][repr[i+1]]
        fitness+=self.__param['mat'][repr[-1]][repr[0]]
        return fitness

    def __initPopulation(self):
        list = []
        for _ in range(0, 100):
            c = Chromosome(self.__param)
            c.fitness = self.__fitnessCalculator(c.repres)
            list.append(c)
        return list

    def __choose(self):
        a = randint(0, 100 -1)
        b = randint(0, 100 -1)
        if (self.__population[a].fitness < self.__population[b].fitness):
            return a
        else:
            return b

    def __bestCromo(self):
        best=self.__population[0]
        for c in self.__population:
            if c.fitness<best.fitness:
                best=c
        return best

    def __oneGeneration(self):
        newPopulation = [self.__bestCromo()]
        for _ in range(100 - 1):
            p1 = self.__population[self.__choose()]
            p2 = self.__population[self.__choose()]
            offspring = p1.crossover(p2)
            offspring.mutation()
            offspring.fitness = self.__fitnessCalculator(offspring.repres)
            newPopulation.append(offspring)
        return newPopulation

    def solution(self):
        best=self.__bestCromo()
        for _ in range(0,1000):
            self.__population = self.__oneGeneration()
            current_best=self.__bestCromo()
            if current_best.fitness<best.fitness:
                best=current_best
            print(current_best.fitness)
        self.__write_data(best)
        return best

    def __readData(self):
        with open(self.__path, "r") as file:
            noNodes = int(file.readline())
            mat=[]
            for _ in range(noNodes):
                line=file.readline()
                mat.append([])
                values = line.split(",")
                for i in values:
                    mat[-1].append(int(i))
        return {'noNodes':noNodes,'mat':mat}

    '''
    def __readData2(self):
        noNodes=0
        with open(self.__path,'r') as file:
            noduri = dict()
            for _ in range(6):
                file.readline()
            line=file.readline()
            while (line)!="EOF":
                values=line.split(" ")
                node=int(values[0])
                x=int(values[1])
                y=int(values[2])
                if node not in noduri:
                    noduri[node]=[x,y]
                noNodes = noNodes + 1
                line=file.readline()
        mat=[[0 for _ in range(noNodes)]
            for _ in range(noNodes)]
        for i in noduri:
            for j in noduri:
                a=noduri[i][0]
                b=noduri[i][1]
                c=noduri[j][0]
                d=noduri[j][1]
                dist=sqrt((a-c)**2+(b-d)**2)
                mat[i-1][j-1]=dist
        return {'noNodes':noNodes,'mat':mat}
    '''

    def __write_data(self,best):
        fileName=self.__path.split('.')[0]+'_solution.txt'
        with open(fileName,'w') as file:
            file.write(str(self.__param['noNodes'])+'\n')
            for i in range(len(best.repres)-1):
                file.write(str(best.repres[i]+1)+',')
            file.write(str(best.repres[-1]+1)+'\n')
            file.write(str(best.fitness)+'\n')