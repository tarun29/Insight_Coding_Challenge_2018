import sys
import time
import math
from collections import defaultdict


##############################################
# Function to Check if the name is empty or malformed
def checkname(name_of_donor):
    flag = 1
    for char in name_of_donor:
        if char.isalpha() or char == "," or char == " " or char == ".":
            flag = 1
        else:
            flag = 0
            break
    if (name_of_donor == ""):
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
        recipient_id = namesList[0]
        donor_name = namesList[7]
        zip_code = namesList[10][:5]  
        transaction_date = namesList[13][4:]
        transaction_amount = int(namesList[14])
        other_id = namesList[15]

        ################################################################
        # To Check Input file Considerations
        try:
            if (other_id != ""):
                raise
            datecheck = int(transaction_date)
            zip_codecheck = int(zip_code)
            if len(zip_code) < 5:
                raise
            if recipient_id == "" or transaction_amount == "":
                raise
            if checkname(donor_name) == 0:
                raise

        except Exception:
            pass

        else:  #if none of the input file considerations is violated.
            if zip_code not in zipdictionary or donor_name not in zipdictionary[zip_code]:  #if new donor
                #zipdictionary is used to check for repeat donors and to keep track of each donation.
                zipdictionary[zip_code][donor_name][transaction_date][recipient_id] = [0, 0]
                zipdictionary[zip_code][donor_name][transaction_date][recipient_id][
                    0] = 0  # This field represents numbers of times donated this year to this recipient for this zip code and donor. 
                zipdictionary[zip_code][donor_name][transaction_date][recipient_id][
                    1] = transaction_amount  # This field represents amount donated this year to this recipient
            else: # if Repeat Donor
                if transaction_date not in zipdictionary[zip_code][donor_name] or recipient_id not in \
                        zipdictionary[zip_code][donor_name][
                            transaction_date]:  
                    zipdictionary[zip_code][donor_name][transaction_date][recipient_id] = [0, 0]

                if transaction_date not in maindict or zip_code not in maindict[transaction_date] or recipient_id not in \
                        maindict[transaction_date][zip_code]:  # initialized maindict to 00
                    maindict[transaction_date][zip_code][recipient_id] = [0, 0]  #maindict keeps track of recipient.
                    # The first element in the value list above is the number of donations to this recipient in this year and from this zipcode.
                    # The second element is the total amount donated for this year and zipcode.

                if zipdictionary[zip_code][donor_name][transaction_date][recipient_id][
                    1] == 0:  # Case when repeat donor has never donated this year to this recipient.
                    percentilelist.append(transaction_amount)
                    maindict[transaction_date][zip_code][recipient_id][0] += 1
                    maindict[transaction_date][zip_code][recipient_id][1] += transaction_amount
                elif zipdictionary[zip_code][donor_name][transaction_date][recipient_id][
                    0] == 0:  # Case when this donor is donating the second time to this recipient. Hence the donors first amount has to be added to the total donated from this donor value.
                    percentilelist.append(transaction_amount)
                    maindict[transaction_date][zip_code][recipient_id][1] += \
                        zipdictionary[zip_code][donor_name][transaction_date][recipient_id][1] + transaction_amount
                    maindict[transaction_date][zip_code][recipient_id][
                        0] += 2  
                else:
                    percentilelist.append(transaction_amount)
                    maindict[transaction_date][zip_code][recipient_id][1] += transaction_amount
                    maindict[transaction_date][zip_code][recipient_id][0] += 1

                zipdictionary[zip_code][donor_name][transaction_date][recipient_id][0] += 1
                count = maindict[transaction_date][zip_code][recipient_id][0]
                totalamt = maindict[transaction_date][zip_code][recipient_id][1]


                #Percentile Calculation
                sortedpercentilelist = sorted(percentilelist, key=int)
                percentileindex1 = int(math.ceil(float(percentilecal / 100.0) * len(sortedpercentilelist)))
                percentile = sortedpercentilelist[percentileindex1-1]

                output_filehandler.write(
                    "%s|%s|%s|%d|%d|%d\n" % (recipient_id, zip_code, transaction_date, percentile, totalamt, count))

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
