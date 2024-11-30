"""
Here we will write our data ingestion code from different sources.

"""

from dataclasses import dataclass
import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from data_transformation import DataTransformation

"""
Utilité principale de dataclass : Créer des classes simples qui contiennent des données sans écrire beaucoup de code.
Avantage : Automatiquement, Python ajoute des méthodes comme __init__, __repr__, et __eq__ pour cette classe.
"""

@dataclass
class DataIngestionConfig:
    """
    Définit des chemins par défaut pour sauvegarder les données brutes, d'entraînement, et de test 
    Ces fichiers seront sauvegardés dans le dossier appellé artifact.
    """
    train_data_path: str = os.path.join('artifact', "train.csv")
    test_data_path: str = os.path.join('artifact', "test.csv")
    raw_data_path: str = os.path.join('artifact', "data.csv")

class DataIngestion:
    def __init__(self):
        # Initialise un objet de la classe DataIngestionConfig pour accéder aux chemins configurés
        self.ingestion_config = DataIngestionConfig()
    
    def initiate_data_ingestion(self):

        logging.info("Enterring the Data ingestion method")
        try:
            # Lecture des data
            df = pd.read_csv(r"notebook\data\stud.csv")
            logging.info("Read the Dataset as Dataframe")
            
            # Creer le dossier artifact
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True) # os.path.dirname("artifact/train.csv") -> "artifact" only takes dir name


            # Sauvegarde des données brutes lues (df) dans le fichier artifact/data.csv
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            # Splitting Train and Test
            logging.info('Splitting into train and test initiated')
            train_set, test_set = train_test_split(df, test_size=.2, random_state=0)

            # Sauvegarde des données train et test dans le fichier artifact/train.csv et artifact/test.csv resp
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("The Ingestion of Data is completed")

            # On retourne le path du train et du test.
            return ( 
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)
        

if __name__=="__main__":
    obj = DataIngestion()
    transf = DataTransformation()
    train_data_path, test_data_path = obj.initiate_data_ingestion()
    train_arr, test_arr, preprocessor_obj_file_path = transf.initiate_data_transformation(train_data_path, test_data_path) 
            

