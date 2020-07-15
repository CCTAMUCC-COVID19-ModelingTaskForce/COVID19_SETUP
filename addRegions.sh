# Script adds data for Coastal Bend scenario
# Run from covid19_scenarios/coastalbend

option=$1

# Backup repo (for later restore)
if [ $option == "--backup" ]
then
	mkdir backup
	# Data sources
	cp ../data/sources.json backup/sources.json.orig
	cp ../data/country_codes.csv backup/country_codes.csv.orig
	cp ../data/populationData.tsv backup/populationData.tsv.orig
	cp ../data/hospital-data/hospital_capacity.csv backup/hospital_capacity.csv.orig
	cp ../data/hospital-data/ICU_capacity.tsv backup/ICU_capacity.tsv.orig
	cp ../data/initialCondition.tsv backup/initialCondition.tsv
	# Data assets
	cp ../src/assets/data/caseCounts.json backup/caseCounts.json.orig
	cp ../src/assets/data/ageDistribution.json backup/ageDistribution.json.orig
	cp ../src/assets/data/severityDistributions.json backup/severityDistributions.json.orig
	cp ../src/assets/data/scenarios.json backup/scenarios.json.orig
	# Remove other countries
	mv ../data/case-counts/ backup/case-counts
	mkdir ../data/case-counts
	mv ../data/parsers/ backup/parsers
	mkdir ../data/parsers/
	cp backup/parsers/utils.py backup/parsers/__init__.py ../data/parsers/
	# Files that will be patched with "--patch" option
	cp ../src/components/Main/validation/schema.ts backup/src-components-Main-validation-schema.ts
	cp ../schemas/ScenarioDatumSimulation.yml backup/schemas-ScenarioDatumSimulation.yml
	cp ../src/components/Form/FormSpinBox.tsx backup/src-components-Form-FormSpinBox.tsx
	cp ../src/components/Main/validation/schema.ts backup/src-components-Main-validation-schema.ts
	cp ../schemas/PercentageRange.yml backup/schemas-PercentageRange.yml
	cp ../src/constants.ts backup/src-constants.ts
fi

# Clean repo (remove coastal bend scenario)
if [ $option == "--restore" ]
then
	# Data sources
	rm ../data/parsers/CoastalBend.py
	cp backup/sources.json.orig ../data/sources.json
	cp country_codes.csv.orig ../data/country_codes.csv
	cp populationData.tsv.orig ../data/populationData.tsv 
	cp hospital_capacity.csv.orig ../data/hospital-data/hospital_capacity.csv
	cp ICU_capacity.tsv.orig ../data/hospital-data/ICU_capacity.tsv
	cp backup/initialCondition.tsv ../data/initialCondition.tsv
	# Data assets
	cp caseCounts.json.orig ../src/assets/data/caseCounts.json
	cp ageDistribution.json.orig ../src/assets/data/ageDistribution.json
	cp severityDistributions.json.orig ../src/assets/data/severityDistributions.json
	cp scenarios.json.orig  ../src/assets/data/scenarios.json
	# Restore other countries
	rm -rf ../data/case-counts/
	mv backup/case-counts/ ../data/case-counts/
	rm -rf ../data/parsers/
	mv backup/parsers/ ../data/parsers/
	# Files that will be patched with "--patch" option
	cp backup/src-components-Main-validation-schema.ts ../src/components/Main/validation/schema.ts 
	cp backup/schemas-ScenarioDatumSimulation.yml ../schemas/ScenarioDatumSimulation.yml
	cp backup/src-components-Form-FormSpinBox.tsx ../src/components/Form/FormSpinBox.tsx 
	cp backup/src-components-Main-validation-schema.ts ../src/components/Main/validation/schema.ts 
	cp backup/schemas-PercentageRange.yml ../schemas/PercentageRange.yml 
	cp backup/src-constants.ts  ../src/constants.ts 
fi

if [ $option == "--add" ]
then
	mkdir out
	# Generate region data
	python3 gendata.py

	cp out/*.py ../data/parsers/ 
	cp out/sources.json.cb ../data/sources.json
	cp out/ageDistribution.json.cb ../src/assets/data/ageDistribution.json
	cp out/scenarios.json.cb ../src/assets/data/scenarios.json
	cp out/severityDistributions.json.cb ../src/assets/data/severityDistributions.json

	cd ../data
	python3 generate_data.py --fetch
	python3 generate_data.py \
		--output-cases ../src/assets/data/caseCounts.json
fi

if [ $option == "--update" ]
then
	# Update the contents of CoastalBend .cb files
	mkdir out

	# Pull data from web
	# Cases
	wget --no-check-certificate \
	       	https://dshs.texas.gov/coronavirus/TexasCOVID19DailyCountyCaseCountData.xlsx -O out/texas_cases.xlsx
	ssconvert out/texas_cases.xlsx out/texas_cases.temp.csv
	sed -i 1,2d out/texas_cases.temp.csv
	sed -i 's/County Name/Name/' out/texas_cases.temp.csv
	perl -pe 'chomp if /Cases/' out/texas_cases.temp.csv | \
	       perl -pe 'chomp if /Cases/' | \
	      sed -e 's/Anderson/\nAnderson/'  > out/texas_cases.csv
	sed -i 's/"//g' out/texas_cases.csv
	sed -i '1,/,,,,,,,,,/!d' out/texas_cases.csv
	sed -i '$ d' out/texas_cases.csv
	sed -i '$ d' out/texas_cases.csv
	sed -i -e 's/_x000D_//g' -e 's/ //g' out/texas_cases.csv 
	sed -i 's/Andrews/\nAndrews/' out/texas_cases.csv
	sed -i -e "s/\r//g" out/texas_cases.csv

	# Fatalities
	wget --no-check-certificate \
		https://dshs.texas.gov/coronavirus/TexasCOVID19DailyCountyFatalityCountData.xlsx -O out/texas_fatalities.xlsx
	ssconvert out/texas_fatalities.xlsx out/texas_fatalities.temp.csv
	sed -i 1,2d out/texas_fatalities.temp.csv
	sed -i 's/Fatalitites/Fatalities/g' out/texas_fatalities.temp.csv
	perl -pe 'chomp if /Fatalities/' out/texas_fatalities.temp.csv | \
		perl -pe 'chomp if /Fatalities/' | \
	       sed -e 's/Anderson/\nAnderson/'	> out/texas_fatalities.csv
	sed -i 's/"//g' out/texas_fatalities.csv
	sed -i -n '/Total,/q;p' out/texas_fatalities.csv
	sed -i 's/ \+/_/g' out/texas_fatalities.csv
	#sed -i 1d texas_fatalities.csv
	sed -i 's/2020\//Fatalities/g' out/texas_fatalities.csv
	#sed -i '/^$/d' texas_fatalities.csv
	#sed -i 's/\//-/g' texas_fatalities.csv
	sed -i 's/Fatalities_/Fatalities0/g' out/texas_fatalities.csv
	sed -i 's/Fatalities00/Fatalities0/g' out/texas_fatalities.csv
	sed -i 's/County_Name/Name/' out/texas_fatalities.csv
	sed -i 's/Andrews/\nAndrews/' out/texas_fatalities.csv
	sed -i 's/\//-/g' out/texas_fatalities.csv
fi

if [ $option == "--patch" ]
then
	# Remove 'training wheels' on number of runs
	sed -i 's/100, MSG_TOO_MANY_RUNS/100001, MSG_TOO_MANY_RUNS/' ../src/components/Main/validation/schema.ts
	sed -i 's/10, MSG_AT_LEAST_TEN/1, MSG_AT_LEAST_TEN/' ../src/components/Main/validation/schema.ts
	sed -i 's/minimum: 10/minimum: 1/' ../schemas/ScenarioDatumSimulation.yml
	sed -i 's/maximum: 100/maximum: 100001/' ../schemas/ScenarioDatumSimulation.yml 
	#sed -i 's/value < min/value < 1/' ../src/components/Form/FormSpinBox.tsx

	# Increase max percentage to 1000
	sed -i 's/100, MSG_MAX_100/1000, MSG_MAX_100/' ../src/components/Main/validation/schema.ts
	sed -i 's/maximum: 100/maximum: 1000/' ../schemas/PercentageRange.yml
 
	# Change default scenario (so the app will load after removing existing countries)
	sed -i -e "s/DEFAULT_SCENARIO_NAME = .* as const/DEFAULT_SCENARIO_NAME = 'TEXAS' as const/" ../src/constants.ts
	sed -i -e "s/DEFAULT_SEVERITY_DISTRIBUTION = .* as const/DEFAULT_SEVERITY_DISTRIBUTION = 'TEXAS' as const/" ../src/constants.ts

fi
