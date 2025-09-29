import math
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, r2_score
class GeneticAlgorithm:
      """
      Genetic Algorithm for Feature Selection
      
      This class implements a genetic algorithm to find the optimal subset of features
      for machine learning models using real model performance evaluation.
      """
      
      def __init__(self, dataframe, target, X, Y, N_generations=4, N_populations=8, model_type='classification', mutation_rate=0.1):
            """
            Initialize Genetic Algorithm for Feature Selection
            
            Args:
                dataframe: Original dataframe containing all data
                target: Target column name
                X: Feature matrix (pandas DataFrame)
                Y: Target vector (pandas Series)
                N_generations: Number of generations to run (default: 4)
                N_populations: Population size (default: 8)
                model_type: Type of model ('classification' or 'regression', default: 'classification')
                mutation_rate: Probability of mutation (default: 0.1)
            """
            self.__df = dataframe
            self.__target = target
            self.__X = X
            self.__Y = Y
            self.__N_generations = N_generations
            self.__N_populations = N_populations
            self.__model = model_type
            self.__N_features = X.shape[1]
            self.__mutation_rate = mutation_rate
            self.__fitness_cache = {}

      def __init_population(self):
            """
            Initialize the initial population of chromosomes
            
            Returns:
                list: List of chromosomes (tuples of binary values)
            """
            chromosomes = []
            while len(chromosomes) < self.__N_populations:
                chrom = tuple(random.choice([0, 1]) for _ in range(self.__N_features))
                # Avoid chromosomes with all 0s or all 1s
                if chrom == tuple([0] * self.__N_features) or chrom == tuple([1] * self.__N_features):
                    continue
                else:
                    chromosomes.append(chrom)
            return chromosomes

      def __fitness(self, chromosome):
            """
            Calculate chromosome fitness using correlation-based scoring
            
            Args:
                chromosome: Chromosome to evaluate (binary array)
                
            Returns:
                float: Fitness score based on feature correlations
            """
            if chromosome in self.__fitness_cache:
                return self.__fitness_cache[chromosome]
            
            # Get selected feature columns
            columns = [self.__X.columns[i] for i, bit in enumerate(chromosome) if bit == 1]
            
            if len(columns) == 0:
                self.__fitness_cache[chromosome] = 0.0
                return 0.0
            
            # Calculate correlation sum
            correlations = self.__df.corr()[self.__target].drop(self.__target).abs()[columns].sum()
            
            # Calculate weighted fitness score
            val = round(correlations * (correlations / len(columns)), 8)
            self.__fitness_cache[chromosome] = val
            return val

      def __crossover(self, first_chromosome, second_chromosome):
            """
            Perform crossover operation between two chromosomes
            
            Args:
                first_chromosome: First parent chromosome
                second_chromosome: Second parent chromosome
                
            Returns:
                list: List containing two offspring chromosomes
            """
            # Select two random crossover points
            p1, p2 = sorted(random.sample(range(len(first_chromosome)), 2))
            
            # Create offspring by swapping segments between parents
            child1 = first_chromosome[:p1] + second_chromosome[p1:p2] + first_chromosome[p2:]
            child2 = second_chromosome[:p1] + first_chromosome[p1:p2] + second_chromosome[p2:]
            
            return [child1, child2]

      def __mutate(self, chromosome):
            """
            Apply mutation to a chromosome
            
            Args:
                chromosome: Chromosome to mutate
                
            Returns:
                tuple: Mutated chromosome
            """
            return tuple(1 - bit if random.random() < self.__mutation_rate else bit for bit in chromosome)

      def __predicate(self, chromosome):
            """
            Evaluate chromosome fitness based on model accuracy
            
            Args:
                chromosome: Chromosome to evaluate (binary array)
                
            Returns:
                float: Model accuracy (accuracy_score or r2_score)
            """
            # 1. Select active columns (features)
            selected_columns = [i for i, bit in enumerate(chromosome) if bit == 1]
            
            # 2. Check if features are selected
            if len(selected_columns) == 0:
                return 0.0  # Cannot build model without features
            
            # 3. Check if not all features are selected
            if len(selected_columns) == len(chromosome):
                return 0.0  # No benefit from feature selection
            
            # 4. Check reasonable feature ratio (optional)
            feature_ratio = len(selected_columns) / len(chromosome)
            if feature_ratio > 0.8:  # More than 80% of features
                return 0.0
            
            # Split data into train and test sets
            X_train, X_test, Y_train, Y_test = train_test_split(
                self.__X, self.__Y, test_size=0.2, random_state=42
            )
            
            # Choose model and evaluation metric based on problem type
            if self.__model == 'classification':
                model = RandomForestClassifier(random_state=42)
                acc = accuracy_score
            else:
                model = RandomForestRegressor(random_state=42)
                acc = r2_score
            
            # Train model and make predictions
            try:
                model.fit(X_train.iloc[:, selected_columns], Y_train)
                preds = model.predict(X_test.iloc[:, selected_columns])
                accuracy = acc(Y_test, preds)
                return accuracy
            except Exception as e:
                # Handle any unexpected errors
                print(f"Error evaluating chromosome: {e}")
                return 0.0

      def start(self):
            """
            Start the genetic algorithm optimization process
            
            Returns:
                tuple: selected feautres,fitness_value,accuracy,length of selected features,total features,generations
            """
            print("Loadding...")

            population = self.__init_population()
            fitness_values = []

            # Initial fitness evaluation
            for chrom in population:
                score = self.__fitness(chrom)
                fitness_values.append((score, chrom))

            generations_child = []
            for gen in range(self.__N_generations):
                fitness_values =sorted(fitness_values, key=lambda x: x[0], reverse=True)
                print(f"\n Generation {gen + 1}")
                parents = [fitness_values[i][1] for i in range(3)]
                children = []
                children +=self.__crossover(parents[0], parents[1])
                children +=self.__crossover(parents[0], parents[2])
                children +=self.__crossover(parents[1], parents[2])
      
                genration = []
                for child in children:
                        mutated = self.__mutate(child)
                        if mutated in [tuple([0]*self.__X.shape[1]), tuple([1]*self.__X.shape[1])]:
                            continue
                        fitness_value = self.__fitness(mutated)
                        item = {}
                        item["child"] = mutated
                        item["fitness"] =fitness_value
                        item['features'] =sum([bit for bit in mutated if bit == 1])
                        genration.append(item)
                        fitness_values.append((fitness_value, mutated))
                generations_child.append(genration)
            best = fitness_values[0]
            fitness_value = self.__fitness(best[1])
            accuracy = self.__predicate(best[1])
            selected_features = [self.__X.columns[i] for i, bit in enumerate(best[1]) if bit == 1]
            return (selected_features,fitness_value,accuracy,len(selected_features),self.__X.shape[1],generations_child)

            
            

