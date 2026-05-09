import os
import sys
import pandas as pd
from src.logger import logging
from src.exception import CustomException

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

class DataIngestionConfig:
    # This creates a file path for train.csv, test.csv and data.csv inside the artifacts folder.
    train_data_path=os.path.join("artifacts","train.csv")
    test_data_path=os.path.join('artifacts',"test.csv")
    raw_data_path=os.path.join("artifacts","data.csv")

@dataclass
class DataIngestion:
    #The __init__() method is a constructor.
    #It runs automatically whenever an object of the class is created.
    def __init__(self):
        #This creates an object of the DataIngestionConfig class and stores it inside the current DataIngestion object.
        #So now the DataIngestion class can access all file paths from DataIngestionConfig.
        self.ingestion_config = DataIngestionConfig()

    
    def initiate_data_ingestion(self):
        logging.info("Enter the data ingestion method or component")

        try:
            #read the data.csv.
            #change this line out if you want to read the data from other sourses ex: database, api, etc
            df=pd.read_csv('notebook/data/stud.csv')
            #loggs it
            logging.info('Read the dataset as dataframe')
            #This line creates the folder (directory) needed to store the file path.
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok = True)
            #saves the dataframe as a csv, the path is assigned via: self.ingestion_config.raw_data_path and remove index that was added pandas dataframe
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            #loggs it
            logging.info("Train test split initiated")
            train_set,test_set = train_test_split(df, test_size=0.2,random_state=42)
            
            #saves the dataframe as a csv, the path is assigned via: self.ingestion_config.raw_data_path and remove index that was added pandas dataframe
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            #saves the dataframe as a csv, the path is assigned via: self.ingestion_config.raw_data_path and remove index that was added pandas dataframe
            test_set.to_csv(self.ingestion_config.test_data_path, index=False,header=True)

            logging.info("Ingestion of data is completed")

            return (
                #data_transformation.py will grab the return values and the datapoints and start the process
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException (e,sys)

if __name__=="__main__":
    obj=DataIngestion()
    obj.initiate_data_ingestion()


        


        