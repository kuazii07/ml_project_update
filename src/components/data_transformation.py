import sys
import os
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    perprocessor_obj_file_path = os.path.join("artifacts","preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
            THIS FUNCTION IS RESPONSIBLE FOR DATA TRANSFORMATION
        '''
        try:
            #create list of numerical features
            numerical_columns = ["writing_score","reading_score"]
            
            #create list of categorical features
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_perparation_course"
                
            ]

            num_pipeline = Pipeline(
                #steps is a list that defines the order of operations applied to your data.
                steps= [
                    #imputer to handle missing values ->replaces null with median value
                    ("imputer",SimpleImputer(strategy="median")),
                    #Standardscaler to standardize the data
                    ("scaler", StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                #steps is a list that defines the order of operations applied to your data.
                steps=[
                    #imputer to hadle missing values with the most common value
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    #replaces categorical features with numerical values
                    ("one_hot_encoding",OneHotEncoder()),
                    #Standardscaler to standardize the data
                    ("scaler",StandardScaler())
                ]
            )

            
            
            logging.info(f"Categorical columns : {categorical_columns}")
            
            logging.info(f"Numerical columns : {numerical_columns}")

            #ColumnTransformer is used to apply different preprocessing steps to different columns of a dataset at the same time.
            preprocessor = ColumnTransformer(transformers=[
                #pipeline_name, pipeline,column_name
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipeline",cat_pipeline,categorical_columns)
            ])

            return preprocessor

        except Exception as e:
            raise CustomException (e,sys)
            
        
    #parameters train_path and test_path comes from data_ingestion.py
    def initiate_data_transformation(self, train_path,test_path):
        try:
            #train path
            train_df=pd.read_csv(train_path)
            #test path
            test_df=pd.read_csv(test_path)

            logging.info("Read train & test data completed")
            logging.info("Obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()

            #target column
            target_column_name = 'math_score'
            
            #numerical columns
            numerical_columns = [
                "writing_score",
                "reading_score"
            ]

            #Remove target column from the dataset and keeps everything else as input features.
            # axis =- 1 means we are dropping a column not a row.
            input_feature_train_df=train_df.drop(columns=[target_column_name], axis=1)
            
            #It selects only the target column from the dataset.
            target_feature_train_df=train_df[target_column_name]

            #Remove target column from the dataset and keeps everything else as input features.
            # axis =- 1 means we are dropping a column not a row.
            input_feature_test_df=test_df.drop(cloumns=[target_column_name],axis=1)
            #It selects only the target column from the dataset.
            target_feature_test_df=test_df[target_column_name]

            logging.info(f"Applying preprocessing object on training dataframe and testing dataframe")

            #fit_transform() => learn patterns from data + immediately apply transformation, applied on test data
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)

            #only transform using learned rules (.transform)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            #np.c_[] (from NumPy) is used to concatenate arrays column-wise. It stacks arrays side by side
            #This line joins (concatenates) two arrays column-wise:
            #basically concatinating input_feature_train_arr and target_feature_train_df 
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(
                #artifacts/preprocessor.pkl
                file_path=self.data_transformation_config.perprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (
                #return train array
                train_arr,
                #return train array
                test_arr,
                #returns artifacts/preprocessor.pkl
                self.data_transformation_config.perprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException (e,sys)
