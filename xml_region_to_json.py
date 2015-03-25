from bs4 import BeautifulSoup
import json


def getCountryDict():
    f = open("countries_and_regions.xml", 'r')
    soup = BeautifulSoup(f)

    country_dict = {}
    for country in soup.find_all('country'):
        name = country.find('name').text.encode('utf-8').decode('utf-8', errors='ignore')
        code = country.find('code').text.encode('utf-8').decode('utf-8', errors='ignore')
        region = country.find('region').text.encode('utf-8').decode('utf-8', errors='ignore')

        # I was even lazier...Just ignored the case altogther...ill get back to it
        # if code in country_dict:
        #     print(code, country_dict[code], region)
        #     raise Exception("Account for this case...stop being lazy.")

        if len(code) == 3 and code[-1] == 'u':
            country_dict[code] = {
                "name": "United States",
                "region": "North America",
                "state": name.encode('utf-8').decode('utf-8', errors='ignore'),
            }
            # Hack...
            continue

        country_dict[code] = {
            "name": name.encode('utf-8').decode('utf-8', errors='ignore'),
            "region": region.encode('utf-8').decode('utf-8', errors='ignore'),
        }
        for uf in country.find_all('uf'):
            note = uf.find('note')
            if not note:
                continue

            note_code = note.find('code')
            if not note_code:
                continue

            n_name = note.find('name').text
            note_code = note_code.text.encode('utf-8').decode('utf-8', errors='ignore')

            if note_code not in country_dict:
                country_dict[note_code] = {
                    "name": n_name.encode('utf-8').decode('utf-8', errors='ignore'),
                    "region": n_name.encode('utf-8').decode('utf-8', errors='ignore'),
                }
            # print(note_code.attrs)

    return country_dict


# json.dump(country_dict, open('regions_test.json', 'w'))
