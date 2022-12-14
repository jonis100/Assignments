##############################################################################################################
##                              Answered by: Yoni Shieber Date: 20-21/2/2022                                ## 
##Question 2                                                                                                ##
##    Write a python script that will do the following (Tip – try using regular expression to solve this):  ##
##    1. Read a log file located in /tmp/mylogfile.log                                                      ##
##    2. Go over each line in the log (example for a single line below) and filter according to the         ##
##      following:                                                                                          ##
##          a. If the remote address is in the range 192.168.1.0 – 192.168.10.254 and the HTTP              ##
##              status is 200, print the following information: Time of the request, the URL and            ##
##              the user-agent that was used                                                                ##
##          b. If the request time is higher than 1 second and the request type is POST, print              ##
##              the following information: remote address, URL and request length                           ##
##          c. If the date of the request is 2020-07-01 and the time of the request is between              ##
##              18:00-19:00, print the following information: request time, request length and              ##
##              remote address                                                                              ##
## log line exemple: 2020-07-20T04:16:20+00:00 {{ remote_addr: 192.168.1.100 }}                             ##
##                                              {{ request: GET /app/myurl HTTP/1.1 }}                      ##    
##                                               {{ status: 200 }} {{ body_bytes_sent: 100 }}               ##
##                                               {{ http_user_agent: ELB- HealthChecker/2.0 }}              ##
##                                               {{ http_accept: */* }} {{ request_time: 0.3 }}             ##
##                                               {{ request_length: 145}}      [ALL IN ONE LINE!]           ##                          
##  Output csv file for each section                                                                        ##
##  ****Assuming all lines in log file are as mention above!!****                                           ##
##                                                                                                          ##
##############################################################################################################

import re
import csv

def extract_URL(line):
    url = line.split()[8]
    return url

def extract_remote_address(line):
    remote_address = re.split('}} {{|:', line)[4]
    return remote_address

def extract_request_length(line):
    request_length = re.split('}} {{|:', line)[18]
    return request_length[1:len(request_length)-2]
    
def time_of_request(line):
    temp = line.split()[0]
    time = temp[11:19]
    return time

def HandleAsection(line):
    #check matching section a requers
    match = re.match(".* remote_addr: 192.168.([1-9]|10).*status: 200.*", line)             
    if match:
        #Adding Time_of_the_request
        row_list = [time_of_request(line)] 
        #Adding the URL
        row_list.append (extract_URL(line)) 
        #Adding the user-agent
        user_agent = line.split("}} {{")[4]
        row_list.append (user_agent[18:])
        return row_list
    
def HandleBsection(line):
    #check matching section b requers
    match = re.match(".*request: POST", line)  
    if match:
        request_time = float(re.split('}} {{|:', line)[16])
        if request_time > 1:
            #Adding remote_address
            row_list = ["remote_address", extract_remote_address(line)] 
            #Adding the URL
            row_list.extend (["url", extract_URL(line)])
            #Adding request_length
            row_list.extend (["request_length", extract_request_length(line)])
            return row_list
            


def HandleCsection(line):
    #check matching section c requers
    date = line.split("T")[0]
    timeOfRequest = time_of_request(line)
    if date == "2020-07-01" and timeOfRequest.split(":")[0] == "18": #assuming 18:00-19:00 == 19:00 not included
        #Adding Time_of_the_request
        row_list = [time_of_request(line)]
        #Adding request_length
        row_list.append (extract_request_length(line))
        #Adding remote_address
        row_list.append (extract_remote_address(line))
        return row_list

    


file = open('/tmp/mylogfile.log', 'r')
#file = open('tmp/mylogfile.log.txt', 'r')
lines = file.read().splitlines()
file.close()

with open('Acsv_file.csv', 'w') as Aoutfile, \
     open('Bcsv_file.csv', 'w') as Boutfile, \
     open('Ccsv_file.csv', 'w') as Coutfile:

    print("start filtering")
    writerA = csv.writer(Aoutfile)
    #write titels in Aoutfile
    titles = ["Time_of_the_request", "url", "http_user_agent:"]
    writerA.writerow(titles)
    
    writerB = csv.writer(Boutfile)
    #write titels in Boutfile
    titles = ["remote_address", "url", "request_length" ]
    writerB.writerow(titles)
    
    writerC = csv.writer(Coutfile)
    #write titels in Coutfile
    titles = ["Time_of_the_request", "request_length", "remote_address"]
    writerC.writerow(titles)
    
    for line in lines:
        #checking section a
        A_row = HandleAsection(line)
        if A_row:
#           print (A_row)
           writerA.writerow(A_row)        
        #checking section b    
        B_row = HandleBsection(line)
        if B_row:
#            print (B_row)
            writerB.writerow(B_row)
        #checking section c    
        C_row = HandleCsection(line)
        if C_row:
#            print (C_row)
            writerC.writerow(C_row)    
    print("finished filtering and writed to 'csv_file'")   
