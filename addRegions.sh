# Script adds data for Coastal Bend scenario
# Run from covid19_scenarios/coastalbend

option=$1

# Backup repo (for later restore)
if [ $option == "--backup" ]
then
	# Data sources
	cp ../data/sources.json sources.json.orig
	cp ../data/country_codes.csv country_codes.csv.orig
	cp ../data/populationData.tsv populationData.tsv.orig
	cp ../data/hospital-data/hospital_capacity.csv hospital_capacity.csv.orig
	cp ../data/hospital-data/ICU_capacity.tsv ICU_capacity.tsv.orig
	#### cp ../data/initialCondition.tsv initialCondition.tsv.orig    # Autopopulated?
	# Data assets
	cp ../src/assets/data/caseCounts.json caseCounts.json.orig
	cp ../src/assets/data/ageDistribution.json ageDistribution.json.orig
	cp ../src/assets/data/severityDistributions.json severityDistributions.json.orig
	cp ../src/assets/data/scenarios.json scenarios.json.orig
fi

# Clean repo (remove coastal bend scenario)
if [ $option == "--restore" ]
then
	# Data sources
	rm ../data/parsers/CoastalBend.py
	cp sources.json.orig ../data/sources.json
	cp country_codes.csv.orig ../data/country_codes.csv
	cp populationData.tsv.orig ../data/populationData.tsv 
	cp hospital_capacity.csv.orig ../data/hospital-data/hospital_capacity.csv
	cp ICU_capacity.tsv.orig ../data/hospital-data/ICU_capacity.tsv
	#### cp initialCondition.tsv.orig ../data/initialCondition.tsv   # Autopopulated?
	# Data assets
	cp caseCounts.json.orig ../src/assets/data/caseCounts.json
	cp ageDistribution.json.orig ../src/assets/data/ageDistribution.json
	cp severityDistributions.json.orig ../src/assets/data/severityDistributions.json
	cp scenarios.json.orig  ../src/assets/data/scenarios.json
fi

if [ $option == "--add" ]
then
	# Add parser
	cp out/*.py ../data/parsers/ 
	# Add sources
	sed -i '$ d' ../data/sources.json
	sed -i '$ d' ../data/sources.json
	cat out/sources.json.cb >> ../data/sources.json
	# Add county codes
	cat out/country_codes.csv.cb >> ../data/country_codes.csv
	# Add population data
	cat out/populationData.tsv.cb >> ../data/populationData.tsv

	# Add age distribution
	head -n -3 ../src/assets/data/ageDistribution.json > ageDistribution.temp
	echo "}," >> ageDistribution.temp
	cat out/ageDistribution.json.cb >> ageDistribution.temp
	echo "] }" >> ageDistribution.temp
	cp ageDistribution.temp ../src/assets/data/ageDistribution.json

	# Add Hospital capacity 
	#cat hospital_capacity.csv.cb >> ../data/hospital-data/hospital_capacity.csv
	# Add ICU capacity 
	#cat ICU_capacity.tsv.cb >> ../data/hospital-data/ICU_capacity.tsv
	##### Add initial conditions  <---- perhaps not. Autopopulated?
	####cat initialCondition.tsv.cb >> ../data/initialCondition.tsv

	# Generate asset data
	cd ../data/
	python3 generate_data.py --fetch --parsers CoastalBend
	python3 generate_data.py \
		--output-cases ../src/assets/data/caseCounts.json \
		--output-population ../src/assets/data/population.json \
		--output-scenarios ../src/assets/data/scenarios.json
fi

if [ $option == "--update" ]
then
	# Update the contents of CoastalBend .cb files

	# Pull data from web
	# Cases
	wget --no-check-certificate \
	       	https://dshs.texas.gov/coronavirus/TexasCOVID19DailyCountyCaseCountData.xlsx -O texas_cases.xlsx
	ssconvert texas_cases.xlsx texas_cases.temp.csv
	sed -i 1,2d texas_cases.temp.csv
	sed -i 's/County Name/Name/' texas_cases.temp.csv
	perl -pe 'chomp if /Cases/' texas_cases.temp.csv | \
	       perl -pe 'chomp if /Cases/' | \
	      sed -e 's/Anderson/\nAnderson/'  > texas_cases.csv
	sed -i 's/"//g' texas_cases.csv
	sed -i '1,/,,,,,,,,,/!d' texas_cases.csv
	sed -i '$ d' texas_cases.csv
	sed -i '$ d' texas_cases.csv
	sed -i -e 's/_x000D_//g' -e 's/ //g' texas_cases.csv 
	sed -i 's/Andrews/\nAndrews/' texas_cases.csv
	sed -i -e "s/\r//g" texas_cases.csv

	# Fatalities
	wget --no-check-certificate \
		https://dshs.texas.gov/coronavirus/TexasCOVID19DailyCountyFatalityCountData.xlsx -O texas_fatalities.xlsx
	ssconvert texas_fatalities.xlsx texas_fatalities.temp.csv
	sed -i 1,2d texas_fatalities.temp.csv
	sed -i 's/Fatalitites/Fatalities/g' texas_fatalities.temp.csv
	perl -pe 'chomp if /Fatalities/' texas_fatalities.temp.csv | \
		perl -pe 'chomp if /Fatalities/' | \
	       sed -e 's/Anderson/\nAnderson/'	> texas_fatalities.csv
	sed -i 's/"//g' texas_fatalities.csv
	sed -i -n '/Total,/q;p' texas_fatalities.csv
	sed -i 's/ \+/_/g' texas_fatalities.csv
	#sed -i 1d texas_fatalities.csv
	sed -i 's/2020\//Fatalities/g' texas_fatalities.csv
	#sed -i '/^$/d' texas_fatalities.csv
	#sed -i 's/\//-/g' texas_fatalities.csv
	sed -i 's/Fatalities_/Fatalities0/g' texas_fatalities.csv
	sed -i 's/Fatalities00/Fatalities0/g' texas_fatalities.csv
	sed -i 's/County_Name/Name/' texas_fatalities.csv
	sed -i 's/Andrews/\nAndrews/' texas_fatalities.csv
	sed -i 's/\//-/g' texas_fatalities.csv


	# Update locally
	# Age distribution
	mapfile -t -s 1 agepop < <(awk '{print $2}' coastalBend_popByAge.tsv)
	echo {\"name\": \"CoastalBend\", \"data\": [{ \"ageGroup\": \"0-9\", \"population\": "${agepop[1]}" }, { \"ageGroup\": \"10-19\", \"population\": "${agepop[1]}" }, { \"ageGroup\": \"20-29\", \"population\": "${agepop[2]}" }, { \"ageGroup\": \"30-39\", \"population\": "${agepop[3]}" }, { \"ageGroup\": \"40-49\", \"population\": "${agepop[4]}" }, { \"ageGroup\": \"50-59\", \"population\": "${agepop[5]}" }, { \"ageGroup\": \"60-69\", \"population\": "${agepop[6]}" }, { \"ageGroup\": \"70-79\", \"population\": "${agepop[7]}" }, { \"ageGroup\": \"80+\", \"population\": "${agepop[8]}" } ]} > ageDistribution.json.cb

	mapfile -t -s 1 agepop < <(awk '{print $2}' coastalBend_popByAge.tsv)
	populationSize=$(IFS=+; echo "$((${agepop[*]}))")
	echo "CoastalBend	${populationSize}	CoastalBend	357	30	Northern	None	None	None" > populationData.tsv.cb

fi

if [ $option == "--patch" ]
then
	# Remove 'training wheels' on number of runs
	sed -i 's/100, MSG_TOO_MANY_RUNS/100001, MSG_TOO_MANY_RUNS/' ../src/components/Main/validation/schema.ts
	sed -i 's/10, MSG_AT_LEAST_TEN/1, MSG_AT_LEAST_TEN/' ../src/components/Main/validation/schema.ts
	sed -i 's/minimum: 10/minimum: 1/' ../schemas/ScenarioDatumSimulation.yml
	sed -i 's/maximum: 100/maximum: 100001/' ../schemas/ScenarioDatumSimulation.yml 
	sed -i 's/value < min/value < 1/' ../src/components/Form/FormSpinBox.tsx

	# Remove other countries
	cd ../data
	mv case-counts/ case-counts-disabled/
	mkdir case-counts
	mv parsers/ parsers-disabled/
	mkdir parsers
	cp parsers-disables/utils.py  parsers/

fi
