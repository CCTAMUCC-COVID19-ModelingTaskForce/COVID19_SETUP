import geopandas as gpd
import pandas as pd

inFile = "regions/County_PublicHealthRegions.shp"
outFile = "region2county.tsv"

# Name to give region that combines all regions
comboName = "texas"

regionsShape = gpd.read_file(inFile)
regions = pd.DataFrame(regionsShape[["CNTY_NM", "TSA", "DIST_NM", "RAC", "PHR"]])
regions = regions.rename(columns = {"CNTY_NM" : "county", "TSA" : "tsa", "DIST_NM" : "district", "RAC" : "rac", "PHR" : "phr"})
regions["county"] = [r.lower().replace(" ", "_") for r in regions["county"]]
regions["tsa"] = [ "TSA-{}".format(a) for a in regions["tsa"]]
regions["phr"] = [ "PHR-{}".format(a) for a in regions["phr"]]

# Create a categorie that contains all categories
combo = regions.copy()
for col in ["tsa", "district", "rac", "phr"]:
	combo[col] = [comboName for a in regions[col]]
regions = pd.concat([regions, combo])

regions.to_csv(outFile, sep = "\t", index = False)

