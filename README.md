# COVID19_CoastalBend
Scripts and data for populating Covid19_scenario with Coastal Bend scenario data

## Summary

The repo is used to insert the Coastal Bend scenario so that it can be used with the covid19_scenario package (https://covid19-scenarios.org)

## Quick Start: Generate 'json' for loading scenario into covid19_scenarios

#### Use default tsv files, assumed sitting in directory

	python3 params2json.py -j output.json

#### OR specify each input tsv 
	python3 params2json.py -j output.json \
		-p PARAMS.tsv -a AGE_DIST.tsv -m MITIGATIONS.tsv -s SEVERITY.tsv

## Quick Start: First Time Running

#### Get dependencies

	sudo apt-get install gnumeric

#### Get covid19_scenarios repository

	git clone --recursive https://github.com/neherlab/covid19_scenarios.git

#### Get this repository
	
	cd covid19_scenarios
	git clone https://github.com/cbirdlab/COVID19_SETUP.git

#### Run covid19_scenarios

	cp .env.example .env
	yarn install
	yarn dev
	
#### Integrate Coastal Bend scenario
	cd COVID19_SETUP
	# Backup the original data files
	bash addRegions.sh --backup

	# Patch code
	bash addRegions.sh --patch
	
	# Update scenario files from web sources
	bash addRegions.sh --update
	
	# Generate scenario data files and add to covid19_scenarios application
	bash addRegions.sh --add

Navigate to http://localhost:3000 in a browser. 

## Optional: update 'region2county.tsv`

The repo already contains a default `region2county.tsv` that maps counties to a region categories. Each region is a scenario within the application.
This file must contain at least two columns. One column has the name _county_ and each value is a county name in lower-case. Spaces have underscores such as "fort_bend". The second column can contain arbitrary strings (no spaces) used to categorize the counties. The application's defaut is Trama Service Areas (TSA). 

	# Generate region2county.tsv
	python3 regions2tsv.py

	# Check the top of the file
	head -n 5 region2county.csv
	county  tsa     district        rac     phr
	atascosa        TSA-P   san_antonio     southwest_texas_rac     PHR-8
	matagorda       TSA-Q   yoakum  southeast_texas PHR-6/5s
	jackson TSA-S   yoakum  golden_crescent PHR-8
	de_witt TSA-S   yoakum  golden_crescent PHR-8

## Optional: update 'region2popByAge.tsv'

The file `region2popByAge.tsv` maps a region (by default, Trama Service Area) to a population distribution. 
These corrospond to the "age distribution" on the `covid_scenarios` web app. 

This file is created with `regions2popByAge.py` using the region to county mapping in `region2county.tsv` (see above) 
and the demographic information in `regions/Texas_Demographics.csv`. 
The user supplies a key, which is the name of the desired region category column in `region2popByAge.tsv`. The default is _tsa_. 

If this file is present, the script `gendata.py` will use this population data instead of the `default_popByAge.tsv`. 
However, if a particular region has its own named parameter file (i.e. `TSA-V_popByAge.tsv`), the named parameter file will be used. 

	# Generate region2popByAge.tsv
	python3 regions2popByAge.py -r region2county.tsv -d regions/Texas_Demographics.csv -k tsa

	# Check the top of the file 
	head -n 5 region2popByAge.tsv
	tsa     age     total
	TEXAS   0-9     4064462
	TEXAS   10-19   4124801
	TEXAS   20-29   4199337
	TEXAS   30-39  	4018531

	# Check the bottom of the file
	tail -n 5 region2popByAge.tsv
	TSA-V   40-49   170704
	TSA-V   50-59   140101
	TSA-V   60-69   114586
	TSA-V   70-79   74496
	TSA-V   80+     39955

## Quick Start After First Time: Upgrade the covid19_scenario model

These steps allow you to pull the latest changes to `covid19_scenarios`. 
First, you have to remove the Coastal Bend data for a smooth upgrade.

#### Restore original data

	cd covid19_scenarios/COVID19_CoastalBend
	bash addCoastalBend.sh --restore

	cd ..
	git pull

	cd COVID19_CoastalBend
	bash addCoastalBend.sh --backup
	bash addCoastalBend.sh --update
	bash addCoastalBend.sh --add

## How to set up each week's `covid19_scenarios` repo
In the following, `$Y` is the year, `$M` is the month, and `$D` is the day.

#### Create local repo
	Y=year   # Replace year with actual year i.e. 2020
	M=month  # Replace month with actual month i.e. 03
	D=day    # Replace day with actual day i.e. 13
	mkdir c19s_$Y$M$D
	cd c19s_$Y$M$D

#### Clone `covid19_scenarios` and this repo, `COVID19_SETUP`
	
	git clone --recursive https://github.com/neherlab/covid19_scenarios.git
	cd covid19_scenarios
	git clone https://github.com/CCTAMUCC-COVID19-ModelingTaskForce/COVID19_SETUP.git
	rm -rf .git* COVID19_SETUP/.git*
	
#### Create repo on github

Navigate to github.com and create repo `c19s_$Y$M$D` in organization `CCTAMUCC-COVID19-ModelingTaskForce`

#### Associate local repo with the github repo
	
	cd ..
	git init
	git remote add origin https://github.com/CCTAMUCC-COVID19-ModelingTaskForce/c19s_$Y$M$D.git
	git add -A
	git commit -m "Init"
	git push -u origin master
	
#### Setup data	

First, follow the above **Quick Start: First Time Running**. 
Then, test out the web application locally.
If all is well, commit and push changes as below:

	git add -A
	git commit -m "Ready"
	git push
	
#### Clone and run on production server `Lancelot`

First, ssh into `Lancelot`

	cd /media/HD2
	git clone https://github.com/CCTAMUCC-COVID19-ModelingTaskForce/c19s_$Y$M$D
	cd c19s_$Y$M$D/covid19_scenarios
	yarn install
	yarn dev
