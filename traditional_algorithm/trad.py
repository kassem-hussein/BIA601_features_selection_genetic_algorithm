from itertools import combinations
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, r2_score
class TraditionalAlgorithm:

      def __init__(self,df,X,Y,target,model_type):
            '''
                  Args:
                        df: dataframe have features and target columns 
                        X : dataframe of features without target column
                        Y : Series for target column
                        target: target column name
                        model_type : type of model for problem (classification or regression)
            '''
            self.__x= X
            self.__y= Y
            self.__model= model_type
            self.__df = df
            self.__target = target
            self.__cache = {}
      def __generate(self):
            '''
                  Args:
                        No thing
                        
                  Return : List of  Possibale solution for select features ways
            '''
            all_combinations = []
            for r in range(1, len(self.__x,) +1):
                  all_combinations.extend(combinations(self.__x, r))
            return all_combinations
      
      def __evaluation(self,combination):
            '''
                  Args:
                        combination tuple of selected features
                  return:
                        sum absolute values of correleation for selected features with target column

            '''
            # avoid selected all feature
            if len(combination) == self.__x.shape[1]:
                  return 0.0
            # avoid No features selected 
            if len(combination) == 0:
                  return 0.0
            # accpet ratio of selected features should be lt 0.7
            if ( len(combination) / self.__x.shape[1]) > 0.7:
                  return 0.0
            if combination in self.__cache:
                  return self.__cache[combination]
            corr = self.__df.corr()[self.__target].drop(self.__target).abs()
            val  = corr[list(combination)].sum()
            self.__cache[combination] =val
            return val
      def __predicate(self,combination):
            '''
                  Args:
                        combination tuple of selected features 
                  return 
                        accuracy of combination  

            '''
            
            # Split data into train and test sets
            X_train, X_test, Y_train, Y_test = train_test_split(
                self.__x, self.__y, test_size=0.2, random_state=42
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

                model.fit(X_train[list(combination)], Y_train)
                preds = model.predict(X_test[list(combination)])
                accuracy = acc(Y_test, preds)
                return accuracy
            except Exception as e:
                # Handle any unexpected errors
                print(f"Error evaluating chromosome: {e}")
                return 0.0      
      
      def start(self):
            '''
                  Args:
                        No args
                  Return:
                        tuple of accuracy and combination 
            '''
            combinations = self.__generate()
            items = []
            for comb in combinations:
                  val = self.__evaluation(combination=comb)
                  items.append((val,comb))
            items = sorted(items, key=lambda x: x[0], reverse=True)
            item  = items[0] 
            combination = item[1]
            acc   = self.__predicate(combination=combination)
            return (acc,combination)
            
                  
            
            


