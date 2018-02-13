import sys
import time
import math
from collections import defaultdict


##############################################
# Function to Check if the name is empty or malformed
def checkname(nameofdonor):
    flag = 1
    for char in nameofdonor:
        if char.isalpha() or char == "," or char == " " or char == ".":
            flag = 1
        else:
            flag = 0
            break
    if (nameofdonor == ""):
        flag = 0
    return flag


##############################################


def process(donations_file, percentile_file, destination_file):
    zipdictionary = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    maindict = defaultdict(lambda: defaultdict(dict))
    output_filehandler = open(destination_file, 'w')
    infile = open(percentile_file, 'r')
    percentilecal = float(infile.readline())
    percentilelist = []


    for line in open(donations_file, 'r'):
        namesList = line.split("|")
        recipientid = namesList[0]
        donorname = namesList[7]
        zipcode = namesList[10][:5]  
        transaction_date = namesList[13][4:]
        transaction_amount = int(namesList[14])
        other_id = namesList[15]

        ################################################################
        # To Check Input file Considerations
        try:
            if (other_id != ""):
                raise
            datecheck = int(transaction_date)
            zipcodecheck = int(zipcode)
            if len(zipcode) < 5:
                raise
            if recipientid == "" or transaction_amount == "":
                raise
            if checkname(donorname) == 0:
                raise

        except Exception:
            pass

        else:
            if zipcode not in zipdictionary or donorname not in zipdictionary[zipcode]:  #if new donor

                zipdictionary[zipcode][donorname][transaction_date][recipientid] = [0, 0]
                zipdictionary[zipcode][donorname][transaction_date][recipientid][
                    0] = 0  # This field represents numbers of times donated this year to this recipient for this zip code and donor. 
                zipdictionary[zipcode][donorname][transaction_date][recipientid][
                    1] = transaction_amount  # This field represents amount donated this year to this recipient
            else: # if Repeat Donor
                if transaction_date not in zipdictionary[zipcode][donorname] or recipientid not in \
                        zipdictionary[zipcode][donorname][
                            transaction_date]:  
                    zipdictionary[zipcode][donorname][transaction_date][recipientid] = [0, 0]

                if transaction_date not in maindict or zipcode not in maindict[transaction_date] or recipientid not in \
                        maindict[transaction_date][zipcode]:  # initialized maindict to 000
                    maindict[transaction_date][zipcode][recipientid] = [0, 0, 0]

                if zipdictionary[zipcode][donorname][transaction_date][recipientid][
                    1] == 0:  # Case when repeat donor who has never donated this year to the recipient. So we check that through transaction amount.
                    percentilelist.append(transaction_amount)
                    maindict[transaction_date][zipcode][recipientid][0] += 1
                    maindict[transaction_date][zipcode][recipientid][1] += transaction_amount
                elif zipdictionary[zipcode][donorname][transaction_date][recipientid][
                    0] == 0:  
                    percentilelist.append(transaction_amount)
                    maindict[transaction_date][zipcode][recipientid][1] += \
                        zipdictionary[zipcode][donorname][transaction_date][recipientid][1] + transaction_amount
                    maindict[transaction_date][zipcode][recipientid][
                        0] += 2  
                else:
                    percentilelist.append(transaction_amount)
                    maindict[transaction_date][zipcode][recipientid][1] += transaction_amount
                    maindict[transaction_date][zipcode][recipientid][0] += 1

                zipdictionary[zipcode][donorname][transaction_date][recipientid][0] += 1
                count = maindict[transaction_date][zipcode][recipientid][0]
                totalamt = maindict[transaction_date][zipcode][recipientid][1]
		
                sortedpercentilelist = sorted(percentilelist, key=int)
                percentileindex1 = int(math.ceil(float(percentilecal / 100.0) * len(sortedpercentilelist)))
                percentile = sortedpercentilelist[percentileindex1-1]

                output_filehandler.write(
                    "%s|%s|%s|%d|%d|%d\n" % (recipientid, zipcode, transaction_date, percentile, totalamt, count))

    output_filehandler.close()


def main(argv):
    start_time = time.time()
    donations_file = argv[1]
    percentile_file = argv[2]
    destination_file = argv[3]
    process(donations_file, percentile_file, destination_file)

    print "Output file created at " + argv[3]
    print "Execution took " + str(time.time() - start_time) + "seconds"

if __name__ == '__main__':
    main(sys.argv)
