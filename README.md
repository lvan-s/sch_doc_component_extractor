Project for parsing .schdoc Altium files and extracting components
data into `result.csv` file

For start to use this project you need:
1. Python >= 3.10
2. Copy or download this repo
3. `pip install -r requirements.txt`
4. `python -m sch_doc_parser.main`

For extracting components data from files placed in the `sch_doc_test_files`
you need to use next command
```commandline
python -m sch_doc_parser.main
```

Available options:
* `python main.py -p` or `--path` - custom path to altium .SchDoc files
    ```commandline
    python -m sch_doc_parser.main -p ./path/to/project
    ```
* `python main.py -r` or `--report` - custom path and name for result file

    ```commandline
    python -m sch_doc_parser.main -r ./path/to/my_result.csv
  ```
  
* `python main.py -d` or `--delimiter` - custom delimiter for the generated result file

  ```commandline
    python -m sch_doc_parser.main -d ";"
```
  
If you need install this package you may use next command:
```commandline
pip install git+https://github.com/lvan-s/sch_doc_component_extractor.git
```

