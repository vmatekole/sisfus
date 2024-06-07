import json

from google.api_core.exceptions import ClientError
from google.cloud import bigquery
from google.cloud.bigquery.table import RowIterator, _EmptyRowIterator

from configs.settings import ConfigSettings
from utils import logger

config = ConfigSettings


class Bq:
    def __init__(self, client: bigquery.Client) -> None:
        self._client = client

    def insert_to_bigquery(
        self,
        objs: list[any],
        table_id: str,
        project_id: str = config.gcp_project_id,
        dataset_id: str = config.bq_dataset_id,
    ):
        client = self._client

        table_ref: bigquery.TableReference = bigquery.TableReference(
            bigquery.DatasetReference(project_id, dataset_id), table_id
        )

        table = client.get_table(table_ref)

        rows_to_insert = []
        for obj in objs:
            row: dict[str, Any] = obj.model_dump(exclude_none=True)
            rows_to_insert.append(row)

        # Insert rows into BigQuery table
        errors = client.insert_rows_json(table, rows_to_insert)
        if errors:
            err_msg = f'Errors occurred while inserting rows: {errors}'
            logger.error(err_msg)
            raise Exception(f'Errors occurred while inserting rows: {err_msg}')
        else:
            logger.info(
                f'All {len(objs)} rows of {table_ref.table_id} have been inserted successfully.'
            )
            return True
