#!/usr/bin/python3
from optparse import OptionParser
import pandas as pd
import json
import datetime

months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

# Options
parser = OptionParser()
parser.add_option("-p", "--params",
    help = "Path to parameters tsv file.",
    default = "coastalBend_params.tsv")
parser.add_option("-a", "--agepop",
    help = "Path to age_population tsv file.",
    default = "coastalBend_popByAge.tsv")
parser.add_option("-m", "--mitigations",
    help = "Path to mitigations tsv file.",
    default = "coastalBend_mitigations.tsv")
parser.add_option("-s", "--severity",
    help = "Path to severity distribution tsv file.",
    default = "coastalBend_severity.tsv")
parser.add_option("-j", "--json",
    help = "Path to output json file.",
    default = None)
(options, args) = parser.parse_args()

# Parameter files
paramsFile = options.params
agepopFile = options.agepop
mitigationsFile = options.mitigations
severityFile = options.severity

# Initialize output dictionary
parameters = {
        "ageDistributionData" : { "data" : [], "name" : None },
        "severityDistributionData" : { "data" : [], "name" : None },
        "scenarioData" : { "data" : {
            "epidemiological" : {
                "hospitalStayDays" : None,
                "icuStayDays" : None,
                "infectiousPeriodDays" : None,
                "latencyDays" : None,
                "overflowSeverity" : None,
                "peakMonth" : None,
                "seasonalForcing" : None,
                "r0" : {
                    "begin" : None,
                    "end" : None,
                },

            },
            "mitigation" : { "mitigationIntervals" : [] },
            "population" : {
                "ageDistributionName" : None,
                "caseCountsName" : None,
                "hospitalBeds" : None,
                "icuBeds" : None,
                "importsPerDay" : None,
                "initialNumberOfCases" : None,
                "populationServed" : None,
            },
            "simulation" : {
                "numberStochasticRuns" : None,
                "simulationTimeRange" : {
                    "begin" : None,
                    "end" : None,
                }
            },

        } },
        "schemaVer" : "2.0.0"
    }

# Populate json from files
paramsDF = pd.read_csv(paramsFile, sep = "\t")
parameters["scenarioData"]["name"] = paramsDF.loc[paramsDF["parameter"] == "Scenario", "meanVal"].item()
parameters["scenarioData"]["data"]["population"]["ageDistributionName"] = paramsDF.loc[paramsDF["parameter"] == "Age distribution", "meanVal"].item()
parameters["scenarioData"]["data"]["population"]["caseCountsName"] = paramsDF.loc[paramsDF["parameter"] == "Confirmed cases", "meanVal"].item()
parameters["scenarioData"]["data"]["population"]["hospitalBeds"] = int(paramsDF.loc[paramsDF["parameter"] == "Hospital beds available", "meanVal"].item())
parameters["scenarioData"]["data"]["population"]["icuBeds"] = int(paramsDF.loc[paramsDF["parameter"] == "ICU beds available", "meanVal"].item())
parameters["scenarioData"]["data"]["population"]["importsPerDay"] = float(paramsDF.loc[paramsDF["parameter"] == "Imports per day", "meanVal"].item())
parameters["scenarioData"]["data"]["population"]["initialNumberOfCases"] = int(paramsDF.loc[paramsDF["parameter"] == "Initial number of cases", "meanVal"].item())
parameters["scenarioData"]["data"]["population"]["populationServed"] = int(paramsDF.loc[paramsDF["parameter"] == "Population size", "meanVal"].item())
parameters["scenarioData"]["data"]["simulation"]["numberStochasticRuns"] = int(paramsDF.loc[paramsDF["parameter"] == "Number of Runs", "meanVal"].item())
start = paramsDF.loc[paramsDF["parameter"] == "Simulation start date", "meanVal"].item().split("/")
startDate = datetime.datetime(int(start[2]), int(start[0]), int(start[1]), 0, 0, 0)
startDate += datetime.timedelta(days = 1)
start = "{}-{:02d}-{:02d}T00:00:00.000Z".format(startDate.year, startDate.month, startDate.day)
stop = paramsDF.loc[paramsDF["parameter"] == "Simulation end date", "meanVal"].item().split("/")
stopDate = datetime.datetime(int(stop[2]), int(stop[0]), int(stop[1]), 0, 0, 0)
stopDate += datetime.timedelta(days = 1)
stop = "{}-{:02d}-{:02d}T00:00:00.000Z".format(stopDate.year, stopDate.month, stopDate.day)
parameters["scenarioData"]["data"]["simulation"]["simulationTimeRange"]["begin"] = start
parameters["scenarioData"]["data"]["simulation"]["simulationTimeRange"]["end"] = stop
parameters["scenarioData"]["data"]["epidemiological"]["hospitalStayDays"] = float(paramsDF.loc[paramsDF["parameter"] == "Days in hospital", "meanVal"].item())
parameters["scenarioData"]["data"]["epidemiological"]["icuStayDays"] = float(paramsDF.loc[paramsDF["parameter"] == "Days in icu", "meanVal"].item())
parameters["scenarioData"]["data"]["epidemiological"]["infectiousPeriodDays"] = float(paramsDF.loc[paramsDF["parameter"] == "Infectious period", "meanVal"].item())
parameters["scenarioData"]["data"]["epidemiological"]["latencyDays"] = float(paramsDF.loc[paramsDF["parameter"] == "Latency", "meanVal"].item())
parameters["scenarioData"]["data"]["epidemiological"]["overflowSeverity"] = float(paramsDF.loc[paramsDF["parameter"] == "Severity of ICU overflow", "meanVal"].item())
peakMonthStr = paramsDF.loc[paramsDF["parameter"] == "Seasonal peak", "meanVal"].item().lower()
parameters["scenarioData"]["data"]["epidemiological"]["peakMonth"] = int(months.index(peakMonthStr)) + 1
parameters["scenarioData"]["data"]["epidemiological"]["seasonalForcing"] = float(paramsDF.loc[paramsDF["parameter"] == "Seasonal forcing", "meanVal"].item())
parameters["scenarioData"]["data"]["epidemiological"]["r0"]["begin"] = float(paramsDF.loc[paramsDF["parameter"] == "Ro", "lower"].item())
parameters["scenarioData"]["data"]["epidemiological"]["r0"]["end"] = float(paramsDF.loc[paramsDF["parameter"] == "Ro", "upper"].item())

agepopDF = pd.read_csv(agepopFile, sep = "\t")
parameters["ageDistributionData"]["data"] = \
        [{"ageGroup" : ageclass, "population" : total} for ageclass, total in zip(agepopDF["AgeClass"], agepopDF["Total"])]
parameters["ageDistributionData"]["name"] = paramsDF.loc[paramsDF["parameter"] == "Age distribution", "meanVal"].item()

severityDF = pd.read_csv(severityFile, sep = "\t")
parameters["severityDistributionData"]["data"] = \
        [{"ageGroup" : ageclass, "confirmed" : confirmed, "critical" : critical, "fatal" : fatal, "isolated" : isolated, "severe" : severe} \
        for ageclass, confirmed, critical, fatal, isolated, severe in \
        zip(severityDF["AgeGroup"], severityDF["Confirmed"], severityDF["Critical"], severityDF["Fatal"], severityDF["Isolated"], severityDF["Severe"])]
parameters["severityDistributionData"]["name"] = paramsDF.loc[paramsDF["parameter"] == "Age distribution", "meanVal"].item()

mitigationsDF = pd.read_csv(mitigationsFile, sep = "\t")
mitigations = []
for name, lower, upper, start, stop in zip(mitigationsDF["Intervention"], \
        mitigationsDF["LowerTransmissionReduction"], mitigationsDF["UpperTransmissionReduction"],
        mitigationsDF["DateBegin"], mitigationsDF["DateEnd"]):

    start = start.split("/")
    startDate = datetime.datetime(int(start[2]), int(start[0]), int(start[1]), 0, 0, 0)
    startDate += datetime.timedelta(days = 1)
    start = "{}-{:02d}-{:02d}T00:00:00.000Z".format(startDate.year, startDate.month, startDate.day)
    stop = stop.split("/")
    stopDate = datetime.datetime(int(stop[2]), int(stop[0]), int(stop[1]), 0, 0, 0)
    stopDate += datetime.timedelta(days = 1)
    stop = "{}-{:02d}-{:02d}T00:00:00.000Z".format(stopDate.year, stopDate.month, stopDate.day)

    mitigations.append({
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

parameters["scenarioData"]["data"]["mitigation"]["mitigationIntervals"] = mitigations

if options.json is None:
    print(json.dumps(parameters, indent = 1))
else:
    with open(options.json, "w") as outfile:
        json.dump(parameters, outfile, indent = 1)
