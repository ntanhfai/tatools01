version = "3.1.0"
def console_main():
    print(
        f"""
ver: {version} - tatools01
1. tact
        """
    )
          

    print("""
from tatools01.ParamsBase import TactParameters
AppName = 'My_Project_Name'
class Params_03(TactParameters):
        def __init__(self):
            super().__init__(ModuleName="chatbotAPI", params_dir='./')
            self.HD = ["Chương trình chatbot"]

            class clsMinio:
                IP = "192.168.3.3:8800"
                access_key = "admin"
                secret_key = "Proton"

            self.Minio = clsMinio()
            self.in_var = 1
            self.load_then_save_to_yaml(file_path=f"{AppName}.yml")

mPs3 = Params_03()
print(f"Minio.IP = {mPs3.Minio.IP}")
print(f"Minio.access_key = {mPs3.Minio.access_key}")
print(f"Minio.secret_key = {mPs3.Minio.secret_key}")
print(f"type(Minio) = {type(mPs3.Minio)}")
print("✓ OK")



class Params_01(TactParameters):
    def __init__(self):
        super().__init__(ModuleName="Module 01", params_dir='./')
        self.HD = ["Chương trình này nhằm xây dựng tham số cho các chương trình khác"]
        self.test1 = "123"
        self.in_var = 1
        self.myList = [1, 2, 3, 4, 5]
        self.myDict = {"key1": "value1", "key2": "value2"}
        self.Multi_types_param = {
            "int": 42,
            "float": 3.14,
            "str": "Hello, World!",
            "list": [1, 2, 3],
            "dict": {"key": "value"},
        }
        self.load_then_save_to_yaml(file_path=f"{AppName}.yml")

# Tạo instance đầu tiên
mPs1 = Params_01()
          """)


