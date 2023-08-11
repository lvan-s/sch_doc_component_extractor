Project for parsing .schdoc Altium files and extracting components
data into `result.csv` file

For start to use this project you need:
1. Python >= 3.10
2. Copy or download this repo
3. `pip install -r requirements.txt`
4. `python main.py`

For extracting components data from files placed in the `sch_doc_test_files`
you need to use next command
```commandline
python main.py
```

Available options:
* `python main.py -p` or `--path` - custom path to altium .SchDoc files
    ```commandline
    python main.py -p ./path/to/project
    ```
* `python main.py -r` or `--report` - custom path and name for result file

    ```commandline
    python main.py -r ./path/to/my_result.csv
  ```
