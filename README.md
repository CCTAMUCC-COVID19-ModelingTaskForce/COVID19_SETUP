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

	git clone https://github.com/neherlab/covid19_scenarios.git

#### Get Coastal Bend scenario repository
	
	cd covid19_scenarios
	git clone https://github.com/cbirdlab/COVID19_CoastalBend.git

#### Run covid19_scenarios

	cp .env.example .env
	yarn install
	yarn dev
	
#### Integrate Coastal Bend scenario
	cd COVID19_CoastalBend
	# Backup the original data files
	bash addCoastalBend.sh --backup

	# Patch code
	bash addCoastalBend.sh --patch
	
	# Update scenario files from web sources
	bash addCoastalBend.sh --update
	
	# Add scenario data files to covid19_scenarios application
	bash addCoastalBend.sh --add

#### Rerunning if something went wrong
	# If something goes wrong, troubleshoot and then run this in `COVID19_CoastalBend`
	bash addCoastalBend.sh --restore
	bash addCoastalBend.sh --update
	bash addCoastalBend.sh --add

Navigate to http://localhost:3000 in a browser. 

## Optional: update 'region2county.tsv`

The repo already contains a default `region2county.tsv` that maps counties to a region categories. Each region is a scenario within the application.
This file must contain at least two columns. One column has the name _county_ and each value is a county name in lower-case. Spaces have underscores such as "fort_bend". The second column can contain arbitrary strings (no spaces) used to categorize the counties. The application's defaut is Trama Service Areas (TSA). 

	# Generate region2county.tsv
	python3 regions2tsv.py

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
