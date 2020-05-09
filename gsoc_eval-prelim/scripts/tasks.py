#!/usr/bin/env python3

## Author@ Balasubramanyam Evani
## mail_id : balasubramanyam.evani@gmail.com
## helper library for CERN evaluation task

import h5py
import pandas as pd
from scipy import signal
import numpy as np
from matplotlib import pyplot as plt
import os
from datetime import datetime
import pytz

class task_1(object):
    
    def __init__(self,file_name):
        '''
        Get the timestamp from file name and converting into nanoseconds
        '''
        self.unix_time  = file_name.split("/")[1].split(".")[0].split("_")[0]
        self.unix_time = float(self.unix_time)/(10**9)
        print("UNIX timestamp: ",self.unix_time)

    def get_UTC_Time(self):
        '''
        method for conversion of UNIX timestamp -> UTC time
        '''
        utc = pytz.utc
        self.utc = utc.localize(datetime.fromtimestamp(self.unix_time))
        return self.utc

    def get_CERN_Time(self):
        '''
        method for conversion of UTC time to CERN time
        '''
        tz_cern = pytz.timezone('Europe/Zurich')
        return self.utc.astimezone(tz_cern)

class task_2(object):

    def __init__(self,file_name):
        '''
        initialize storing array and get hdf5 file
        '''
        self.mat = []
        self.file_name = file_name

    def recurr(self,h,root=''):
        '''
        goes down the tree structure and recurrs back
        '''
        for key in h.keys():
            
            item = h[key]
            path = root+'/'+str(key)
            
            if isinstance(item, h5py.Dataset): # checks whether instance is dataset
                try:
                    data_type = item.dtype
                except Exception as error:
                    data_type = str(error)
                self.mat.append([path,'dataset',item.size,item.shape,data_type])
            
            elif isinstance(item, h5py.Group): # checks whether instance is group
                self.mat.append([path,'group','n/a','n/a','n/a'])
                self.recurr(item, path) 

    def traverse_and_save(self,dst,sort):
        '''
        open the file and traverse
        dst -> destination folder where csv will be saved
        sort -> True: saves csv with groups first and then datasets
                False: saves in the order the groups and datasets are read
        '''

        print('---- traversing the provided file ----')

        with h5py.File(self.file_name, 'r') as f:
            self.recurr(f)

        '''
        root group and indexes of columns
        '''
        cols = ['Name','Record Type','Dataset Size','Dataset Shape','Dataset dtype'];
        df_root = pd.DataFrame([['/','root_group','n/a','n/a','n/a']],columns=cols)
        df = pd.DataFrame(self.mat,columns=cols)
        
        df_final = pd.concat([df_root,df])
        if sort is True: # checking if dst exists or not
            df_final = df_final.sort_values(['Record Type'],ascending=False)

        if not os.path.exists(dst):
            os.makedirs(dst)
        
        '''
        saving the dataframe to csv format
        '''

        df_final.to_csv(dst+'/task2.csv',index=False)
        print('--- CSV Created ! ---')

class task_3(object):
    
    def __init__(self,file,image_file,width_file,height_file):
        
        '''
        Reading hdf5 file and image datasets
        ''' 

        f = h5py.File(file,'r')

        print('--- loading image data -----')

        self.image_name = image_file
        self.image = f[image_file][:]
        self.width_data = f[width_file][0]
        self.height_data = f[height_file][0]  

    def filter_plot_save(self,kernel,dst):

        '''
        methods filters and saves the resulting images
        kernel -> window size for median filtering
        dst -> destination folder where the image will be saved
        '''

        self.image = np.reshape(self.image , (self.height_data,self.width_data)) # reshaping the image
        self.image_filt = signal.medfilt(self.image,kernel) # applying median filter with kernel
        
        plt.title(self.image_name) # title of plot
        plt.imshow(self.image_filt)
        plt.axis('off')	# switching off axis

        if not os.path.exists(dst): # checking dst exist or not
            os.makedirs(dst)

        plt.savefig(dst+'/streakImage.png',dpi=100,bbox_inches='tight') # saving the final image
        print('--- Figure Saved ! ---')
        plt.show() # showing the saved image