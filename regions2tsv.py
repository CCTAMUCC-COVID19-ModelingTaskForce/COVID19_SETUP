import geopandas as gpd
import pandas as pd

inFile = "regions/County_PublicHealthRegions.shp"
outFile = "region2county.tsv"

regionsShape = gpd.read_file(inFile)
regions = pd.DataFrame(regionsShape[["CNTY_NM", "TSA", "DIST_NM", "RAC", "PHR"]])
regions = regions.rename(columns = {"CNTY_NM" : "county", "TSA" : "tsa", "DIST_NM" : "district", "RAC" : "rac", "PHR" : "phr"})
regions["county"] = [r.lower().replace(" ", "_") for r in regions["county"]]
regions["tsa"] = [ "TSA-{}".format(a) for a in regions["tsa"]]
regions["phr"] = [ "PHR-{}".format(a) for a in regions["phr"]]

regions.to_csv(outFile, sep = "\t", index = False)

