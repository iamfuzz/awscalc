import sys

if len(sys.argv) < 2:
	print "Usage `python awscalc.py <filename.txt>`"
	sys.exit()

supported_services = ['Compute',
			'Elastic LBs',
			'Data Processed by Elastic LBs',
			'EBS Volumes',
			'EBS IOPS',
			'EBS Snapshots',
			'Reserved Instances (One-time Fee)',
			'Amazon CloudWatch Service',
			'AWS Directory Service',
			'AWS Direct Connect Service',
			'Amazon VPC Service',
			'AWS Data Transfer In',
			'AWS Data Transfer Out',
			'Support for all AWS services',
			'Free Tier Discount',
			'Support for Reserved Instances (One-time Fee)']

buffer = open(sys.argv[1])
data = buffer.readlines()
buffer.close()

services_data = {}

counter = 0
for line in data:
	line = line.strip()
	#remove trailing : is it exists
	if line.endswith(":"):
		line = line[0:-1]
	#remove region info if it exists
	if (line.count("(") >= 1) and (line.count('One-time Fee') <= 0):
		line = line[0:line.find('(')].strip()
	if line in supported_services:
		if not services_data.has_key(line):
			services_data[line] = []
			services_data[line].append(data[counter + 3].strip())
		else:
			services_data[line].append(data[counter + 3].strip())
	else:
		pass
	counter = counter + 1

pricing_data = {}

for key in services_data.keys():
	value = services_data[key]
	if len(value) == 1:
		pricing_data[key] = value[0]
	else:
		sum = 0.00
		for item in value:
			sum = sum + float(item)
		pricing_data[key] = sum

#print out values so that they can simply be copy/pasted into spreadsheet
if pricing_data.has_key('Compute'):
	print pricing_data['Compute']
else:
	print "0.00"


if pricing_data.has_key('Elastic LBs'):
	print float(pricing_data['Elastic LBs']) + float(pricing_data['Data Processed by Elastic LBs'])
else:
	print "0.00"

if pricing_data.has_key('EBS Volumes'):
	print pricing_data['EBS Volumes']
else:
	print "0.00"

if pricing_data.has_key('EBS IOPS'):
	print pricing_data['EBS IOPS']
else:
	print "0.00"


if pricing_data.has_key('EBS Snapshots'):
	print pricing_data['EBS Snapshots']
else:
	print "0.00"

if pricing_data.has_key('Amazon VPC Service'):
	print pricing_data['Amazon VPC Service']
else:
	print "0.00"

if pricing_data.has_key('AWS Direct Connect Service'):
	print pricing_data['AWS Direct Connect Service']
else:
	print "0.00"

if pricing_data.has_key('Amazon CloudWatch Service'):
	print pricing_data['Amazon CloudWatch Service']
else:
	print "0.00"

if pricing_data.has_key('AWS Directory Service'):
	print pricing_data['AWS Directory Service']
else:
	print "0.00"

if pricing_data.has_key('AWS Data Transfer Out'):
	print pricing_data['AWS Data Transfer Out']
else:
	print "0.00"

if pricing_data.has_key('AWS Data Transfer In'):
	print pricing_data['AWS Data Transfer In']
else:
	print "0.00"

#account for "Other" fields.  Just 0 them out for now and allow for manual adjustment
for i in range(0,7):
	print "0.00"

if pricing_data.has_key('Support for all AWS services'):
	print pricing_data['Support for all AWS services']
else:
	print "0.00"

if pricing_data.has_key('Free Tier Discount'):
	print pricing_data['Free Tier Discount']
else:
	print "0.00"

if pricing_data.has_key('Reserved Instances (One-time Fee)'):
	print pricing_data['Reserved Instances (One-time Fee)']
else:
	print "0.00"

if pricing_data.has_key('Support for Reserved Instances (One-time Fee)'):
	print pricing_data['Support for Reserved Instances (One-time Fee)']
else:
	print "0.00"
