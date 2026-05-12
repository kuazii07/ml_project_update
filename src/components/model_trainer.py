import os
import sys

from dataclasses import dataclass
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def initiate_model_trainer(self, train_array,test_array,preprocessor_path):
        try:
            logging.info("Spit training and test input data")
            X_train,y_train,X_test,y_test = (
                #all columns except as cloumns
                X_train[:,:-1],
                #only last column
                y_train[:,-1],
                #all columns except last column
                X_test[:,:-1],
                #only last column
                y_test[:,-1]
            )
            #dict of models to be applied
            models={
                "Random Forest": RandomForestRegressor(),
                "Decision Tree" : DecisionTreeRegressor(),
                "Gradiant Boosting": GradientBoostingRegressor(),
                "Linear Regression" : LinearRegression(),
                "K-Neighbors": KNeighborsRegressor(),
                "XGBClassifier": XGBRegressor(),
                "Catboosting Classifier": CatBoostRegressor(),
                "AdaBoost": AdaBoostRegressor()
            }
            #evaluate_models(X_train,y_train,X_test,y_test, models):
            model_report:dict = evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models)

            #To get the best model score from dict
            best_model_score = max(sorted(model_report.values()))
            #to get the best model name
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            best_model = models[best_model_name]
            
            
            if best_model_score < 0.6:
                raise CustomException ("No best model found")
            logging.info(f"Best found model on both training and test dataset")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
            
            
        except Exception as e:
            raise CustomException (e,sys)