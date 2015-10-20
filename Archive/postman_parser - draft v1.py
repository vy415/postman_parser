import argparse
import csv
import sys
#import requests
import lxml.etree as etree




def main():
	parser = argparse.ArgumentParser(description="Parse Postman XML Files for Available Apartment Units")
	parser.add_argument('infile', nargs='?', type=str, default='')
	parser.add_argument('outfile', nargs='?', type=str, default=sys.stdout)
	args = parser.parse_args()

	if args.infile != "":
		try:
			tree = etree.parse(args.infile)

			units = []
			for unitObjNode in tree.xpath("//UnitObject"):
				pmcID = unitObjNode.xpath(".//PmcID/text()")[0]
				siteID = unitObjNode.xpath(".//SiteID/text()")[0]
				unitNumber = unitObjNode.xpath(".//UnitNumber/text()")[0]
				floorplanID = unitObjNode.xpath(".//FloorplanID/text()")[0]
				sqft = unitObjNode.xpath(".//RentSqFtCount/text()")[0]
				rent = unitObjNode.xpath(".//BaseRentAmount/text()")[0]
				date = unitObjNode.xpath(".//AvailableDate/text()")[0]
				avail_bit = unitObjNode.xpath(".//AvailableBit/text()")[0]
				units.append({"PMC_ID": pmcID, "Site_ID": siteID, "UnitNumber": unitNumber, "FloorplanID": floorplanID, "Sqft": sqft, "Price": rent, "AvailableDate": date, "AvailableBit": avail_bit})

			with open(args.outfile, 'wb') as out_file:
				writer = csv.DictWriter(out_file, fieldnames=["PMC_ID", "Site_ID", "UnitNumber", "FloorplanID", "Sqft", "Price", "AvailableDate", "AvailableBit"])
				writer.writeheader()
				writer.writerows(units)

		except Exception as inst:
			sys.stderr.write("Fatal Error: %s. Aborting\n" % str(inst))

if __name__ == "__main__":
	main()