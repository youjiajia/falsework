from model import Model
from helper import db_query


class BusinessApp(Model):
    table_name = "business_app"

    def create_table(self):
        db_query(f"""
                CREATE TABLE IF NOT EXISTS `{self.table_name}` (                                                      
                 `id` bigint(20) NOT NULL AUTO_INCREMENT,
                 `created_at` datetime DEFAULT CURRENT_TIMESTAMP,                                      
                 `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
                 `name` varchar(256) NOT NULL DEFAULT '' COMMENT '业务应用名',
                 `code` varchar(32) NOT NULL DEFAULT '' COMMENT '业务应用code',
                 `session_token` varchar(128) NOT NULL DEFAULT '' COMMENT '业务应用token',
                 `secret_key` varchar(128) NOT NULL DEFAULT '' COMMENT '业务应用秘钥',
                 PRIMARY KEY (`id`),                                                                     
                 KEY `id` (`id`),                                                               
                 KEY `code` (`code`),                                                                 
                 KEY `session_token` (`session_token`)
               ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
