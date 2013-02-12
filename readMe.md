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