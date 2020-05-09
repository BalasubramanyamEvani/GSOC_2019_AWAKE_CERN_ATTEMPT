#!/usr/bin/env python3

## Author@ Balasubramanyam Evani
## mail_id : balasubramanyam.evani@gmail.com
## mail file

from tasks import *

file_name = '../1541962108935000000_167_838.h5'
image = "/AwakeEventData/XMPP-STREAK/StreakImage/streakImageData"
height = "/AwakeEventData/XMPP-STREAK/StreakImage/streakImageHeight" 
width = "/AwakeEventData/XMPP-STREAK/StreakImage/streakImageWidth" 

print('\n ----------------------------- \n')
print('Execution of Task 1')

test_1 = task_1(file_name)
utc = test_1.get_UTC_Time()
cern = test_1.get_CERN_Time()
print("UTC TIME: ",utc)
print("CERN TIME: ",cern)

print('\n ----------------------------- \n')
print('Execution of Task 2')

sort_records = False
dst = '../out'
test_2  = task_2(file_name)
test_2.traverse_and_save(dst,sort_records)


print("\n ------------------------------ \n")
print('Execution of Task 3')

kernel = 3
test_3 = task_3(file_name,image,width,height)
test_3.filter_plot_save(kernel,dst)

print("\n")