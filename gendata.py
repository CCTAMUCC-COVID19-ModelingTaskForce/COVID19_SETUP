# Generate parsers and associated data files for each region
# A region is a category containing counties

months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
ageGroups = ["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80+"]

import json
from os import path
import fileinput
import pandas as pd
from shutil import copyfile 
from optparse import OptionParser
import datetime
import numpy as np

parser = OptionParser()
parser.add_option("-i", "--infile",
	help = "Path to file mapping counties to regions. One column must be 'county' and another must be the region categories.",
	default = "region2county.tsv")
parser.add_option("-p", "--pop_by_age", 
	help = "Path to file mapping population stats to regions. One column must be 'age', another 'total', and one with the regions",
	default = "region2popByAge.tsv")
parser.add_option("-k", "--key",
	help = "Column name of region categories in the mapping file. Default is 'tsa'.",
	default = "tsa")
(options, args) = parser.parse_args()

# Input files
key = options.key
r2cFile = options.infile
r2pFile = options.pop_by_age
pdir = "params/"
parserTemplateFile = "ParserTemplate.py"
if options.key == "tsa":
	parserTemplateFile = "ParserTemplate_TSA.py"
sourcesTemplateFile = "sources.json.template"
defaultParamsFile = pdir + "default_params.tsv"
defaultPopByAgeFile = pdir + "default_popByAge.tsv"
defaultMitigationsFile = pdir + "default_mitigations.tsv"
defaultSeverityFile = pdir + "default_severity.tsv"
# Output files
sourcesOutFile = "out/sources.json.cb"
ageDistributionOutFile = "out/ageDistribution.json.cb"
scenarioOutFile = "out/scenarios.json.cb"
severityOutFile = "out/severityDistributions.json.cb"
# Templates
ageDistributionTemplate = '{"name" : "NAME", "data" : [{ "ageGroup" : "0-9", "population" : P1 }, { "ageGroup" : "10-19", "population" : P2 },  { "ageGroup" : "20-29", "population" : P3 }, { "ageGroup" : "30-39", "population" : P4 }, { "ageGroup" : "40-49", "population" : P5 }, { "ageGroup" : "50-59", "population" : P6 }, { "ageGroup" : "60-69", "population" : P7 }, { "ageGroup" : "70-79", "population" : P8 }, { "ageGroup" : "80+", "population" : P9 } ]}'

# Get list of regions
r2c = pd.read_csv(r2cFile, sep = '\t')
regions = list(set([r.strip() for r in list(r2c["tsa"])]))
numRegions = len(regions)

# Get region popByAge
if r2pFile is not None:
	r2p = pd.read_csv(r2pFile, sep = '\t')

# Open defaults
default_params = pd.read_csv(defaultParamsFile, sep = "\t")
default_popByAge = pd.read_csv(defaultPopByAgeFile, sep = "\t")
default_mitigations = pd.read_csv(defaultMitigationsFile, sep = "\t")
default_severity = pd.read_csv(defaultSeverityFile, sep = "\t")

# Open sources template
f = open(sourcesTemplateFile, "r")
sourcesTemplate = f.read()
f.close()

sources = "{\n"
ageDistribution = '{\n  "all": [\n'
scenarios = {"all" : []}
severities = {"all" : []}

count = 0
for region in regions:
	# Get region's counties
	counties = list(set([c.strip() for c in list(r2c[r2c["tsa"] == region]["county"])]))

	default = True
	# Try to open region-specific files
	if path.exists("{d}/{r}_params.tsv".format(d = pdir, r = region)):
		params = pd.read_csv("{d}/{r}_params.tsv".format(d = pdir, r = region), sep = "\t")
	else:
		params = default_params
	if path.exists("{d}/{r}_popByAge.tsv".format(d = pdir, r = region)):
		popByAge = pd.read_csv("{d}/{r}_popByAge.tsv".format(d = pdir, r = region), sep = "\t")
		default = False
	else:
		popByAge = default_popByAge
	if path.exists("{d}/{r}_mitigations.tsv".format(d = pdir, r = region)):
		mitigations = pd.read_csv("{d}/{r}_mitigations.tsv".format(d = pdir, r = region), sep = "\t")
	else:
		mitigations = default_mitigations
	if path.exists("{d}/{r}_severity.tsv".format(d = pdir, r = region)):
		severity = pd.read_csv("{d}/{r}_severity.tsv".format(d = pdir, r = region), sep = "\t")
	else:
		severity = default_severity

	# In-place correct popByAge if the region2popByAge was provided
	pops = list(popByAge["Total"])
	if r2pFile is not None and default == True:
		pops = list(r2p[r2p[key] == region]["total"])
	else:
		pops = list(popByAge["Total"])

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
	newdata = newdata.replace("##NAME_PLACEHOLDER", "parserName = '{r}'".format(r = region))
	f = open(parserFile, "w")
	f.write(newdata)
	f.close()

	# Sources
	sources = sources.replace("}\n", "},\n")
	template = sourcesTemplate.replace("REGION", region)
	sources += template

	# Age distribution
	ageDistribution += ageDistributionTemplate.replace("NAME", region).replace("P1", str(pops[0])).replace("P2", str(pops[1])).replace("P3", str(pops[2])).replace("P4", str(pops[3])).replace("P5", str(pops[4])).replace("P6", str(pops[5])).replace("P7", str(pops[6])).replace("P8", str(pops[7])).replace("P9", str(pops[8]))
	if count < numRegions - 1:
		ageDistribution += ",\n"

	peakMonthStr = params.loc[params["parameter"] == "Seasonal peak", "meanVal"].item().lower()
	start = params.loc[params["parameter"] == "Simulation start date", "meanVal"].item().split("/")
	startDate = datetime.datetime(int(start[2]), int(start[0]), int(start[1]), 0, 0, 0)
	startDate += datetime.timedelta(days = 1)
	start = "{}-{:02d}-{:02d}".format(startDate.year, startDate.month, startDate.day)
	stop = params.loc[params["parameter"] == "Simulation end date", "meanVal"].item().split("/")
	stopDate = datetime.datetime(int(stop[2]), int(stop[0]), int(stop[1]), 0, 0, 0)
	stopDate += datetime.timedelta(days = 1)
	stop = "{}-{:02d}-{:02d}".format(stopDate.year, stopDate.month, stopDate.day)

	# Scenario
	scenario = {
		"name" : region,
		"data" : {
			"epidemiological" : {
				"hospitalStayDays" : float(params.loc[params["parameter"] == "Days in hospital", "meanVal"].item()),
				"icuStayDays" : float(params.loc[params["parameter"] == "Days in icu", "meanVal"].item()),
				"infectiousPeriodDays" : float(params.loc[params["parameter"] == "Infectious period", "meanVal"].item()),
				"latencyDays" : float(params.loc[params["parameter"] == "Latency", "meanVal"].item()),
				"overflowSeverity" : float(params.loc[params["parameter"] == "Severity of ICU overflow", "meanVal"].item()),
				"peakMonth" : int(months.index(peakMonthStr)) + 1,
				"r0" : {
					"begin" :  float(params.loc[params["parameter"] == "Ro", "lower"].item()),
					"end" : float(params.loc[params["parameter"] == "Ro", "upper"].item()),
				},
				"seasonalForcing" : float(params.loc[params["parameter"] == "Seasonal forcing", "meanVal"].item()),
			},			
			"mitigation" : { "mitigationIntervals" : [] },
			"population" : {
				"ageDistributionName" : region,
				"caseCountsName" : region,
				"hospitalBeds" : int(params.loc[params["parameter"] == "Hospital beds available", "meanVal"].item()),
				"icuBeds" : int(params.loc[params["parameter"] == "ICU beds available", "meanVal"].item()),
				"importsPerDay" : float(params.loc[params["parameter"] == "Imports per day", "meanVal"].item()),
				"initialNumberOfCases" : int(params.loc[params["parameter"] == "Initial number of cases", "meanVal"].item()),
				"populationServed" : int(np.sum(pops)),
			},
			"simulation" : {
				"numberStochasticRuns": int(params.loc[params["parameter"] == "Number of Runs", "meanVal"].item()),
				"simulationTimeRange": {
					"begin" : start,
					"end" : stop,
				}
			}
		}
	}
	
	# Mitigations
	for name, lower, upper, start, stop in zip(mitigations["Intervention"], \
			mitigations["LowerTransmissionReduction"], mitigations["UpperTransmissionReduction"],
			mitigations["DateBegin"], mitigations["DateEnd"]):
		start = start.split("/")
		startDate = datetime.datetime(int(start[2]), int(start[0]), int(start[1]), 0, 0, 0)
		startDate += datetime.timedelta(days = 1)
		start = "{}-{:02d}-{:02d}".format(startDate.year, startDate.month, startDate.day)
		stop = stop.split("/")
		stopDate = datetime.datetime(int(stop[2]), int(stop[0]), int(stop[1]), 0, 0, 0)
		stopDate += datetime.timedelta(days = 1)
		stop = "{}-{:02d}-{:02d}".format(stopDate.year, stopDate.month, stopDate.day)
		
		scenario["data"]["mitigation"]["mitigationIntervals"].append({
			"color" : "#bf5b17",
			"name" : name,
			"transmissionReduction" : {
				"begin" : float(lower),
				"end" : float(upper),
			},
			"timeRange" : {
				"begin" : start,
				"end" : stop,
			},
		})
	scenarios["all"].append(scenario)

	# Severity
	severe = {
		"name" : region,
		"data" : [],
	}
	severe["data"] = [{"ageGroup" : ageclass, "confirmed" : confirmed, "critical" : critical, 
					"fatal" : fatal, "isolated" : isolated, "severe" : severe} \
		for ageclass, confirmed, critical, fatal, isolated, severe in \
		zip(ageGroups, severity["Confirmed"], severity["Critical"], 
		severity["Fatal"], severity["Isolated"], severity["Severe"])]
	severities["all"].append(severe)

	count += 1

# Write files
# Sources
sources += "}"
f = open(sourcesOutFile, "w")
f.write(sources)
f.close()
# Age distribution
ageDistribution += " ]}"
f = open(ageDistributionOutFile, "w")
f.write(ageDistribution)
f.close()
# Scenarios
with open(scenarioOutFile, "w") as f:
	json.dump(scenarios, f, indent = 2)
# Severity
with open(severityOutFile, "w") as f:
	json.dump(severities, f, indent= 2 )
