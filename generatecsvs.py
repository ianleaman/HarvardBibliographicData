'''
Writen By Jason Krone and Ian Leaman
'''


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
import csv

# Leave as an empty string for all regions
region = "Africa"

where_region = ""
if region:
    where_region = "WHERE region=" + "'" + region + "'"
# Generate Normalization Weights (AKA total publications)
totals_query = engine.execute("SELECT COUNT(*), year_pub FROM records {0} GROUP BY year_pub".format(where_region))
# Generate normalization dict
normalizationDict = {}
for entry in totals_query:
    freq = entry[0]
    year = entry[1]
    normalizationDict[year] = freq
    # print(year, freq)

# print(normalizationDict)


def create_row(year, frequency, group):
    normalized_frequency = 0
    # Generate normalized frequency as a percentage
    # If normalized frequency is not in the db sets percentage to 0
    if year in normalizationDict:
        totalPub = normalizationDict[year]
        if totalPub:
            normalized_frequency = (frequency / totalPub) * 100

    return [group, year, frequency, normalized_frequency]

# Generate CSV HERE
f = open("output/output{0}.tsv".format(region), "w")
writer = csv.writer(f, delimiter="\t", lineterminator="\n")
writer.writerow(["group", "year", "frequency", "normalized_frequency"])

file_path = "groupings/groupings{0}.csv".format(region)
with open(file_path, 'r', encoding="utf-8") as csvfile:
    csvreader = csv.reader(csvfile, delimiter="\t")
    for group in csvfile:
        sql_query = "SELECT COUNT(key_term) AS FREQUENCY, year_pub AS YEAR FROM records WHERE (key_term="
        subjects = group.split("\t")
        group_name = subjects[0]
        sql_query += "'"+subjects[1]+"'"
        for subj in subjects[2:]:
            sql_query += " or key_term=" + "'" + str(subj[:-1]) + "'"

        and_region = ""
        if region:
            and_region = "and region='" + region + "'"
        sql_query += ") {0} GROUP BY year_pub ORDER BY year_pub DESC".format(and_region)
        # print(sql_query)
        result = engine.execute(sql_query)
        for i, entry in enumerate(result):
            frequency = entry[0]
            year = entry[1]
            row = create_row(year=year, frequency=frequency, group=group_name)
            # print(row)
            writer.writerow(row)
        try:
            print("[Processed group:", group_name, "]")
        except:
            print("[Error Printing Processed Name]")
f.close()
