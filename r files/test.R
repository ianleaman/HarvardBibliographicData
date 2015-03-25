library("RSQLite")
drv <- dbDriver("SQLite")
con <- dbConnect(drv, "C:/Users/ian/Desktop/Text Mining/HarvardBibliographicData/sqltest.db")
year_pub_freq = dbGetQuery(con, "SELECT year_pub AS Year, language AS Language, COUNT(language) AS FREQUENCY FROM records GROUP BY year_pub;")

english = year_pub_freq[year_pub_freq[,"Language"] == "eng",]
english$Language <- "English"

year_pub_sub_freq = dbGetQuery(con, "SELECT year_pub AS YEAR, key_term AS SUBJECT, country_code AS COUNTRY, COUNT(key_term) As Subject_freq  from records GROUP BY key_term ORDER BY key_term DESC;")

SUBJECT_FREQ= dbGetQuery(con, "SELECT key_term AS SUBJECT, COUNT(key_term) AS SUBJECT_FREQ from records GROUP BY GROUP BY year_pub GROUP BY key_term LIMIT 50;")

# Total Number of Pubs per Year as an R List.
yearDict = {}

# CHOOSE COUNTRY IS SQL
year = []
subject = []
frequency = []
