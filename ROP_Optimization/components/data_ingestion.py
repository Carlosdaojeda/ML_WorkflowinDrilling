

## configuration of the Data Ingestion Config

import os
import sys
import pandas as pd
import numpy as np
import pymongo
import certifi
from sklearn.model_selection import train_test_split
from ROP_Optimization.Exception.exception import ROPException
from ROP_Optimization.logging.logger import logging
from ROP_Optimization.entity.config_entity import DataIngestionConfig
from ROP_Optimization.entity.artifact_entity import DataIngestionArtifact
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
CA_FILE = certifi.where()

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise ROPException(e, sys)

    def export_collection_as_dataframe(self) -> pd.DataFrame:
        try:
            logging.info(f"Connecting to MongoDB with URL: {MONGO_DB_URL}")

            client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=CA_FILE)
            collection = client[self.data_ingestion_config.database_name][
                self.data_ingestion_config.collection_name
            ]
            df = pd.DataFrame(list(collection.find()))
            
            if "_id" in df.columns:
                df = df.drop(columns=["_id"], axis=1)
            
            df.replace({"na": np.nan}, inplace=True)

            if df.empty:
                raise ROPException("No data found in MongoDB collection.", sys)

            logging.info(f"Number of records fetched from MongoDB: {len(df)}")
            return df

        except Exception as e:
            raise ROPException(e, sys)

    def export_data_into_feature_store(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        try:
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(os.path.dirname(feature_store_path), exist_ok=True)
            dataframe.to_csv(feature_store_path, index=False, header=True)
            logging.info(f"Data exported to feature store at: {feature_store_path}")
            return dataframe

        except Exception as e:
            raise ROPException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            if len(dataframe) < 2:
                raise ROPException("Not enough data to split into train and test.", sys)

            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info(f"Train/Test split done. Train: {len(train_set)}, Test: {len(test_set)}")

            os.makedirs(os.path.dirname(self.data_ingestion_config.training_file_path), exist_ok=True)
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)

            logging.info(f"Train and Test files saved at {self.data_ingestion_config.training_file_path} and {self.data_ingestion_config.testing_file_path}")

        except Exception as e:
            raise ROPException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            df = self.export_collection_as_dataframe()
            df = self.export_data_into_feature_store(df)
            self.split_data_as_train_test(df)

            artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            logging.info("Data ingestion completed successfully.")
            return artifact

        except Exception as e:
            raise ROPException(e, sys)
