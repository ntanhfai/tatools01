"""
tatools01

An python parametters library.
"""

__version__ = "1.0.2" # Nhớ update cả Readme.md

__author__ = "Nguyễn Tuấn Anh - nt.anh.fai@gmail.com"
__credits__ = "MIT License"
__console__ = "tact"
import os
import sys
import argparse
import json
 
   
from . import ParamsBase
from tatools01.Thoi_gian.taTimers import MultiTimer


__help__ = """
"""

def console_main():
    print(
        """
Running: 
1. tact
        """
    )
    
    print("""
from tatools01.ParamsBase import TactParameters
AppName = 'My_Project_Name'
class Parameters(TactParameters):
    def __init__(self):
        super().__init__(ModuleName="Module 01")
        self.HD = ["Chương trình này nhằm xây dựng tham số cho các chương trình khác"]
        self.test1 = "123"             
        self.load_then_save_to_yaml(file_path=f"{AppName}.yml")
        self.in_var = 1
mPs = Parameters()
mPs.mlog("hello")          
          """)

