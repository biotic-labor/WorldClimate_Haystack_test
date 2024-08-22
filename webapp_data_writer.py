import shutil
import json
def write(location, json_data, query_type):
    hyphenated_city = location['city_name'].replace(' ', '-')
    with open('../../Climate Platform/React/ClimatePlatform/data/'+hyphenated_city+'/genai_analysis_'+query_type+'.json', 'w') as file:
        json.dump(json_data, file)
        print('Data copied to web app')
    return True