import re
import requests
from datetime import datetime, timedelta
import json

email = "70DCTT21148@utteduvn.onmicrosoft.com"
key = "hX1G8tWQqA8WNG!1-iJN"
url = "https://api.acleddata.com/acled/read"
delta_days = 7

countries = {
    "Germany": "DEU",
    "United Kingdom": "GBR",
    "France": "FRA",
    "Italy": "IT",
    "Spain": "ESP",
    "Poland": "POL",
    "Romania": "ROU",
    "Netherlands": "NER",
    "Belgium": "BEL",
    "Ireland": "IRL",
    "Sweden": "SWE",
    "Czech Republic": "CZE",
    "Greece": "GRC",
    "Portugal": "POR",
    "Hungary": "HUN",
    "Austria": "AUT",
    "Serbia": "SRB",
    "Bulgaria": "BUL",
    "Denmark": "DEN",
    "United States": "US",
    "China": "CHN",
    "Japan": "JPN",
    "South Korea": "KOR",
    "Taiwan": "TWN",
    "Vietnam": "VNM",
    "Thailand": "THA",
    "Malaysia": "MYS",
    "Philippines": "PHL",
    "Indonesia": "IDN",
    "Myanmar": "MMR",
    "Brunei": "BRN",
    "Laos": "LAO",
    "Cambodia": "KHM",
    "Singapore": "SGP",
    "Hong Kong": "HKG",
    "Macau": "MAC",
    "Taipei": "TPE",
    "Macao": "MAC",
    "Nigeria": "NGR",
    "Kenya": "KEN",
    "Uganda": "UGA",
    "Rwanda": "RWA",
    "Burundi": "BDI",
    "Tanzania": "TZA",
    "Ethiopia": "ETH",
    "Somalia": "SOM",
    "Zambia": "ZMB",
    "Zimbabwe": "ZWE",
    "Afghanistan": "AFG",
    "Bahrain": "BHR",
    "Bangladesh": "BGD",
    "Bhutan": "BTN",
    "India": "IND",
    "Maldives": "MDV",
    "Nepal": "NPL",
    "Pakistan": "PAK",
    "Sri Lanka": "LKA",
    "Malawi": "MWI",
    "Mozambique": "MOZ",
    "Kyrgyzstan": "KGZ",
    "Lebanon": "LBN",
    "Jordan": "JOR",
    "Sudan": "SDN",
    "Syria": "SYR",
    "Yemen": "YEM",
    "Azerbaijan": "AZE",
    "Georgia": "GEO",
    "Armenia": "ARM",
    "Aland Islands": "ALA",
    "Eritrea": "ERI",
    "Libya": "LBY",
    "Palestine": "PSE",
    "Qatar": "QAT",
    "Slovakia": "SVK",
    "Tunisia": "TUN",
    "Ukraine": "UKR",
    "Ecuador": "ECU",
    "Paraguay": "PRY",
    "Colombia": "COL",
    "Chile": "CHL",
    "Costa Rica": "CRI",
    "Dominican Republic": "DOM",
    "El Salvador": "SLV",
    "Guatemala": "GTM",
    "Honduras": "HND",
    "Nicaragua": "NIC",
    "Panama": "PAN",
    "Peru": "PER",
    "Puerto Rico": "PRI",
    "Trinidad and Tobago": "TTO",
    "Uruguay": "URY",
    "Venezuela": "VEN",
    "Guyana": "GUY",
    "Suriname": "SUR",
    "French Polynesia": "PYF",
    "French Guiana": "GUF",
    "New Caledonia": "NCL",
    "Russia": "RUS",
    "United Arab Emirates": "ARE",
    "Saudi Arabia": "SAU",
    "Uzbekistan": "UZB",
    "Kazakhstan": "KAZ",
    "Tajikistan": "TJK",
    "Korean": "KOR",
    "Norway": "NOR",
    "Northern Cyprus": "CYP",
    "Slovenia": "SVN",
    "Croatia": "HRV",
    "Bosnia and Herzegovina": "BIH",
    "Macedonia": "MKD",
    "Serbia and Montenegro": "SCG",
    "Northern Ireland": "NIR",
    "Iceland": "ISL",
    "Scotland": "SCT",
    "Wales": "WAL",
    "North Korea": "PRK",
    "china": "CHN",
    "Monaco": "MCO",
    "Mogolia": "MNG",
    "Montenegro": "MNE",
    "Canada": "CAN",
    "Brazil": "BRA",
    "Iran": "IRN",
    "Australia": "AUS",
    "New Zealand": "NZL",
    "England": "GBR",
    "Switzerland": "CHE",
    "Luxembourg": "LUX",
    "Lithuania": "LTU",
    "Latvia": "LVA",
    "Argentina": "ARG",
    "Cuba": "CUB",
    "Dominica": "DMA",
    "Haiti": "HTI",
    "Jamaica": "JAM",
    "Grenada": "GRD",
    "Angola": "AGO",
    "Cameroon": "CMR",
    "Congo": "COG",
    "Cote d'Ivoire": "CIV",
    "Gambia": "GMB",
    "Guinea": "GIN",
    "Mali": "MLI",
    "Niger": "NER",
    "Senegal": "SEN",
    "Togo": "TGO",
    "Egypt": "EGY",
    "Morocco": "MAR",
    "Algeria": "DZA",
    "Tukey": "TKY",
    "Seychelles": "SYC",
    "Chad": "TCD",
    "Sudan, South": "SSD",
    "Sudan, North": "SDN",
    "Iraq": "IRQ",
    "Kuwait": "KWT",
    "Timor-Leste": "TLS",
}
pattern_equals = 'at least ([0-9]+)'
pattern_start = 'from (([0-9]{4})-(0[1-9]|1[0,1,2])-([0-9]{2}))'
pattern_end = 'to (([0-9]{4})-(0[1-9]|1[0,1,2])-([0-9]{2}))'
PATTERN_COUNTRY = 'the country of ([a-zA-Z]+) between'

def get_prop_by_description(description):
    print("Input description " + description)
    try:
        if (
            re.search(PATTERN_COUNTRY, description) is not None
            and re.search(pattern_equals, description) is not None
            and re.search(pattern_start, description) is not None
            and re.search(pattern_end, description) is not None
        ):
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
            print("Params" + json.dumps(params))

            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data["count"] is not None:
                    print(
                        "Amount events" + str(data["count"]) + " compare to" + str(equals)
                    )
                    count = data["count"]
                    prop = count / int(equals)
                    if prop >= alpha:
                        return 1
                    else:
                        return 0

        return 0

    except Exception as e:
        print(e)
        return 0
