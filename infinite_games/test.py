import re
import requests
from datetime import datetime, timedelta

title = 'Will the amount of peaceful protests in Sweden be above 33 for the duration 2024-08-17 to 2024-08-23?'
description = 'Will the amount of peaceful protests in Sweden be above 4 for the duration 2024-08-16 to 2024-08-18?This event resolves to `YES` if there are at least 5 peaceful protests, for the country of Sweden between the following dates, from 2024-08-16  00:00:00 to 2024-08-18  23:59:59 in Europe/Stockholm timezone. A peaceful protest is when demonstrators gather for a protest and do not engage in violence or other forms of rioting activity, such as property destruction, and are not met with any sort of force or intervention. We use ACLED (https://acleddata.com/) as the source of ground truth'
email = '70DCTT21148@utteduvn.onmicrosoft.com'
key = 'hX1G8tWQqA8WNG!1-iJN'
url = 'https://api.acleddata.com/acled/read'
delta_days = 7
countries = {
    'Germany': 'DEU',
    'United Kingdom': 'GBR',
    'France': 'FRA',
    'Italy': 'IT',
    'Spain': 'ESP',
    'Poland': 'POL',
    'Romania': 'ROU',
    'Netherlands': 'NER',
    'Belgium': 'BEL',
    'Ireland': 'IRL',
    'Sweden': 'SWE',
    'Czech Republic': 'CZE',
    'Greece': 'GRC',
    'Portugal': 'POR',
    'Hungary': 'HUN',
    'Austria': 'AUT',
    'Serbia': 'SRB',
    'Bulgaria': 'BUL',
    'Denmark': 'DEN',
    'United States': 'US'
}
pattern_equals = 'least ([0-9]+)'
pattern_start = 'from (([0-9]{4})-(0[1-9]|1[0,1,2])-([0-9]{2}))'
pattern_end = 'to (([0-9]{4})-(0[1-9]|1[0,1,2])-([0-9]{2}))'
PATTERN_COUNTRY = 'the country of ([a-zA-Z]+) between'
if re.search(PATTERN_COUNTRY, description) is not None and re.search(pattern_equals, description) is not None and re.search(pattern_start, description) is not None and re.search(pattern_end, description) is not None:
    equals = re.search(pattern_equals, description).group(1)
    start = re.search(pattern_start, description).group(1)
    end = re.search(pattern_end, description).group(1)
    country = re.search(PATTERN_COUNTRY, description).group(1)

    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = (datetime.strptime(end, '%Y-%m-%d') + timedelta(1))
    current_date = datetime.now()
    start_diff = (current_date - start_date).days
    end_diff = (end_date - current_date).days
    alpha = 1
    if start_diff > 7:
        start_date = current_date - timedelta(days=delta_days)
        alpha = 0.8

    if end_diff > 0:
        end_date = current_date
        alpha = 0.8

    params = {
        'key': key,
        'email': email,
        'event_date': start_date.strftime("%Y-%m-%d") + '|' + end_date.strftime("%Y-%m-%d"),
        'event_date_where': 'BETWEEN',
        'sub_event_type': 'Peaceful',
        'event_id_cnty': countries[country]
    }
    print(params)
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        count = data['count']
        prop = count / int(equals)
        print(f'count:{count} and prop:{prop}')
        if prop >= alpha:
             print(1)
        else:
             print(0)

    print(response.json())
