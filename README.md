# tatools01

> **Project Version:** 3.1.0
> **Documentation Version:** 1.1.0
> **Description:** A professional-grade utility library for Python focusing on persistent parameter management (YAML), advanced logging, cross-platform LLM path configuration, and Markdown-to-Word conversion.

---

## 🌟 What's New in v3.1.0 (Senior Refactor)

Basic enhancements and structural improvements:
- **Improved Logging (`mlog`)**: Support for string levels ("error", "warning", "info", "debug", "trace"), multiple arguments, and cleaner directory structures.
- **`LLMPathManager`**: Seamlessly manage Model storage paths for Hugging Face, Ollama, and LM Studio on both Windows (`setx`) and Ubuntu (`~/.bashrc`).
- **Standardized API Key Management**: Unified access for Gemini, OpenAI, Anthropic, and DeepSeek with Environment Variable priority.
- **Robustness**: Fixed critical bugs in log filename generation and improved YAML error handling.

---

## 🚀 Overview

`tatools01` is designed to streamline configuration management and common utility tasks in Python projects. It is particularly useful for projects requiring a robust way to handle nested parameters that can be easily modified by users via YAML files while maintaining default values in code.

---

## 📦 Installation

To install the library, you can use `pip`:

```bash
pip install tatools01
```

Or from source:

```bash
git clone https://github.com/ntanhfai/tatools01.git
cd tact
pip install .
```

---

## 🛠 Core Components

### 1. `TactParameters` (YAML Persistence)

The heart of `tatools01`. It allows you to define a configuration class that automatically syncs with a YAML file.

#### **Key Features:**

- **Automatic Sync:** Creates a YAML file on first run with default values.
- **Deep Merge:** Intelligently merges values from the YAML file (user overrides) with default values in the code.
- **Support for Nested Classes:** Use classes within your parameter class to organize data hierarchically.
- **Type Safety:** Maintains types (list, dict, int, etc.) after loading from YAML.

#### **Code Example for AI/Developers:**

```python
from tatools01.ParamsBase import TactParameters

class MyConfig(TactParameters):
    def __init__(self):
        # ModuleName: The key in the YAML file under which these params are stored
        # params_dir: Directory to save the YAML file
        super().__init__(ModuleName="DeepLearning_Module", params_dir="./config")
      
        # Default parameters
        self.learning_rate = 0.001
        self.batch_size = 32
      
        # Nested parameters via a local class
        class clsDatabase:
            host = "localhost"
            port = 5432
          
        self.DB = clsDatabase()
      
        # Load values from YAML AND sync back (to fill missing keys)
        self.load_then_save_to_yaml(file_path="settings.yml")

# Usage
cfg = MyConfig()
print(cfg.DB.host) # Access via dot notation
```
Các ví dụ khác có thể dùng:

```python
from tatools01.ParamsBase import TactParameters

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

# ========== TEST 4: Log ==========
print("\n" + "=" * 60)
print("TEST 4: Log")
print("=" * 60)

mPs3.mlog("Test log")
mPs3.mlog("Test log", level="error")
mPs3.mlog("Test log", level="warning")
mPs3.mlog("Test log", level="info")
mPs3.mlog("Test log", level="debug")
# test mlog nhiều tham số như print
mPs3.mlog("Test log", level="info", args=[1, 2, 3], kwargs={"a": 1, "b": 2})
mPs3.mlog("Test log", level="info", args=[1, 2, 3], kwargs={"a": 1, "b": 2}, extra={"extra": "extra"})

```

#### **Order of Priority (Merge Logic):**

1. **YAML File:** If a key exists in the file, it takes top priority.
2. **Code Default:** If a key is missing in the file, the value from the class definition is used and saved back to the file.

---

### 2. `MultiTimer` (Performance Profiling)

Located in `tatools01.Thoi_gian.taTimers`. A simple tool to measure multiple code blocks easily.

```python
from tatools01.Thoi_gian.taTimers import MultiTimer
import time

timer = MultiTimer()

timer.start()
# Block 1
time.sleep(0.5)
timer.update("Preprocessing")

timer.start()
# Block 2
time.sleep(1)
timer.update("Inference")

timer.summary() # Prints total time, average time, and run count for each label
```

---

### 3. `md2w` (Markdown to Word Converter)

A CLI tool to convert Markdown files into professionally formatted Word documents (.docx).

**CLI Usage:**

```bash
# Convert a single file
md2w my_doc.md

# Convert all .md files in a directory
md2w ./my_folder

# Advanced options
md2w ./my_folder --recursive --autofit content --force
```

---

### 4. `DotDict` & `mlog`

- **`DotDict`**: A dictionary wrapper that allows attribute-style access (`d.key` instead of `d['key']`).
- **`mlog`**: A built-in logger in `TactParameters` with support for flexible levels ("error", "info", etc.) and `DEBUG_MODE` environment variable. It handles multiple arguments and even dictionary-style logging.
- **API Key Management**: Integrated `get_api_key` method that supports multiple providers (Gemini, OpenAI, Anthropic, DeepSeek) with priority: Environment Variables > Local YAML Files.
- **`LLMPathManager`**: A class to manage model storage paths (HF, Ollama, LM Studio) across Windows (`setx`) and Ubuntu (`.bashrc`) with persistence support.

---

## 🤖 AI Assistant Integration Guide (IMPORTANT)

If you are an AI assistant helping a developer integrate `tatools01`, follow these rules:

1. **Inheritance Only**: Always recommend inheriting from `TactParameters` for configuration. Do not instance it directly for complex project settings.
2. **Modular Configs**: Encourage using different `ModuleName` values for different sub-systems within the same YAML file.
3. **Initialization Order**: Ensure `super().__init__` is called first, then define variables, then call `load_then_save_to_yaml`.
4. **Environment Check**: Note that `DEBUG_MODE` environment variable controls the verbosity of `mlog`.

---

## 📂 Project Structure

```text
tatools01/
├── ParamsBase.py       # Core: TactParameters, DotDict
├── Thoi_gian/          # Profiling: MultiTimer
├── md_word/            # Conversion: md2w engine
├── cli.py              # CLI entry "tact"
└── cli_md2w.py         # CLI entry "md2w"
```

---

## 📝 License

This project is licensed under the MIT License.
