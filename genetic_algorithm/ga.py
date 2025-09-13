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
         chromosomes = []
         for _ in range( self.__N_populations):
            chrom = tuple(random.choice([0,1]) for _ in range( self.__N_features))
            if chrom  == ([0]* self.__N_features) or chrom == ([1]*  self.__N_features):
                  continue
            else :
               chromosomes.append(chrom)
         return chromosomes   

    

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



      


