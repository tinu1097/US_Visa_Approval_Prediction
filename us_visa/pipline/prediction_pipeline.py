import os
import sys

import numpy as np
import pandas as pd
from us_visa.entity.config_entity import USvisaPredictorConfig
from us_visa.entity.s3_estimator import USvisaEstimator
from us_visa.exception import USvisaException
from us_visa.logger import logging
from pandas import DataFrame


class USvisaData:
    def __init__(self,
                 CONTINENT,
                 EDUCATION_OF_EMPLOYEE,
                 HAS_JOB_EXPERIENCE,
                 REQUIRES_JOB_TRAINING,
                 NO_OF_EMPLOYEES,
                 REGION_OF_EMPLOYMENT,
                 PREVAILING_WAGE,
                 UNIT_OF_WAGE,
                 FULL_TIME_POSITION,
                 COMPANY_AGE
                 ):
        """
        USvisa Data constructor
        Input: all features of the trained model for prediction
        """
        try:
            self.CONTINENT = CONTINENT
            self.EDUCATION_OF_EMPLOYEE = EDUCATION_OF_EMPLOYEE
            self.HAS_JOB_EXPERIENCE = HAS_JOB_EXPERIENCE
            self.REQUIRES_JOB_TRAINING = REQUIRES_JOB_TRAINING
            self.NO_OF_EMPLOYEES = NO_OF_EMPLOYEES
            self.REGION_OF_EMPLOYMENT = REGION_OF_EMPLOYMENT
            self.PREVAILING_WAGE = PREVAILING_WAGE
            self.UNIT_OF_WAGE = UNIT_OF_WAGE
            self.FULL_TIME_POSITION = FULL_TIME_POSITION
            self.COMPANY_AGE = COMPANY_AGE

        except Exception as e:
            raise USvisaException(e, sys) from e

    def get_usvisa_input_data_frame(self) -> DataFrame:
        """
        This function returns a DataFrame from USvisaData class input
        """
        try:
            usvisa_input_dict = self.get_usvisa_data_as_dict()
            return DataFrame(usvisa_input_dict)

        except Exception as e:
            raise USvisaException(e, sys) from e

    def get_usvisa_data_as_dict(self):
        """
        This function returns a dictionary from USvisaData class input
        """
        logging.info("Entered get_usvisa_data_as_dict method as USvisaData class")

        try:
            input_data = {
                "CONTINENT": [self.CONTINENT],
                "EDUCATION_OF_EMPLOYEE": [self.EDUCATION_OF_EMPLOYEE],
                "HAS_JOB_EXPERIENCE": [self.HAS_JOB_EXPERIENCE],
                "REQUIRES_JOB_TRAINING": [self.REQUIRES_JOB_TRAINING],
                "NO_OF_EMPLOYEES": [self.NO_OF_EMPLOYEES],
                "REGION_OF_EMPLOYMENT": [self.REGION_OF_EMPLOYMENT],
                "PREVAILING_WAGE": [self.PREVAILING_WAGE],
                "UNIT_OF_WAGE": [self.UNIT_OF_WAGE],
                "FULL_TIME_POSITION": [self.FULL_TIME_POSITION],
                "COMPANY_AGE": [self.COMPANY_AGE],
            }

            logging.info("Created USvisa data dict")
            logging.info("Exited get_usvisa_data_as_dict method as USvisaData class")

            return input_data

        except Exception as e:
            raise USvisaException(e, sys) from e


class USvisaClassifier:
    def __init__(self, prediction_pipeline_config: USvisaPredictorConfig = USvisaPredictorConfig()) -> None:
        """
        :param prediction_pipeline_config: Configuration for prediction
        """
        try:
            self.prediction_pipeline_config = prediction_pipeline_config
        except Exception as e:
            raise USvisaException(e, sys)

    def predict(self, dataframe) -> str:
        """
        This is the method of USvisaClassifier
        Returns: Prediction in string format
        """
        try:
            logging.info("Entered predict method of USvisaClassifier class")
            model = USvisaEstimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_path=self.prediction_pipeline_config.model_file_path,
            )
            result = model.predict(dataframe)

            return result

        except Exception as e:
            raise USvisaException(e, sys)
