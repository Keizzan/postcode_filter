"""
##############################################################################
#######             PROJECT NAME : Postcodes filter                    #######
##############################################################################

                             Synopsis:
 Script reads dataframe object, validates and output validated and errors dataframes 
"""

import pandas as pd
import numpy as np
from pandas_schema import Column, Schema
from pandas_schema.validation import CustomElementValidation, InRangeValidation

def validator(dataframe):
    """
    Parameters
    -----------
    dataframe {pandas dataframe object } : designated dataframe for validation
    
    Returns
    -----------
    dataframe, error:
    pandas dataframe objects
    """    

    ### Custom function for validation float
    def float_check(num):
        """
        Parameters
        -----------
        num : any
        
        Returns
        -----------
        Boolean
        """
        try:
            float(num)
        except ValueError:
            return False
        return True
    
    ### Custom validators for pandas_schema's Schema
    ### Decimal number
    float_validation = [CustomElementValidation(lambda i: float_check(i),'is not decimal number')]
    ### Empty data point
    null_validation = [CustomElementValidation(lambda a: a is not np.nan, 'cannot be empty')]

    ### Schema object used for validation
    schema = Schema([
        ### Validate latitude column
        Column('latitude', [InRangeValidation(-90,90)]+null_validation+float_validation),
        ### Validate longitude column
        Column('longitude', [InRangeValidation(-180,180)]+null_validation+float_validation)
    ])

    ### Validate and find errors in dataframe based on prepared Schema
    errors = schema.validate(dataframe)
    errors_index_rows = [e.row for e in errors]

    ### Isolate valid data and create new dataframes
    data_cleaned = dataframe.drop(index=errors_index_rows)
    error_dataframe = pd.DataFrame({'Errors':errors})

    ### return two dataframes, validated and invalid records
    return data_cleaned, error_dataframe

    