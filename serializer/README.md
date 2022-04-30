# About Serializer
```
usage: serializer.py [-h] [-s SOURCE] [-f FORMAT] [-r RESULT_FILE]

options:
  -h, --help            Show this help message and exit
  -s SOURCE, --source   Path to source file
  -f FORMAT, --format   Final format: json, toml or yaml
  -r RESULT_FILE, --result-file
                        Path to file to save result.
```

Usage example
```
python serializer.py -r example\test_result.yaml -s example\test_module_func.json -f yaml
```
