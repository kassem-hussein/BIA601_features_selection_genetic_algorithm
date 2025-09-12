import random
class GeneticAlgorithm:

      # constractor 
      def __init__(self,dataframe,target,X,Y,N_generations = 4,N_populations = 8,model_type='calssification',mutation_rate = 0.1):
            self.__df = dataframe
            self.__target = target
            self.__X = X
            self.__Y = Y
            self.__N_generations = N_generations
            self.__N_populations = N_populations
            self.__model         = model_type
            self.__N_features    = X.shape[1]
            self.__mutation_rate = mutation_rate

      def __init_population(self):
            pass

      def __fitness(self):
            pass
      
      def __crossover(self,first_chromosome,second_chromosome):
            pass
      
      def __mutate(self,chromosome):
            return tuple(1 - bit if random.random() < self.__mutation_rate else bit for bit in chromosome)
      def __predicate(self,chromosome):
            pass
      def start(self):
            pass



      


