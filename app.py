"""
##############################################################################
#######             PROJECT NAME : Postcodes filter                    #######
##############################################################################

                             Synopsis:
 Main class thats read postcodes.csv, validate invalid records, and then isolate all postcodes within provadided distance and postcode
 and map in html file with highlighted desired radius
"""

### Import necessary libraries
import pandas as pd
import manipulator, validator
import folium


# Main class
class Postcode_dist:
    def __init__(self, distance, postcode):
        ### Create data frame from 'ukpostcodes.csv' file, use 'postcode' column as index 
        dataframe = pd.read_csv('ukpostcodes.csv', index_col='postcode').drop('id', axis=1)
        data, error = validator.validator(dataframe)

        ### output error and validated data to csv files
        error.to_csv('error.csv')
        data.to_csv('validated_postcode.csv')

        ### set variables for latitude and longtitude
        lat = data[data.index == postcode]['latitude']
        lon = data[data.index == postcode]['longitude']
        
        ### create map in html with highlighted required distance
        map = folium.Map(location=[lat,lon],zoom_start=10, tiles='openstreetmap')
        fg = folium.FeatureGroup(name='Postcodes')
        fg.add_child(folium.Circle(location=[lat,lon],radius = distance*1000))
        map.add_child(fg)
        map.save('map.html')
    
        ### get distance for each postcode
        result = manipulator.get_distance(data, postcode)
        ### isolate desired records
        result = result[result['distance'] <= distance ]
        ### output csv file with desired result
        result.to_csv('final_result.csv')
    



 