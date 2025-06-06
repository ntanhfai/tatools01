# from ruamel import yaml
# from ruamel.yaml import YAML
# # ruamel.yaml.__version__
# # Out[15]: '0.18.6'
#
import pathlib
import sys
from os.path import exists, join
import os
from datetime import datetime
from os.path import dirname
from pprint import pprint
from pprint import pprint as pp

from ruamel.yaml import YAML

yaml = YAML()
# yaml.indent(offset=4)
yaml.compact(seq_seq=False, seq_map=False)

yml_file_contents = {}


def delkeyVal(mDict, lstmkey):
    for mkey in lstmkey:
        if mkey in mDict:
            del mDict[mkey]
    return mDict

from os.path import join, exists, dirname, basename
class tactParametters:
    def __init__(self, ModuleName="TACT", logdir="", params_dir=""):
        self.ModuleName = ModuleName
        self.logdir = logdir
        self.fn = ""
        self.AppName = ""
        self.params_dir=params_dir

    def to_yaml(self, file_path):
        global yml_file_contents
        if self.AppName:
            pHome = self.params_dir
            file_path = os.path.join(pHome, basename(file_path))
        self.config_file_path = file_path
        with open(file_path, "w", encoding="utf-8") as file:
            # mdict = {self.ModuleName: self.__dict__}
            mDict = self.__dict__.copy()
            mDict = delkeyVal(
                mDict,
                [
                    "ModuleName",
                    "logdir",
                    "fn",
                    "AppName",
                    "saveParam_onlyThis_APP_NAME",
                    "config_file_path",
                    "params_dir"
                ],
            )
            yml_file_contents[self.ModuleName] = mDict
            yaml.dump(yml_file_contents, file)

    def from_yaml(self, file_path):
        global yml_file_contents
        if self.AppName:
            pHome=self.params_dir
            file_path = os.path.join(pHome, basename(file_path))
        if exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                xxx = yaml.load(file)
                if xxx:
                    yml_file_contents = xxx
                if yml_file_contents:
                    if self.ModuleName in yml_file_contents:
                        data = yml_file_contents[self.ModuleName]
                        self.__dict__.update(data)

    def load_then_save_to_yaml( self, file_path, ModuleName=None, flogDict=False , save2file=True):
        if ModuleName:
            self.ModuleName = ModuleName
        self.fn = file_path
        self.from_yaml(file_path)
        if save2file:
            self.to_yaml(file_path)
        if flogDict:
            self.ta_print_log(str(self.__dict__))

    def save_to_yaml_only(self, filepath=None):
        if filepath is not None:
            self.fn = filepath
        self.to_yaml(self.fn)
    def get(self, key, default=None):
        if key in self.__dict__:
            return self.__dict__[key]
        else:
            return default
    @staticmethod
    def fnFIS(mDir, exts=(".jpg", ".jpeg", ".png")):  # mConf.local_log_data_dir_input
        inputTypes_Files = []
        for D, _, F in os.walk(mDir):
            for fn in F:
                if fn.endswith(exts):
                    inputTypes_Files.append(join(D, fn).replace("\\", "/"))
        inputTypes_Files.sort()
        return inputTypes_Files

    def ta_print_log(self, *args):
        logdir = self.logdir
        margs = []
        for x in args:
            try:
                margs.append(str(x))
            except:
                pass
        s = " ".join(margs)
        currTime = datetime.now()
        sDT = currTime.strftime("%m/%d, %H:%M:%S")
        if logdir:
            fn = f"{logdir}/logs/{currTime.year}/{currTime.month}/{currTime.day}/logs.txt"
        else:
            fn = f"logs/{currTime.year}/{currTime.month}/{currTime.day}/logs.txt"
        os.makedirs(dirname(fn), exist_ok=True)
        with open(fn, "a", encoding="utf-8") as ff:
            ff.write(f"{s}\n")
        print(sDT, s)

    # def get_Home_Dir(self,AppName=None):
    #     if not AppName:
    #         AppName = self.AppName
    #     return get_Home_Dir(AppName)


# def get_Home_Dir(AppName=None):
#     if AppName:
#         drive = pathlib.Path.home().drive 
#         folder_path = join(drive, "/RunProgram", AppName).replace("\\", "/")
#         os.makedirs(folder_path, exist_ok=True)
#     return ''
 

if __name__=="__main__":

    # from tatools01.ParamsBase import tactParametters
    APP_NAME='My_Project_Name'

    class Parameters(tactParametters):
        def __init__(self):
            super().__init__(ModuleName="Module 01")
            self.HD =[
                "Chương trình này nhằm xây dựng tham số cho các chương trình khác",
            ]
            self.test1="123"
            self.load_then_save_to_yaml(file_path=f"{APP_NAME}.yml")
            # ===================================================================================================
            self.in_var=1


    mPs = Parameters() 
    mPs.ta_print_log("hello") 
    # from tatools01 import ParamsBase 

 
 
