from sqlglot import parse_one, exp

class SQLSchemaValidator:
    def __init__(self, schema: dict[str, list[str]]):
        self.schema = schema

    def validate(self, sql: str):
        try:
            tree = parse_one(sql, read="sqlite")
        except Exception as e:
            raise ValueError(f"SQL parsing failed: {str(e)}")

        self._validate_tables(tree)
        self._validate_columns(tree)

    def _validate_tables(self, tree):
        tables = {t.name for t in tree.find_all(exp.Table)}

        for table in tables:
            if table not in self.schema:
                raise ValueError(f"Unknown table: {table}")

    def _validate_columns(self, tree):
        
        if list(tree.find_all(exp.Star)):
            return

        columns = list(tree.find_all(exp.Column))

        for col in columns:
            col_name = col.name
            
            if not any(col_name in cols for cols in self.schema.values()):
                    raise ValueError(f"Unknown column: {col_name}")
