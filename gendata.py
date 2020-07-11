# Generate parsers and associated data files for each region
# A region is a category containing counties

from os import path
import fileinput
import pandas as pd
from shutil import copyfile 

# Input files
r2cFile = "region2county.tsv"
parserTemplateFile = "ParserTemplate.py"
sourcesTemplateFile = "sources.json.template"
defaultParamsFile = "default_params.tsv"
defaultPopByAgeFile = "default_popByAge.tsv"
# Output files
sourcesOutFile = "out/sources.json.cb"
countrycodesOutFile = "out/country_codes.csv.cb"
populationDataOutFile = "out/populationData.tsv.cb"
ageDistributionOutFile = "out/ageDistribution.json.cb"
# Templates
countrycodesTemplate = '{},TX,TX,"","",Americas,Northern America,"","","",""\n'
populationDataTemplate = "{}\t{}\t{}\t357\t30\tNone\tNone\tNone\n"
ageDistributionTemplate = '{"name" : "NAME", "data" : [{ "ageGroup" : "0-9", "population" : P1 }, { "ageGroup" : "10-19", "population" : P2 },  { "ageGroup" : "20-29", "population" : P3 }, { "ageGroup" : "30-39", "population" : P4 }, { "ageGroup" : "40-49", "population" : P5 }, { "ageGroup" : "50-59", "population" : P6 }, { "ageGroup" : "60-69", "population" : P7 }, { "ageGroup" : "70-79", "population" : P8 }, { "ageGroup" : "80+", "population" : P9 } ]}'

# Get list of regions
r2c = pd.read_csv(r2cFile, sep = '\t', names = ["region", "county"])
regions = list(set([r.strip() for r in list(r2c["region"])]))
numRegions = len(regions)

# Open defaults
default_popByAge = pd.read_csv(defaultPopByAgeFile, sep = "\t")

# Open sources template
f = open(sourcesTemplateFile, "r")
sourcesTemplate = f.read()
f.close()

sources = "},\n"
countrycodes = ""
populationData = ""
ageDistribution = ""


count = 0
for region in regions:
	print(region)
	# Get region's counties
	counties = list(set([c.strip() for c in list(r2c[r2c["region"] == region]["county"])]))

	# Try to open region-specific files
	if path.exists("{r}_popByAge.tsv".format(r = region)):
		popByAge = pd.read_csv("{r}_popByAge.tsv".format(r = region))
	else:
		popByAge = default_popByAge

	# Parser
	fmtCounties = "counties = ["
	for county in counties:
		fmtCounties += "'{c}', ".format(c = county)
	fmtCounties += "]"

	parserFile = "out/" + region + ".py"
	copyfile(parserTemplateFile, parserFile)
	f = open(parserFile, "r")
	filedata = f.read()
	f.close()
	newdata = filedata.replace("##COUNTIES_PLACEHOLDER", fmtCounties)
	newdata = newdata.replace("##NAME_PLACEHOLDER", "parserName = {r}".format(r = region))
	f = open(parserFile, "w")
	f.write(newdata)
	f.close()

	# Sources
	sources = sources.replace("}\n", "},\n")
	template = sourcesTemplate.replace("REGION", region)
	sources += template

	# Country codes
	countrycodes += countrycodesTemplate.format(region)

	# Population data
	populationData += populationDataTemplate.format(region, sum(list(default_popByAge["Total"])) ,region)

	ageDistribution += ageDistributionTemplate.replace("NAME", region).replace("P1", str(popByAge["Total"][0])).replace("P2", str(popByAge["Total"][1])).replace("P3", str(popByAge["Total"][2])).replace("P4", str(popByAge["Total"][3])).replace("P5", str(popByAge["Total"][4])).replace("P6", str(popByAge["Total"][5])).replace("P7", str(popByAge["Total"][6])).replace("P8", str(popByAge["Total"][7])).replace("P9", str(popByAge["Total"][8]))
	
	if count < numRegions - 1:
		ageDistribution += ",\n"

	count += 1

print(ageDistribution)

# Write files
# Sources
sources += "}"
f = open(sourcesOutFile, "w")
f.write(sources)
f.close()
# Countrycodes
f = open(countrycodesOutFile, "w")
f.write(countrycodes)
f.close()
# Population data
f = open(populationDataOutFile, "w")
f.write(populationData)
f.close()
# Age distribution
f = open(ageDistributionOutFile, "w")
f.write(ageDistribution)
f.close()

