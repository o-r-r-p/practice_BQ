import argparse
import csv
import logging
import os
from google.cloud import storage
from pathlib import Path

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser


def pdf_to_paper_info_list(pdf_files: list) -> list:
    """generate list of papers info.
    Args:
    pdf_files: list of file paths.
    Return:
    paper_info_list: list of papers info"""
    papers_info_list = []
    for pdf_file in pdf_files:
        fp = open(pdf_file, "rb")
        # PDFParserオブジェクトの取得
        parser = PDFParser(fp)

        # PDFDocumentオブジェクトの取得
        doc = PDFDocument(parser)
        extract_list = []
        for value in extract_value:
            try:
                extract_list.append(doc.info[0][value].decode())
            except KeyError:
                break

        if len(extract_list) == len(extract_value):
            papers_info_list.append(extract_list)
            logging.info(f"{pdf_file} is done!")
        else:
            logging.warning(f'{pdf_file} is no info')

    return papers_info_list


def papers_info_list_to_csv(papers_info_list: list) -> None:
    """generate csv file to transfer gcp bucket
    Args:
    papers_info_list: list of papers info
    Return:
    None"""
    f = open("row_data.csv", "w", newline='')
    writer = csv.writer(f)
    writer.writerows(papers_info_list)
    f.close()


def upload_blob(
    project_name: str, bucket_name: str, source_file_name: Path,
    destination_blob_name: str
) -> None:
    """Uploads a file to the bucket.
    Args:
    bucket_name: your bucket name
    source_file_name: file path to upload bucket
    destination_blob_name = storage object name
    """
    storage_client = storage.Client(project_name)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, type=str)
    parser.add_argument("--bucket", required=True, type=str)
    parser.add_argument("--storage", required=True, type=str)
    args = parser.parse_args()

    path = Path('.')
    pdf_files = list(path.glob("./pdf/*.pdf"))
    logging.basicConfig(
        filename="no_info_papers.log", filemode="w"
        )

    extract_value = [
        'Title', 'Author', 'Book', 'Subject', 'Date', 'Created',
        'Description-Abstract', 'firstpage', 'lastpage'
        ]

    papers_info_list = pdf_to_paper_info_list(pdf_files)

    papers_info_list_to_csv(papers_info_list=papers_info_list)

    if os.path.isfile("./row_data.csv"):
        upload_blob(
            project_name=args.project, bucket_name=args.bucket,
            source_file_name="./row_data.csv",
            destination_blob_name=args.storage
            )
    else:
        raise Exception
