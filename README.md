# tatools01

> **Project Version:** 3.0.7
> **Documentation Version:** 1.0.0
> **Description:** A utility library for Python focusing on persistent parameter management (YAML), performance profiling, and Markdown-to-Word conversion.

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
- **`mlog`**: A built-in logger in `TactParameters` with support for `DEBUG_MODE` environment variable levels (0: Critical, 1: Info, 2: Debug, 3: Trace).

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
