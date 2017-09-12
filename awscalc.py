import sys

if len(sys.argv) < 2:
	print "Usage `python awscalc.py <filename.csv>`"
	sys.exit()

buffer = open(sys.argv[1])
data = buffer.readlines()
buffer.close()

services_data = {}
service_type = []
compute_total = 0.0
reserved_total = 0.0
ebs_total = 0.0
iops_total = 0.0
snapshots_total = 0.0
elb_total = 0.0
vpc_total = 0.0
dc_total = 0.0
cw_total = 0.0
ds_total = 0.0
data_out_total = 0.0
data_in_total = 0.0
support_total = 0.0
discount_total = 0.0
reserved_support = 0.0
ec2_other = 0.0

for line in data:
	line = line.strip()
	fields = line.split(",")
	if line.startswith("Your Estimate"):
		continue
	if line.startswith("Service Type"):
		continue
	if line.count("Free Tier Discount") == 1:
		discount_total = fields[4].strip()[1:]	
	if not line.startswith(','):
		service_type = fields[0]
		services_data[service_type] = {}
		services_data[service_type]['Total Price'] = fields[4]
	else:
		services_data[service_type][fields[1]] = fields[3] 

#Calculate compute info
for key in services_data.keys():
	if not 'EC2' in key:
		continue
	sub_keys =  services_data[key].keys()
	for sub_key in sub_keys:
		if 'Compute:' in sub_key:
			price = float(services_data[key][sub_key].strip()[1:])
			compute_total = compute_total + price
		elif 'Reserved Instances (One-time Fee):' in sub_key:
			price = float(services_data[key][sub_key].strip()[1:])
			reserved_total = reserved_total + price
		elif 'Elastic LBs:' in sub_key:
			price = float(services_data[key][sub_key].strip()[1:])
			elb_total = elb_total + price
		elif 'EBS Volumes:' in sub_key:
			price = float(services_data[key][sub_key].strip()[1:])
			ebs_total = ebs_total + price
		elif 'EBS IOPS:' in sub_key:
			price = float(services_data[key][sub_key].strip()[1:])
			iops_total = iops_total + price
		elif 'EBS Snapshots:' in sub_key:
			price = float(services_data[key][sub_key].strip()[1:])
			snapshots_total = snapshots_total + price
		else:
			if not 'Total' in sub_key:
				price = float(services_data[key][sub_key].strip()[1:])
				ec2_other = ec2_other + price
#Calculate VPC info
for key in services_data.keys():
	if not 'VPC' in key:
		continue
	price = float(services_data[key]['Total Price'].strip()[1:])	
	vpc_total = vpc_total + price

#Calculate Direct Connect info
for key in services_data.keys():
	if not 'Direct Connect' in key:
		continue
	price = float(services_data[key]['Total Price'].strip()[1:])	
	dc_total = dc_total + price

#Calculate CloudWatch info
for key in services_data.keys():
	if not 'CloudWatch' in key:
		continue
	price = float(services_data[key]['Total Price'].strip()[1:])	
	cw_total = cw_total + price

#Calculate Directory Service info
for key in services_data.keys():
	if not 'Directory Service' in key:
		continue
	price = float(services_data[key]['Total Price'].strip()[1:])	
	ds_total = ds_total + price

#Calculate Data Out info
for key in services_data.keys():
	if not 'Data Transfer Out' in key:
		continue
	price = float(services_data[key]['Total Price'].strip()[1:])	
	data_out_total = data_out_total + price

#Calculate Data In info
for key in services_data.keys():
	if not 'Data Transfer In' in key:
		continue
	price = float(services_data[key]['Total Price'].strip()[1:])	
	data_in_total = data_in_total + price

#Calculate Support info
for key in services_data.keys():
	if not 'AWS Support' in key:
		continue
	sub_keys =  services_data[key].keys()
	for sub_key in sub_keys:
		if 'Support for all AWS services:' in sub_key:
			price = float(services_data[key][sub_key].strip()[1:])
			support_total = price			
		if 'Support for Reserved Instances (One-time Fee):' in sub_key:
			price = float(services_data[key][sub_key].strip()[1:])
			reserved_support = price			

print "\n\nCopy the following lines of output, select cell C13 in the pricing spreadsheet, and paste:\n\n"

print compute_total
print elb_total
print ebs_total
print iops_total
print snapshots_total
print vpc_total
print dc_total
print cw_total
print ds_total
print data_out_total
print data_in_total
#print 0's for 'Other' fields, these will be printed separately
for i in range(0,7):
	print 0.0
print support_total
print discount_total
print reserved_total
print reserved_support

#Print out the prices of the other services not explicitly defined in the pricing spreadsheet
defined_services = ["EC2",
			"VPC",
			"Direct Connect",
			"CloudWatch",
			"Directory Service",
			"Data Transfer In",
			"Data Transfer Out",
			"AWS Support"]

#Print other price points not explicitly represented in the pricing spreadsheet, i.e. SQS, SNS, etc...
print "\n\nThe following services (if any) are not explicitly represented in our pricing spreadsheet.  You will need to manually enter them in the 'Other' fields in cells C24-C30:\n\n"

#Print any other EC2 service costs not explicitly represented in the pricing spreadsheet
print "Misc EC2-related Services: " + str(ec2_other)

for key in services_data.keys():
	defined = 0
	for defined_service in defined_services:
		if defined_service in key:
			defined = 1
	if defined == 1:
		continue
	else:
		print key + ": " + services_data[key]['Total Price'].strip()[1:]	
		
print "\n\n"
