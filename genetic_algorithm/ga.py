import math


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

      def fitness(self, chromosome):
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
            pass
      
      def __mutate(self,chromosome):
            pass
      def __predicate(self,chormosome):
            pass
      def start(self):
            pass



      


