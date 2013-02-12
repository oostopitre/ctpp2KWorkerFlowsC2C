# The MIT License (MIT)
# Copyright (c) <2013> <Abi Komma>
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, I
# NCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#-------------------------------------------------------------------------------
# Purpose:    Script to tabulate a County-to-County Worker Flows from the 2000 CTPP Data
# Inputs:     This script uses two inputs:
#              1. 2KWRKCO_US.txt as an input file. Fixed File Format containing the Year 2000 CTPP for entire USA
#              Input File Format -   1-2      Res_ST     FIPS State Code of Residence
#                                    4-6      Res_CO     FIPS County Code of Residence
#                                   18-57      Res_Name   Residence County name and State abbreviation
#                                   59-61      Wrk_ST     Modified FIPS State Code or Foreign Country/Area Code of Workplace
#                                   63-65      Wrk_CO     FIPS County Code of Workplace
#                                   77-116     Wrk_Name   Workplace area name and State abbreviation
#                                   118-124    Count      Number of Workers 16 years old and over in the commuter flow
#              2. extract_Counties.csv as an input file. The unique list of counties which cover the Study Area of interest
#              Input File Format - 2 fields: CNTYIDFP00,NAME00
# Author:      Abi Komma
# Created:     30/11/2012
# Version:     Python 2.7.3
#-------------------------------------------------------------------------------


#CONSTANTS
_inputFileCTPP = './rawCTPP/2KWRKCO_US.txt'
_inputFileCounties = './extract_Counties.csv'

_outputFileCCFlows = 'ctpp2K_workerFlows_C2C.csv'

#Initialize Variables and Open Files
import csv, os, math

myCounties = {}
ctppCCFLows = {}


#Read the input .csv file to store the unique set of counties in the study area
with open(_inputFileCounties) as inputFile:
    reader = csv.reader(inputFile)
    print('opening file:', _inputFileCounties)
    _lineCount = 0

    #Process each line in input file
    for line in reader:
        _lineCount += 1
        if _lineCount == 1:              #read in headers
            headers = line
            continue

        #Record the fields in the csv file
        myCounties.update({line[headers.index('CNTYIDFP00')]:line[headers.index('NAME00')]})

#Now read the input .txt file containing the  CTPP data
with open(_inputFileCTPP) as inputFile:
    print('opening file:', _inputFileCTPP)
    _lineCount = 0

    #Process each line in input file
    for line in inputFile:
        _lineCount += 1

        #Record the work-location, home-location, #total_jobs data in the respective fields in the txt file
        _wCounty=line[59:61]+line[62:65] #Extracting work county field from cols 63:65
        _hCounty=line[0:2]+line[3:6] #Extracting home county field from cols 4:6
        totalJobs = int(line[117:124]) #Extracting #JTW Flows from cols 118:124

        if (_wCounty or _hCounty) in myCounties.keys():
            #print(_wCounty,_hCounty,totalJobs)
            ctppCCFLows[(_wCounty,_hCounty)]=int(ctppCCFLows.get((_wCounty,_hCounty),0))+int(totalJobs)



#Write Output File
with open(_outputFileCCFlows, 'wb') as outputFile:
    writer = csv.writer(outputFile, delimiter=',')

    print('begining output')
    #Writing headers for the output csv file
    outheaders=['Home County','Work County','Home County Name','Work County Name','No. of Trips','TripType']
    writer.writerow(outheaders)

    for key in ctppCCFLows.keys():
        if(myCounties.get(key[1]) is None and myCounties.get(key[0]) is not None):
            _tType='External-Internal'
        elif(myCounties.get(key[1]) is not None and myCounties.get(key[0]) is None):
            _tType='Internal-External'
        elif(myCounties.get(key[1]) is None and myCounties.get(key[0]) is None):
            _tType='External-External'
        else:
            _tType='Internal-Internal'

        record = [key[1],key[0],myCounties.get(key[1]),myCounties.get(key[0]),ctppCCFLows[key],_tType]
        writer.writerow(record)
        _tType=''

print('All Done! Check the output County-to-County worker flows file...')
