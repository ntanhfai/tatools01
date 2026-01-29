import os
from os.path import join, exists, basename
from datetime import datetime
from typing import Any, Optional, List
from ruamel.yaml import YAML
from pprint import pprint as pp

yaml = YAML()
yaml.indent(mapping=4, sequence=4, offset=2)

version = "3.0.7"

class DotDict:
    """Dict có thể truy cập bằng dot notation: obj.key thay vì obj['key']"""
    
    def __init__(self, data: dict = None):
        for key, value in (data or {}).items():
            if isinstance(value, dict):
                setattr(self, key, DotDict(value))
            else:
                setattr(self, key, value)
    
    def __repr__(self):
        return f"DotDict({self.__dict__})"
    
    def to_dict(self) -> dict:
        result = {}
        for k, v in self.__dict__.items():
            if isinstance(v, DotDict):
                result[k] = v.to_dict()
            else:
                result[k] = v
        return result

import os # Set từ đầu chương trình luôn
class TactParameters:
    """Base class để quản lý parameters với YAML persistence."""
    
    _INTERNAL_KEYS = frozenset([
        "ModuleName", "logdir", "fn", "AppName", "DEBUG_MODE",
        "saveParam_onlyThis_APP_NAME", "config_file_path", "params_dir", "pp"
    ])
    
    def __init__(
        self, 
        ModuleName: str = "TACT", 
        logdir: str = "", 
        params_dir: str = "", 
        AppName: str = ""
    ):
        self.ModuleName = ModuleName
        self.logdir = logdir
        self.fn = ""
        self.AppName = AppName
        self.params_dir = params_dir
        self.config_file_path: Optional[str] = None
        
        self.DEBUG_MODE = int(os.getenv("DEBUG_MODE", -1))
        if self.DEBUG_MODE == -1:
            os.environ["DEBUG_MODE"] = "2"

    # ==================== API Keys ====================
    
    def get_Gemini_key(self, file_path: str = None) -> dict:
        file_path = file_path or "D:/taEnv/API_Keys_Gemini.yml"
        return self._read_yaml_safe(file_path)
    
    @staticmethod
    def load_api_keys(file_path: str) -> dict:
        if not exists(file_path):
            return {}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return yaml.load(f) or {}
        except Exception:
            return {}

    # ==================== Core: Serialize to plain Python types ====================
    
    def _to_plain_dict(self, obj: Any) -> Any:
        """
        Chuyển đổi object thành plain Python types (dict, list, scalar).
        Đảm bảo YAML có thể serialize được.
        """
        if obj is None:
            return None
        
        # Scalar types - trả về nguyên
        if isinstance(obj, (str, int, float, bool)):
            return obj
        
        # List/tuple
        if isinstance(obj, (list, tuple)):
            return [self._to_plain_dict(item) for item in obj]
        
        # Dict thường
        if isinstance(obj, dict):
            return {k: self._to_plain_dict(v) for k, v in obj.items()}
        
        # DotDict
        if isinstance(obj, DotDict):
            return self._to_plain_dict(obj.to_dict())
        
        # Nested class instance (như clsMinio)
        if hasattr(obj, '__dict__') and not isinstance(obj, type):
            result = {}
            for key in dir(obj):
                if key.startswith('_'):
                    continue
                value = getattr(obj, key)
                if callable(value):
                    continue
                result[key] = self._to_plain_dict(value)
            return result
        
        # Fallback: convert to string
        return str(obj)

    # ==================== Core: Check if nested class ====================
    
    def _is_nested_class(self, obj: Any) -> bool:
        """Kiểm tra obj có phải là instance của nested class không."""
        if obj is None:
            return False
        if isinstance(obj, (dict, list, tuple, str, int, float, bool, DotDict)):
            return False
        if isinstance(obj, type):
            return False
        return hasattr(obj, '__dict__')

    # ==================== Core: Deep Merge ====================
    
    def _deep_merge(self, default: Any, from_file: Any) -> Any:
        """
        Deep merge: from_file ưu tiên, default bổ sung key thiếu.
        Giữ nguyên TYPE của default.
        """
        # from_file là dict
        if isinstance(from_file, dict):
            # Lấy default dưới dạng dict
            if isinstance(default, dict):
                base = dict(default)  # Copy
                convert_to_dotdict = False
            elif isinstance(default, DotDict):
                base = default.to_dict()
                convert_to_dotdict = True
            elif self._is_nested_class(default):
                base = self._to_plain_dict(default)
                convert_to_dotdict = True
            else:
                base = {}
                convert_to_dotdict = False
            
            # Merge từng key
            for k, v in from_file.items():
                base[k] = self._deep_merge(base.get(k), v)
            
            # Trả về đúng type
            if convert_to_dotdict:
                return DotDict(base)
            else:
                return base
        
        # from_file là list
        elif isinstance(from_file, (list, tuple)):
            return list(from_file)
        
        # from_file là scalar
        else:
            return from_file

    # ==================== YAML Operations ====================
    
    def to_yaml(self, file_path: str) -> None:
        """Lưu parameters của module hiện tại vào file YAML."""
        file_path = self._get_full_file_path(file_path)
        
        # Đọc file hiện tại
        existing_content = self._read_yaml_safe(file_path)
        
        # Chuyển params thành plain dict
        params = self._get_params()
        plain_params = self._to_plain_dict(params)
        
        # Cập nhật module
        existing_content[self.ModuleName] = plain_params
        
        # Ghi file
        self._write_yaml(file_path, existing_content)

    def from_yaml(self, file_path: str) -> None:
        """
        Đọc parameters từ file YAML và merge với default.
        - File có key → dùng giá trị file
        - File không có key → giữ default
        """
        file_path = self._get_full_file_path(file_path)
        data = self._read_yaml_safe(file_path)
        
        if self.ModuleName in data:
            file_data = data[self.ModuleName]
            
            for key, file_value in file_data.items():
                if key in self._INTERNAL_KEYS:
                    continue
                
                default_value = getattr(self, key, None)
                merged = self._deep_merge(default_value, file_value)
                setattr(self, key, merged)

    def load_then_save_to_yaml(
        self, 
        file_path: str, 
        ModuleName: str = None, 
        flogDict: bool = False, 
        save2file: bool = True
    ) -> None:
        """
        Load params từ file (merge với default), sau đó save lại.
        """
        if ModuleName:
            self.ModuleName = ModuleName
        self.fn = file_path
        self.from_yaml(file_path)
        if save2file:
            self.to_yaml(file_path)
        if flogDict:
            self._log(str(self.__dict__))

    def save_to_yaml_only(self, filepath: str = None) -> None:
        """Chỉ save, không load."""
        self.to_yaml(filepath or self.fn)

    # ==================== File Operations ====================
    
    def _read_yaml_safe(self, file_path: str) -> dict:
        """Đọc YAML file an toàn, trả về {} nếu lỗi."""
        if not exists(file_path):
            return {}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = yaml.load(f)
                # Convert ruamel types to plain Python
                return self._to_plain_dict(content) if content else {}
        except Exception as e:
            self.mlog(f"Warning: Cannot read {file_path}: {e}")
            return {}
    
    def _write_yaml(self, file_path: str, content: dict) -> None:
        """Ghi content vào YAML file."""
        dir_path = os.path.dirname(file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(content, f)

    def _get_full_file_path(self, file_path: str) -> str:
        if self.AppName and self.params_dir:
            return join(self.params_dir, basename(file_path))
        return file_path

    # ==================== Utilities ====================
    
    def _get_params(self) -> dict:
        """Lấy params, loại bỏ internal keys."""
        return {k: v for k, v in self.__dict__.items() if k not in self._INTERNAL_KEYS}

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)

    @staticmethod
    def find_files(directory: str, exts: tuple = (".jpg", ".jpeg", ".png")) -> List[str]:
        return sorted(
            join(root, f).replace("\\", "/")
            for root, _, files in os.walk(directory)
            for f in files if f.lower().endswith(exts)
        )

    # ==================== Logging ====================
    
    def _log(self, message: str) -> None:
        self.mlog(message)
    
    # def mlog(self, *args) -> None:
    #     message = " ".join(str(arg) for arg in args)
    #     now = datetime.now()
    #     timestamp = now.strftime("%m/%d, %H:%M:%S")
        
    #     base = self.logdir or "."
    #     log_file = f"{base}/logs/{now.year}/{now.month}/{now.day}/logs.txt"
        
    #     os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
    #     log_line = f"{timestamp} [{self.ModuleName}] {message}"
    #     with open(log_file, "a", encoding="utf-8") as f:
    #         f.write(log_line + "\n")
    #     print(log_line)
    def mlog(self, *args, debug_level: int | None = None) -> None:
        """
        Simple logger with debug level filter

        debug_level:
            0 = CRITICAL
            1 = INFO
            2 = DEBUG
            3 = TRACE (mapped to DEBUG)
            None = default (2)
        """
        # Default level
        if debug_level is None:
            debug_level = 2
            
        # import os # Set từ đầu chương trình luôn
        # os.environ["DEBUG_MODE"] = "3"
        
         
        # Early return (O(1))
        if self.DEBUG_MODE < debug_level:
            return

        message = " ".join(str(arg) for arg in args)

        now = datetime.now()
        timestamp = now.strftime("%m/%d, %H:%M:%S")

        base = self.logdir or "."
        log_file = f"{base}/logs/{now.year}/{now.month}/{now.day}/logs.log"
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        log_line = f"{timestamp} [{self.ModuleName}] {message}"

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_line + "\n")

        print(log_line)
    def getLogfilename(self):
        base = self.logdir or "."
        log_file = f"{base}/logs/{now.year}/{now.month}/{now.day}/logs.log"
        return log_file

# ==================== TEST ====================

if __name__ == "__main__":
    AppName = 'My_Project_Name'
    
    # Xóa file cũ để test sạch
    # if exists(f"{AppName}.yml"):
    #     os.remove(f"{AppName}.yml")
    
    # ========== TEST 1: Params_01 với dict thường ==========
    print("=" * 60)
    print("TEST 1: Params_01 - Scalar, List, Dict thường")
    print("=" * 60)
    
    class Params_01(TactParameters):
        def __init__(self):
            super().__init__(ModuleName="Module 01", params_dir='./')
            self.HD = ["Chương trình này nhằm xây dựng tham số"]
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

    mPs1 = Params_01()
    print(f"test1 = {mPs1.test1}")
    print(f"myDict = {mPs1.myDict}")
    print(f"myDict['key1'] = {mPs1.myDict['key1']}")
    print(f"type(myDict) = {type(mPs1.myDict)}")
    print(f"Multi_types_param = {mPs1.Multi_types_param['list']}")
    assert isinstance(mPs1.myDict, dict), "myDict phải là dict!"
    print("✓ OK")
    
    # Load lại
    print("\n--- Reload Params_01 ---")
    mPs1_reload = Params_01()
    print(f"myDict['key1'] = {mPs1_reload.myDict['key1']}")
    print(f"type(myDict) = {type(mPs1_reload.myDict)}")
    assert isinstance(mPs1_reload.myDict, dict), "myDict phải vẫn là dict sau reload!"
    print("✓ OK")
    
    # ========== TEST 2: Params_02 ==========
    print("\n" + "=" * 60)
    print("TEST 2: Params_02 - Module khác trong cùng file")
    print("=" * 60)
    
    class Params_02(TactParameters):
        def __init__(self):
            super().__init__(ModuleName="Module 02", params_dir='./')
            self.HD = ["Chương trình 02"]
            self.test1 = "456"
            self.test2 = "New param"
            self.in_var = 2
            self.load_then_save_to_yaml(file_path=f"{AppName}.yml")
    
    mPs2 = Params_02()
    print(f"test1 = {mPs2.test1}")
    print(f"test2 = {mPs2.test2}")
    print("✓ OK")
    
    # ========== TEST 3: Params_03 với nested class ==========
    print("\n" + "=" * 60)
    print("TEST 3: Params_03 - Nested class (access bằng dot)")
    print("=" * 60)
    
    class Params_03(TactParameters):
        def __init__(self):
            super().__init__(ModuleName="chatbotAPI", params_dir='./')
            self.HD = ["Chương trình chatbot"]
            
            class clsMinio:
                IP = "192.168.3.42:9000"
                access_key = "admin"
                secret_key = "Proton@2025"
            
            self.Minio = clsMinio()
            self.in_var = 1
            self.load_then_save_to_yaml(file_path=f"{AppName}.yml")

    mPs3 = Params_03()
    print(f"Minio.IP = {mPs3.Minio.IP}")
    print(f"Minio.access_key = {mPs3.Minio.access_key}")
    print(f"Minio.secret_key = {mPs3.Minio.secret_key}")
    print(f"type(Minio) = {type(mPs3.Minio)}")
    print("✓ OK")
    
    # Reload
    print("\n--- Reload Params_03 ---")
    mPs3_reload = Params_03()
    print(f"Minio.IP = {mPs3_reload.Minio.IP}")
    print(f"Minio.access_key = {mPs3_reload.Minio.access_key}")
    print(f"Minio.secret_key = {mPs3_reload.Minio.secret_key}")
    # print(f"abc = {mPs3_reload.abc}")
    print("✓ OK")

    mPs3.mlog("Test log")
    mPs3.mlog("Test log", level="error")
    mPs3.mlog("Test log", level="warning")
    mPs3.mlog("Test log", level="info")
    mPs3.mlog("Test log", level="debug")
    # test mlog nhiều tham số như print
    mPs3.mlog("Test log", level="info", args=[1, 2, 3], kwargs={"a": 1, "b": 2})
    mPs3.mlog("Test log", level="info", args=[1, 2, 3], kwargs={"a": 1, "b": 2}, extra={"extra": "extra"})
    
    
    # # ========== TEST 4: User sửa file YAML ==========
    # print("\n" + "=" * 60)
    # print("TEST 4: User sửa file YAML")
    # print("=" * 60)
    
    # # Đọc file, sửa, ghi lại
    # with open(f"{AppName}.yml", "r", encoding="utf-8") as f:
    #     content = yaml.load(f)
    
    # content['chatbotAPI']['Minio']['IP'] = "10.0.0.1:9000"
    # content['chatbotAPI']['in_var'] = 999
    # content['Module 01']['myDict']['key1'] = "MODIFIED"
    
    # with open(f"{AppName}.yml", "w", encoding="utf-8") as f:
    #     yaml.dump(content, f)
    
    # print("Đã sửa: Minio.IP, in_var, myDict['key1']")
    
    # # Reload và kiểm tra
    # mPs3_mod = Params_03()
    # print(f"Minio.IP = {mPs3_mod.Minio.IP} (expect: 10.0.0.1:9000)")
    # print(f"in_var = {mPs3_mod.in_var} (expect: 999)")
    # assert mPs3_mod.Minio.IP == "10.0.0.1:9000"
    # assert mPs3_mod.in_var == 999
    
    # mPs1_mod = Params_01()
    # print(f"myDict['key1'] = {mPs1_mod.myDict['key1']} (expect: MODIFIED)")
    # assert mPs1_mod.myDict['key1'] == "MODIFIED"
    # print("✓ OK")
    
    # # ========== TEST 5: User xóa key trong file ==========
    # print("\n" + "=" * 60)
    # print("TEST 5: User xóa key trong file → khôi phục từ default")
    # print("=" * 60)
    
    # with open(f"{AppName}.yml", "r", encoding="utf-8") as f:
    #     content = yaml.load(f)
    
    # del content['chatbotAPI']['Minio']['secret_key']  # Xóa key này
    
    # with open(f"{AppName}.yml", "w", encoding="utf-8") as f:
    #     yaml.dump(content, f)
    
    # print("Đã xóa: Minio.secret_key")
    
    # mPs3_del = Params_03()
    # print(f"Minio.IP = {mPs3_del.Minio.IP} (expect: 10.0.0.1:9000 - giữ từ file)")
    # print(f"Minio.secret_key = {mPs3_del.Minio.secret_key} (expect: Proton@2025 - từ default)")
    # assert mPs3_del.Minio.IP == "10.0.0.1:9000"
    # assert mPs3_del.Minio.secret_key == "Proton@2025"
    # print("✓ OK")
    
    # # Kiểm tra file đã được bổ sung key
    # with open(f"{AppName}.yml", "r", encoding="utf-8") as f:
    #     content = yaml.load(f)
    # assert 'secret_key' in content['chatbotAPI']['Minio']
    # print("✓ File đã được bổ sung secret_key")
    
    # # ========== DONE ==========
    # print("\n" + "=" * 60)
    # print("✓ TẤT CẢ TESTS PASSED!")
    # print("=" * 60)
    
    # # In file cuối cùng
    # print("\n--- File YAML cuối cùng ---")
    # with open(f"{AppName}.yml", "r", encoding="utf-8") as f:
    #     print(f.read())