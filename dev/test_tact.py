from pprint import pprint
from tatools01.ParamsBase import tactParametters


# print(ntanh.__version__)
mParams = tactParametters()

fns = mParams.fnFIS(r"../", exts=(".py"))
pprint(fns)

from pprint import pprint
from tatools01.ParamsBase import tactParametters


class Parameters(tactParametters):
    def __init__(self, ModuleName="TACT"):
        super().__init__()
        self.thamso1 = "thamso1"
        self.thamso2 = " xâu tiếng việt"
        self.api_url = "https://200.168.90.38:6699/avi/collect_data"
        self.testpath = "D:/test_debug_fii"
        self.test_real = 0.8
        self.test_int = 12
        self.test_dict = {
            1: 2,
            3: 4.5,
            "6": "bảy nhá",
            -1: "Tám",
            9: [10, 11.2, "22", (33, 44, "55")],
            10: {101: 12, 102: "mười ba"},
        }
        self.test_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        self.load_then_save_to_yaml(file_path="configs_test.yml", ModuleName=ModuleName)
        self.privateVar1 = 2
        self.privateVar2 = "Not in param file"


mParams = Parameters(ModuleName="test")

pprint(mParams.__dict__)
