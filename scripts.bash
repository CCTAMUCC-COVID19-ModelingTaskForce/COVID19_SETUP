# code to make a set of tsv files for a new TSA using an exsisting TSA's files, then convert to json

## load variables
oldTSA=V
newTSA=U

## make lists of old and new file names
ls TSA-${oldTSA}*tsv > fileNames_TSA-${oldTSA}.txt
sed "s/TSA-$oldTSA/TSA-$newTSA/g" > fileNames_TSA-${newTSA}.txt

## make copy of old files and name as new files
parallel --link "cp {1} {2}" :::: fileNames_TSA-${oldTSA}.txt fileNames_TSA-${newTSA}.txt

## replace old TSA w new TSA in new files
sed "s/TSA-$oldTSA/TSA-$newTSA/g" TSA-${newTSA}_params.tsv

## make json
python3 params2json.py -j TSA-${newTSA}_fit.json -p TSA-${newTSA}_params.tsv -a TSA-${newTSA}_popByAge.tsv -m TSA-${newTSA}_mitigations.tsv -s TSA-${newTSA}_severity.tsv


