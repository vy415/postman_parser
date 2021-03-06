import argparse
import csv
import sys
#import requests
import lxml.etree as etree




def main():
	parser = argparse.ArgumentParser(description="Parse Postman XML Files for Available Apartment Units")
	parser.add_argument('infile_fp', nargs='?', type=str, default='')
	parser.add_argument('infile_units', nargs='?', type=str, default='')
	parser.add_argument('outfile', nargs='?', type=str, default=sys.stdout)
	args = parser.parse_args()

	if args.infile_fp != "" and args.infile_units != "":
		try:
			fp_tree = etree.parse(args.infile_fp)

			floorplans = {}
			for floorplanObjNode in fp_tree.xpath("//FloorPlanObject"):
				floorplanID = floorplanObjNode.xpath(".//FloorPlanID/text()")[0]
				floorplanName = floorplanObjNode.xpath(".//FloorPlanName/text()")[0]
				bed = floorplanObjNode.xpath(".//Bedrooms/text()")[0]
				bath = floorplanObjNode.xpath(".//Bathrooms/text()")[0]
				floorplans[floorplanID] = [floorplanName, bed, bath]

	#if args.infile_units != "":
	#	try:
			unit_tree = etree.parse(args.infile_units)

			units = []
			for unitObjNode in unit_tree.xpath("//UnitObject"):
				pmcID = unitObjNode.xpath(".//PmcID/text()")[0]
				siteID = unitObjNode.xpath(".//SiteID/text()")[0]
				unitNumber = unitObjNode.xpath(".//UnitNumber/text()")[0]
				floorplanID = unitObjNode.xpath(".//FloorplanID/text()")[0]
				sqft = unitObjNode.xpath(".//RentSqFtCount/text()")[0]
				rent = unitObjNode.xpath(".//BaseRentAmount/text()")[0]
				date = unitObjNode.xpath(".//AvailableDate/text()")[0]
				avail_bit = unitObjNode.xpath(".//AvailableBit/text()")[0]
				
				#units.append({"PMC_ID": pmcID, "Site_ID": siteID, "UnitNumber": unitNumber, "FloorplanID": floorplanID, "Sqft": sqft, "Price": rent, "AvailableDate": date, "AvailableBit": avail_bit})
				fpName = floorplans[floorplanID][0]
				bed = floorplans[floorplanID][1]
				bath = floorplans[floorplanID][2]
				units.append({"PMC_ID": pmcID, "Site_ID": siteID, "UnitNumber": unitNumber, "FloorplanID": floorplanID, "FloorplanName": fpName, "Sqft": sqft, "Bed": bed, "Bath": bath, "Price": rent, "AvailableDate": date, "AvailableBit": avail_bit})


			with open(args.outfile, 'wb') as out_file:
				writer = csv.DictWriter(out_file, fieldnames=["PMC_ID", "Site_ID", "UnitNumber", "FloorplanID", "FloorplanName", "Sqft", "Bed", "Bath", "Price", "AvailableDate", "AvailableBit"])
				writer.writeheader()
				writer.writerows(units)

		except Exception as inst:
			sys.stderr.write("Fatal Error: %s. Aborting\n" % str(inst))

	else:
		sys.stderr.write("Missing input files! Need floorplan and units file.")

if __name__ == "__main__":
	main()