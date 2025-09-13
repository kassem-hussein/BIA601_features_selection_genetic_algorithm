import math
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

      def __fitness(self, chromosome):
            columns = [self.__X.columns[i] for i, bit in enumerate(chromosome) if bit == 1]
            if len(columns) == 0:
                     return 0.0
            correlations = 0.0
     
            for col in columns:
               res = self.__df[self.__target].corr(self.__df[col] )
               res = float(res)
            if not math.isnan(res):
              correlations += abs(res)
            return round(correlations * (correlations / len(columns)), 8)
        

           
      
      def __crossover(self,first_chromosome,second_chromosome):
            p1, p2 = sorted(random.sample(range(len(a)), 2))
            child1 = first_chromosome[:p1] + second_chromosome[p1:p2] + first_chromosome[p2:]
            child2 = second_chromosome[:p1] + first_chromosome[p1:p2] + second_chromosome[p2:]
            return [child1, child2]
      
      def __mutate(self,chromosome):
            return tuple(1 - bit if random.random() < self.__mutation_rate else bit for bit in chromosome)
      def __predicate(self,chromosome):
            pass
      def start(self):
            pass



      


