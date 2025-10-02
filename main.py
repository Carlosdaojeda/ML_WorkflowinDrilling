from ROP_Optimization.components.data_ingestion import DataIngestion
from ROP_Optimization.Exception.exception import ROPException
from ROP_Optimization.logging.logger import logger
from ROP_Optimization.entity.config_entity import DataIngestionConfig
from ROP_Optimization.entity.config_entity import TrainingPipelineConfig
import sys

if __name__=='__main__':
    try:
       trainingpipelineconfig=TrainingPipelineConfig()
       dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
       data_ingestion=DataIngestion(dataingestionconfig)
       logger.info("Initiate the data ingestion")
       dataingestionartifact=data_ingestion.initiate_data_ingestion()
       print(dataingestionartifact)


    except Exception as e:
           raise ROPException(e,sys)   