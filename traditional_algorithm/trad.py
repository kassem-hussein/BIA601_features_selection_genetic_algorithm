from itertools import combinations
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import f_classif,f_regression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, r2_score
import pandas as pd
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
            self.__model_select = f_classif if model_type == 'classification' else f_regression
            self.__model= RandomForestClassifier() if model_type== 'classification' else RandomForestRegressor() 
            self.__acc_f = accuracy_score  if model_type == 'classification' else r2_score
            self.__df = df
            self.__target = target
            self.__cache = {}
      def __get_selected_features(self):
            '''
                  Args:
                        No thing
                        
                  Return : List of  selected feauture using SelectFromModel from scikit-learn 
            '''
            X_train, X_test, Y_train, Y_test = train_test_split(
                self.__x, self.__y, test_size=0.2, random_state=42
            )      
                  
            f_scores, p_values = self.__model_select(X_train, Y_train)

            # Combine into a DataFrame
            feature_scores = pd.DataFrame({
            'Feature': self.__x.columns,
            'F Score': f_scores,
            'P-value': p_values
            }).sort_values(by='F Score', ascending=False)

            # Select features with p < 0.05
            selected = feature_scores[feature_scores['P-value'] < 0.05]
            return list(selected['Feature'])
      
      def __predicate(self,features):
            '''
                  Args:
                        list of features 
                  return 
                        accuracy of model on selected features  

            '''
            
            # Split data into train and test sets
            X_train, X_test, Y_train, Y_test = train_test_split(
                self.__x, self.__y, test_size=0.2, random_state=42
            )
            
            
            
            
            # Train model and make predictions
            try:

                self.__model.fit(X_train[list(features)], Y_train)
                preds = self.__model.predict(X_test[list(features)])
                accuracy = self.__acc_f(Y_test, preds)
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
            selected_features =  self.__get_selected_features()
            acc               =  self.__predicate(selected_features)
            print((selected_features,acc))
            return (acc,selected_features)
            
                  
            
            


