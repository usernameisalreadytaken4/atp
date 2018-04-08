from flask_restful import Resource, reqparse
from models.sql_con import SQLConnect
from sqlalchemy import create_engine, Table, MetaData
from flask import jsonify


class TableAPI(Resource):
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('api_key', type=str)
        parser.add_argument('conn_string', type=str)
        parser.add_argument('host', type=str)
        parser.add_argument('port', type=str)
        parser.add_argument('login', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('db_name', type=str)
        conn_string = SQLConnect(**parser.parse_args())
        SQLALCHEMY_DATABASE_URI = conn_string.make_conn_string()

        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        conn = engine.connect()

        result = conn.execute(
            "select * from pg_tables where schemaname='public';"
        )
        tables_data = []
        table_names = []
        for row in result:
            table_names.append(row._row[1])

        for table_name in table_names:
            md = MetaData()
            table = Table(table_name, md, autoload=True, autoload_with=conn)

            single_table_data = {'name': table_name}

            indexes = [] # хз как прикрутить, нужна база на поискать

            primary_key = {}
            if table.primary_key:
                primary_key.update({'name': table.primary_key.name, 'columns': [col.name for col in table.primary_key.columns]})
            single_table_data.update({'primary_key': primary_key})

            constrains = []
            for constrain in table.constraints:

                ref_table = []
                ref_col = []
                expression = []  # с экспрессиями у меня возникла заминка к сожалению.
                #  возможно надо немного менять структуру извлечения ограничений

                for column in constrain.columns:
                    if hasattr(column, 'base_columns'):
                        for b_column in column.base_columns:
                            try:
                                for key in b_column.foreign_keys:
                                    ref_table.append(key.column.table.name)
                            except:
                                pass
                            try:
                                for key in b_column.foreign_keys:
                                    ref_col.append(key.column.name)
                            except:
                                pass

                constrains.append(
                    {
                        'name': constrain.name,
                        'type': type(constrain).__name__,
                        'constr_key': [col.name for col in constrain.columns],
                        'ref_table': ref_table,
                        'ref_col': ref_col,
                        'expression': '' or None
                    }
                )
            single_table_data.update({'constraints': constrains})

            column_names = []
            for column in table.columns:
                column_names.append({'name': column.name, 'type': type(column.type).__name__})

            single_table_data.update({'columns': column_names})

            tables_data.append(single_table_data)

        conn.close()
        return jsonify(tables_data)


