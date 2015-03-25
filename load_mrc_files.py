'''
Tufts University - Text Mining
Writen By: Ian Leaman

TODO:
    - Add in support for subject_list and geographical_name
'''
from pymarc import MARCReader
import json
import time
import os

from xml_region_to_json import getCountryDict

# ###############################################################
from sqlalchemy.orm import sessionmaker

from models import Base, Records
from sqlalchemy import create_engine

engine = create_engine('sqlite:///sqltest.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# ###############################################################


class Maxim(object):
    """Class to create csv files from dictionaries"""
    def __init__(self):
        # year_lang_xx_freq = {}
        self.numPushed = 0

    def push(self, dictionary):
        '''
        Ingests a json object and tallies frequencies
        '''
        pass

    def export_csv(self):
        '''
        Exports all dictionaries to csvs
        '''
        pass

    def push_sql(self, dictionary):
        '''
        Exports to alchemy
        '''
        new_record = Records()
        if "year_pub" in dictionary:
            new_record.year_pub = dictionary["year_pub"]

        if "country_code" in dictionary:
            new_record.country_code = dictionary["country_code"]

        if "language" in dictionary:
            new_record.language = dictionary["language"]

        if "key_term" in dictionary:
            new_record.key_term = dictionary["key_term"]

        if "region" in dictionary:
            new_record.region = dictionary["region"]

        session.add(new_record)
        if (self.numPushed % 500) == 0:
            session.commit()
        self.numPushed += 1


def scrub_field(field):
    '''
    Attempts to remove iregularities in fields
    Todo:
        - Specilize scrubers for different field types
    '''
    field = field.strip()
    if field.endswith((".", ",", ";")):
        field = field[:-1]

    feild = field.lower()
    # field = field
    return field


def process_country_code(code):
    '''
    Padds the country codes
    '''
    if not code:
        return ""
        print(code)
    if code.endswith(" "):
        code = code[:-1]

    return code


def read_mrc_file(fileName, authority_list=None):
    new_maxim = Maxim()
    # recordList = []
    with open(fileName, 'rb') as fh:
        reader = MARCReader(fh)
        numSkips = 0
        i = 0
        totalRegionsSkipped = 0
        while True:
            try:
                record = next(reader)
                i += 1
                recordDict = {}
                # Parse 008 fields
                field008 = record.get_fields('008')
                if not field008:
                    numSkips += 1
                    continue

                field008 = field008[0].value()
                country_code = process_country_code(field008[15:18])
                recordDict["year_pub"] = scrub_field(field008[7:11])
                recordDict["country_code"] = country_code
                recordDict["language"] = scrub_field(field008[35:38])

                # Get Corporate Info
                subject_list = []
                geographical_name = None
                key_term = None
                for f in record.get_fields('610'):
                    # Get field x or "general subdivision"
                    if 'x' in f:
                        subject_list.append(scrub_field(f['x'].encode('utf-8').decode()))

                # Get Personal Info
                for f in record.get_fields('600'):
                    if 'x' in f:
                        subject_list.append(scrub_field(f['x'].encode('utf-8').decode()))

                for f in record.get_fields('650'):
                    if 'x' in f:
                        subject_list.append(scrub_field(f['x'].encode('utf-8').decode()))
                    if 'a' in f:
                        key_term = scrub_field(f['a'].encode('utf-8').decode())

                for f in record.get_fields('651'):
                    if 'x' in f:
                        subject_list.append(scrub_field(f['x'].encode('utf-8').decode()))
                    if 'a' in f:
                        geographical_name = scrub_field(f['a'].encode('utf-8').decode())

                recordDict["subject_list"] = subject_list
                if geographical_name:
                    recordDict["geographical_name"] = geographical_name
                if key_term:
                    recordDict["key_term"] = key_term

                # Insert Region Into Record Dictionary
                if authority_list:
                    if country_code in authority_list:
                        recordDict["region"] = authority_list[country_code]["region"]
                    else:
                        totalRegionsSkipped += 1
                # print(json.dumps(recordDict, sort_keys=True,
                #       indent=4, separators=(',', ': ')))

                # recordList.append(recordDict)
                new_maxim.push_sql(recordDict)

                if i % 50000 == 0:
                    print("[Scanned {0:,d} docs]".format(i))
                    continue

            except UnicodeDecodeError:
                numSkips += 1
            except StopIteration:
                break

        print("Final Docs:", i, "   Skipped:", numSkips, "docs.")
        print("Docs without regions:", totalRegionsSkipped)


def main():
    print("Loading Auth List")
    authList = getCountryDict()
    print("Auth List Loaded")
    startingDir = os.getcwd()
    os.chdir("../data")
    for f_name in [f for f in os.listdir() if f.endswith(".mrc")]:
        start = time.time()
        read_mrc_file(f_name, authority_list=authList)
        print("Completed load in", (time.time() - start) / 60, "minutes.")

    os.chdir(startingDir)

    # totalSkipped = 0
    # total = 0
    # for key, val in authList.items():
    #     try:
    #         print(key, val)
    #         total += 1
    #     except:
    #         totalSkipped += 1
    # print(totalSkipped)
    # print(total)


if __name__ == '__main__':
    main()
