## Tracking down all the data files that we need to alter or know about

### `data/case-counts/unitedstates_texas_coastalbend/USA-CoastalBend.tsv`

* This file has the confirmed case counts and other info that we upload

* This dir/file should be here `data/case-counts/unitedstates/USA-CoastalBend.tsv`


### `data/fit_parameters.json`

* this dir/file has the start data (tmin), initial number of cases (initialCases), and Ro (r0) for each country and state

* this dir/file should be automatically updated with coastal bend info, i think.  it does not have coastal bend right now

### `data/generate_data.py`

* this file has parsers

* run this to generate various files, then move the files to  `src/assets/data`

* Evan thinks this runs model.py

### `data/initialCondition.tsv`

* this file has the initial number of cases, tMin, tMax for each country and state

* CoastalBend is in here, but I suspect it should be populated automatically

* see what happens when we run model.py


### `data/__init__.py`

* this file seems only contain this name

### `data/Makefile`

* run with `make` to update data  

* It looks like it is some sort of master controller script calling `generate_data.py`

	* it removes the `generated/**` dir
	* it runs generate_data.py --fetch
	* it runs generate_data.py --output-scenarios ../src/assets/data/scenarios/scenarios.json \
                --output-cases ../src/assets/data/case_counts.json

### `data/paths.py`

* This file sets variables containing the locations of several files

### `data/Pipfile`

* this file seems to have python packages to load

* according to the readme, this allows pipenv to spin up and run everything in here

### `data/Pipfile.lock`

* Evan, what does this do, and do we care?

### `data/populationData.tsv`

* this file contains the following columns:
	* pop size
	* ageDistribution, the name of the moniker to grab age distributions from
	* hospitalBeds
	* ICUBeds
	* hemisphere
	* srcPopulation
	* srcHospitalBeds
	* srcICUBeds

* CoastalBend is here, but it needs to point to the ageDistribution named CoastalBend instead of united states

### `README.md`

* it has markdown instructions on how to run the scripts in this dir

### `data/sources.json`

* this seems to have url to the data sources for each region/country


### `data/case-counts/*`

* this is where the case count data is stored

### `data/generated/types.py`

* Evan thinks this generates custom "types" on the fly and needs to be called for program to run

* "it gets made" by yarn.dev

* probably need to run yarn.dev just to make this dir and be able to run program locally

### `data/hospital-data/hospital_capacity.csv`

* seems to have hospital capacity by year and country, but no United States

### `data/hospital-data/ICU_capacity.csv`

* seems to have icu capacity data, but no United States

### `data/parsers`

* this is where we put our parsing script. it is there

### `data/scripts/default_schema_values.py`

* This file contains the default Epidemiological and Mitigation (containment) Data
	* latencyTime
	* infectiousPeriod
	* lengthHospitalStay
	* lengthICUStay
	* seasonalForcing
	* peakMonth
	* overflowSeverity
	* r0
	* numberPoints     #not sure what this is? something to do with mitigation, perhaps old setting for sliders in old interface
	

### `data/scripts/download_age_dists.py`

* This script grabs the age dist data for each country and saves it to `src/assets/data/country_age_distribution.json`
* so we just need to hack that json file
	

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
### `data/scripts/model.py`

* "All details of our fitting algorithms can be found within data/scripts/model.py"
* This script is the one that estimates Ro, initial date from our case data according to the discussion I had on github https://github.com/neherlab/covid19_scenarios/discussions/18#discussioncomment-4255
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

### `data/scripts/populations.py`

* This script generates the json with the population presets that contain
 * name
 * populationServed
 * initial cases
 * imports
 * hospital beds
 * ICU beds

### `data/scripts/scenarios.py`

* this script has mitigation measures and seems to be linked to the list of scenarios, need to look at this closer
* seems that mitigation scenarios are not read in

### `data/scripts/transform_ages.py`

* Evan? seems like this converts data format

### `data/scripts/tsv.py`

* parse all manually maintained .tsv files in the case-counts/ folder 
	* this should be run from the top level of the repo.

###


