import config

from google.cloud import bigquery
from pathlib import Path


Path = Path('..')


def main():
    client = bigquery.Client.from_service_account_json(config.SERVICE_ACCOUNT_JSON)
    # set table_id to the ID of the table to create
    table_id = config.DATASET + ".table_py"

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField('Title', 'STRING'),
            bigquery.SchemaField('Author', 'STRING'),
            bigquery.SchemaField('Book', 'STRING'),
            bigquery.SchemaField('Subject', 'STRING'),
            bigquery.SchemaField('Date', 'INTEGER'),
            bigquery.SchemaField('Created', 'INTEGER'),
            bigquery.SchemaField('Description_Abstract', 'STRING'),
            bigquery.SchemaField('firstpage', 'STRING'),
            bigquery.SchemaField('lastpage', 'STRING')
        ],
        source_format=bigquery.SourceFormat.CSV,
        autodetect=True,
    )

    file_path = str(Path) + '/practice_BQ/row_data.csv'
    source_file = open(file_path, "rb")
    job = client.load_table_from_file(
        source_file, table_id,
        job_config=job_config
        )

    job.result()

    table = client.get_table(table_id)

    print(
        "Loaded {} rows to {}".format(
            table.num_rows, table_id
        )
    )


if __name__ == "__main__":
    main()
