from common.exception import SimpleException
from helper import db_query
DBMODELS = dict()


class ModelType(type):
    def __new__(cls, name, bases, attrs):
        instance = super(ModelType, cls).__new__(cls, name, bases, attrs)
        instance.objects = instance()
        return instance

    def __init__(self, name, bases, attrs):
        if name == 'Model':
            pass
        else:
            DBMODELS[name] = self

        super(ModelType, self).__init__(name, bases, attrs)


def __parse_field_name(str):
    pos = str.find('__')
    if pos == -1:
        return str, None
    else:
        return str[:pos], str[pos:]


def filter_parser(*args, **kwargs):
    args = []
    values = {}
    for field_name, value in kwargs.items():
        field_name, op = __parse_field_name(field_name)
        values[field_name] = value

        if not op:
            args.append(f"{field_name}=:{field_name}")
        else:
            if op == '__not':
                args.append(f"{field_name}!=:{field_name}")
            elif op == '__lt':
                args.append(f"{field_name}<:{field_name}")
            elif op == '__lte':
                args.append(f"{field_name}<=:{field_name}")
            elif op == '__gt':
                args.append(f"{field_name}>:{field_name}")
            elif op == '__gte':
                args.append(f"{field_name}>=:{field_name}")
            elif op == '__notin':
                if len(value) > 0:
                    del values[field_name]
                    keys = []
                    for i, item in enumerate(value):
                        values[f'{field_name}_{i}'] = item
                        keys.append(f':{field_name}_{i}')
                    args.append(f"{field_name} not in ({', '.join(keys)})")
            elif op == '__icontains':
                args.append(f"{field_name} like :{field_name}")
                values[field_name] = f"%{value}%"
            elif op == '__range':
                del values[field_name]
                values[f'{field_name}_0'] = value[0]
                values[f'{field_name}_1'] = value[1]
                args.append(f"{field_name} > :{field_name}_0 and {field_name} < :{field_name}_1")
            elif op == '__in':
                if len(value) == 0:
                    value = ['-98765']
                del values[field_name]
                keys = []
                for i, item in enumerate(value):
                    values[f'{field_name}_{i}'] = item
                    keys.append(f':{field_name}_{i}')
                args.append(f"{field_name} in ({', '.join(keys)})")
    return args, values


class Model(metaclass=ModelType):
    table_name = "model"
    required_fields = []

    def __init__(self):
        self.db_query = db_query

    def create_table(self):
        # demo
        db_query(f"""
                CREATE TABLE IF NOT EXISTS `{self.table_name}` (                                                      
                 `id` bigint(20) NOT NULL AUTO_INCREMENT,
                 `name` varchar(20) NOT NULL DEFAULT "1",
                 `created_at` datetime DEFAULT CURRENT_TIMESTAMP,                                      
                 `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
                 PRIMARY KEY (`id`),                                                                     
                 KEY `id` (`id`)                                               
               ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

    def count(self, *args, **kwargs):
        fileldstr = "count(1) as cnt"
        args, values = filter_parser(*args, **kwargs)
        if args:
            sql = f"""
                select {fileldstr} from {self.table_name} where {' and '.join(args)};
            """
        else:
            sql = f"""
                select {fileldstr} from {self.table_name};
            """
        return db_query(sql, **values).first(as_dict=True)['cnt']

    def find(self, fields=None, sort=None, skip=None, limit=None, *args, **kwargs):
        fileldstr = "*"
        if fields:
            fileldstr = ",".join(fields)
        args, values = filter_parser(*args, **kwargs)
        if args:
            sql = f"""
                select {fileldstr} from {self.table_name} where {' and '.join(args)}
            """
        else:
            sql = f"""
                select {fileldstr} from {self.table_name}
            """
        if sort:
            strsorts = []
            for v in sort:
                if ":" in v:
                    s, seq = v.split(":")
                else:
                    s, seq = v, 'asc'
                if seq not in ['desc', 'asc']:
                    raise SimpleException("error seq")
                strsorts.append(f"`{s}` {seq}")
            sql += f" order by {','.join(strsorts)}"
        if skip is not None and limit is not None:
            sql += f" limit {skip},{limit}"
        return db_query(sql, **values).all(as_dict=True)

    def find_one(self, fields=None, *args, **kwargs):
        fileldstr = "*"
        if fields:
            fileldstr = ",".join(fields)
        args, values = filter_parser(*args, **kwargs)
        if args:
            sql = f"""
                select {fileldstr} from {self.table_name} where {' and '.join(args)};
            """
        else:
            sql = f"""
                select {fileldstr} from {self.table_name};
            """
        return db_query(sql, **values).first(as_dict=True)

    def insert(self, *args, **kwargs):
        if list(set(self.required_fields).difference(set(kwargs.keys()))):
            raise SimpleException("missing params")
        keys = ', '.join(list(map(lambda x: f"`{x}`", kwargs.keys())))
        values = ':' + ', :'.join(kwargs.keys())
        db_query(f"""
        INSERT INTO {self.table_name} ({keys}) VALUES ({values})
        """, **kwargs)

    def update(self, filters, set_data):
        if not filters or not set_data:
            return
        args, values = filter_parser(**filters)
        set_data_str = []
        set_prefix = "set_"
        for k, v in set_data.items():
            set_data_str.append(f"{k}=:{set_prefix}{k}")
            values[f"{set_prefix}{k}"] = v
        return db_query(f"""
        update {self.table_name} set {', '.join(set_data_str)} where {' and '.join(args)}
        """, **values)

    def delete(self, id):
        return db_query(f"""
        DELETE FROM {self.table_name} WHERE id=:id;
        """, id=id)
