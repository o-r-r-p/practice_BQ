# practice_BQ
## Directory Tree Structure
![Directory Tree Structure](/.images/directory.jpg)

Please place pdf files you want to process under the pdf directory

## Set environment
```
git clone https://github.com/o-r-r-p/practice_BQ.git
cd practice_BQ
poetry install
poetry shell
```

## Upload csv file to your bucket
`python csv_to_bucket.py --project <your project> --bucket <your bucket> --storage <your storage name>`

### Required arguments
**--project**
Your project name.

**--bucket**
Your bucket name.

**--storage**
Your storage name.

## Create table
`python create_table.py`

※ Before you exexted this command, you need to change some variables (SURVICE_ACCOUNT_JSON, table_id, file_path). I will modify there to use arguments.