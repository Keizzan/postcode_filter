"""
##############################################################################
#######             PROJECT NAME : Postcodes filter                    #######
##############################################################################

                             Synopsis:
Script reads dataframe, creates new column with distance in km from starting point 
"""


### imports
import pandas as pd
from geopy.distance import great_circle

### Create new column 'distance' which is calculated distance in km for each postcode to chosen postcode
def get_distance(dataframe, postcode):
    """
    Parameters:
    -----------
        dataframe { pandas dataframe object }: dataframe
        postcode { str }: starting point

    Returns:
    --------
        dataframe 
    """
    df = dataframe
    df['distance'] = df.apply( lambda x:
    great_circle((df['latitude'][postcode],df['longitude'][postcode]), (x['latitude'], x['longitude'])).miles, axis=1)

    # returns modified dataframe
    return df