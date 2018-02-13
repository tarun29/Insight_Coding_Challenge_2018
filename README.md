# Insight_Coding_Challenge_2018

Coding Challenge - Feb 2018: 
The python script is inside the src folder. I have implemented the challenge using nested dictiories in python. This allows for easier lookup and organization of data for other purposes as well. 

The code reads each line and first checks if any of the data violates the input consideration. This is followed by checking if the donor is a repeat donor. This is done using the hash map "zipdict". It also stores the number of times the donor has donated to each recipient and the year of donation.  Similarly "maindict" keeps track of things on the recipient end. Every time a donation is made from a repeat donor, it updates the total amount donated to that recipient for that year and zipcode. Percentile is calculated for repeat donors as a whole.

At the end of each read, the output file is updated with the required information. 


# Test Cases checked for: 
1. General Repeat donor donating to a recipient in a given year and zip code. 
2. Repeat donor but a new donation to this particular recipient for this year and zipcode. 
3. Repeat donor donating a second time in the same year(but has donated to this recipient only the first time this year), in this case the first donation is tracked in the dictionary and is added to the "maindict" dictionary to keep track of total amount donated from this donor to this recipient this year. 

