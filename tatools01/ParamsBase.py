import os
# import pathlib
from os.path import join, exists, basename
from datetime import datetime
from ruamel.yaml import YAML

yaml = YAML()
yaml.compact(seq_seq=False, seq_map=False)

class TactParameters:
    def __init__(self, ModuleName="TACT", logdir="", params_dir=""):
        self.ModuleName = ModuleName
        self.logdir = logdir
        self.fn = ""
        self.AppName = ""
        self.params_dir = params_dir
        self.config_file_path = None

    def to_yaml(self, file_path):
        file_path = self._get_full_file_path(file_path)
        with open(file_path, "w", encoding="utf-8") as file:
            yml_content = {self.ModuleName: self._clean_dict(self.__dict__)}
            yaml.dump(yml_content, file)

    def from_yaml(self, file_path):
        file_path = self._get_full_file_path(file_path)
        if exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                data = yaml.load(file)
                if self.ModuleName in data:
                    self.__dict__.update(data[self.ModuleName])

    def load_then_save_to_yaml(self, file_path, ModuleName=None, flogDict=False, save2file=True):
        if ModuleName:
            self.ModuleName = ModuleName
        self.fn = file_path
        self.from_yaml(file_path)
        if save2file:
            self.to_yaml(file_path)
        if flogDict:
            self._log(str(self.__dict__))

    def save_to_yaml_only(self, filepath=None):
        if filepath is not None:
            self.fn = filepath
        self.to_yaml(self.fn)

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    @staticmethod
    def find_files(mDir, exts=(".jpg", ".jpeg", ".png")):
        return sorted(
            [join(D, fn).replace("\\", "/") for D, _, F in os.walk(mDir) for fn in F if fn.endswith(exts)]
        )

    def _get_full_file_path(self, file_path):
        if self.AppName and self.params_dir:
            return os.path.join(self.params_dir, basename(file_path))
        return file_path

    def _clean_dict(self, input_dict):
        keys_to_remove = [
            "ModuleName", "logdir", "fn", "AppName", "saveParam_onlyThis_APP_NAME", "config_file_path", "params_dir"
        ]
        return {k: v for k, v in input_dict.items() if k not in keys_to_remove}

    def mlog(self, *args):
        logdir = self.logdir
        message = " ".join([str(arg) for arg in args])
        currTime = datetime.now()
        sDT = currTime.strftime("%m/%d, %H:%M:%S")
        log_file = f"{logdir}/logs/{currTime.year}/{currTime.month}/{currTime.day}/logs.txt" if logdir else f"logs/{currTime.year}/{currTime.month}/{currTime.day}/logs.txt"
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, "a", encoding="utf-8") as log:
            log.write(f"{sDT} [{self.ModuleName}] {message}\n")
        print(f"{sDT} [{self.ModuleName}] {message}\n")



if __name__ == "__main__":
    # from tatools01.ParamsBase import TactParameters
    AppName = 'My_Project_Name'
    class Parameters(TactParameters):
        def __init__(self):
            super().__init__(ModuleName="Module 01", params_dir='./' )
            self.HD = ["Chương trình này nhằm xây dựng tham số cho các chương trình khác"]
            self.test1 = "123"             
            self.load_then_save_to_yaml(file_path=f"{AppName}.yml")
            self.in_var = 1
    mPs = Parameters()
    mPs.mlog("hello")
    print(mPs.test1)
