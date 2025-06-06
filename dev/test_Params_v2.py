import yaml


class BaseParams:
    def to_dict(self):
        # Trả về dictionary của các thuộc tính của class cha (BaseParams)
        return self.__dict__.copy()

    def from_dict(self, data):
        # Cập nhật các thuộc tính từ dictionary vào đối tượng
        for key, value in data.items():
            setattr(self, key, value)

    def save_to_yaml(self, file_path):
        # Lưu dữ liệu vào file YAML
        with open(file_path, "w") as file:
            yaml.dump(self.to_dict(), file)

    def load_from_yaml(self, file_path):
        # Đọc dữ liệu từ file YAML và cập nhật vào đối tượng
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
            self.from_dict(data)


class Params1(BaseParams):
    def __init__(self):
        self.param1 = "value1"
        self.param2 = "value2"


class Params2(BaseParams):
    def __init__(self):
        self.param3 = "value3"
        self.param4 = "value4"

params1 = Params1()
params1.param1 = "new_value1"  # Thay đổi giá trị thuộc tính

# Lưu params1 ra file YAML
params1.save_to_yaml("params1.yaml")

# Tạo một đối tượng mới và đọc dữ liệu từ file YAML
params1_loaded = Params1()
params1_loaded.load_from_yaml("params1.yaml")

# Kiểm tra xem các thuộc tính đã được cập nhật chưa
print(
    params1_loaded.to_dict()
)  # Kết quả sẽ là {'param1': 'new_value1', 'param2': 'value2'}


params2 = Params2()
params2.param1 = "new_value2"  # Thay đổi giá trị thuộc tính

# Lưu params1 ra file YAML
params2.save_to_yaml("params2.yaml")

# Tạo một đối tượng mới và đọc dữ liệu từ file YAML
params2_loaded = Params2()
params2_loaded.load_from_yaml("params2.yaml")

# Kiểm tra xem các thuộc tính đã được cập nhật chưa
print(
    params2_loaded.to_dict()
)  # Kết quả sẽ là {'param1': 'new_value1', 'param2': 'value2'}
