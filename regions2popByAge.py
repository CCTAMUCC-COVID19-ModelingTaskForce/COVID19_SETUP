import numpy as np
import pandas as pd
from optparse import OptionParser

cutoffs = [0, 10, 20, 30, 40, 50, 60, 70, 1000]
popCats = ["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80+"]

parser = OptionParser()
parser.add_option("-r", "--region2county",
	help = "Path to file mapping counties to regions. One column must be 'county' and another must be the region categories.",
	default = "region2county.tsv")
parser.add_option("-d", "--demographics", 
	help = "Path to Texas demographics file",
	default = "regions/Texas_Demographics.csv")
parser.add_option("-k", "--key",
	help = "Column name of region categories in the mapping file. Default is 'tsa'.",
	default = "tsa")
(options, args) = parser.parse_args()

# Outfile
outFile = "region2popByAge.tsv"

# Regions to counties
r2cFile = options.region2county
demosFile = options.demographics
key = options.key
r2c = pd.read_csv(r2cFile, sep = "\t")
demos = pd.read_csv(demosFile)

# Clean demographics table
demos = demos[demos["Age"] != "All Ages"]
county = demos["County"]
age = demos["Age"]
total = demos["Total"]

county = [c.lower().replace("state of ", "").replace(" county", "").replace(" ", "_") for c in county]
age = np.array([int(a.replace(" ", "").replace("<", "").replace("Years", "").replace("+", "").replace("Year", "")) for a in age])

cats = np.zeros(len(age))
for i in range(len(cats)):
	for j in range(1, len(cutoffs)):
		if age[i] < cutoffs[j] and age[i] >= cutoffs[j - 1]:
			cats[i] = j - 1
		if age[i] >= 80:
			cats[i] = 8

demos = pd.DataFrame({"county" : county, "age_group" : cats, "total" : total})
demos["age_group"] = demos["age_group"].apply(np.int)

grp = demos.groupby(["county", "age_group"])["total"].sum().reset_index()
grp["age"] = [popCats[i] for i in grp["age_group"]]

m = pd.merge(grp, r2c, on = ["county", "county"])
mm = m.groupby([key, "age"])["total"].sum().reset_index()

print(mm)
mm.to_csv(outFile, sep = "\t", index = False)
