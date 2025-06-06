class BaseParams:
    def to_dict(self):
        # Trả về dictionary của các thuộc tính của class cha (BaseParams)
        return self.__dict__.copy()


class Params1(BaseParams):
    def __init__(self):
        self.param1 = "value1"
        self.param2 = "value2"

    def to_dict(self):
        # Kế thừa thuộc tính từ BaseParams và lưu các thuộc tính của Params1
        return self.__dict__.copy()


class Params2(BaseParams):
    def __init__(self):
        self.param3 = "value3"
        self.param4 = "value4"

    def to_dict(self):
        # Kế thừa thuộc tính từ BaseParams và lưu các thuộc tính của Params2
        return self.__dict__.copy()


params1 = Params1()
params2 = Params2()

print(params1.to_dict())  # Kết quả sẽ là {'param1': 'value1', 'param2': 'value2'}
print(params2.to_dict())  # Kết quả sẽ là {'param3': 'value3', 'param4': 'value4'}
