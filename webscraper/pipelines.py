# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import boto3
import psycopg2

class WebscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()

        for field_name in field_names:
            value = adapter.get(field_name)
            adapter[field_name] = value.strip()

            value = adapter.get(field_name)

            if(field_name == 'start_date' or field_name == 'end_date'):
                adapter[field_name] = value[:-2]

            if(field_name == 'serial'):
                adapter['serial'] = value.split('-')[-1].strip()
            
            if(field_name == 'city'):
                adapter[field_name] = value.split(',')[0].strip()

        return item

class SaveToDynamoDBPipeline:
    def __init__(self):
        self.dynamo = boto3.client('dynamodb')

    def process_item(self, item, spider):
        self.response = self.dynamo.put_item(
            TableName = 'conferences-table',
            Item = {
                'serial': {'S': item['serial']},
                'title': {'S': item['title']},
                'organizer': {'S': item['organizer']},
                'start_date': {'S': item['start_date']},
                'end_date': {'S': item['end_date']},
                'proposal_deadline': {'S': item['proposal_deadline']},
                'city': {'S': item['city']},
                'nation': {'S': item['nation']},
                'link': {'S': item['link']}
            }
        )

        return item

class SaveToPostgresPipeline:
    def __init__(self):
        #Connection details        
        hostname = 'localhost'
        username = 'postgres'
        password = 'Jimmy1704'
        database = 'data_engineering'

        #Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username,
                                        password=password, dbname=database )
        
        #Create cursor to execute commands
        self.cursor = self.connection.cursor()

        #Create table 'Conference' if not existed
        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS conferences (
                    id integer PRIMARY KEY,
                    title varchar(200) NOT NULL,
                    organizer varchar(200),
                    start_date date,
                    end_date date,
                    proposal_deadline date,
                    city varchar(100),
                    nation varchar(100),
                    official_link varchar(200))
            """
        )

    def process_item(self, item, spider):
        #Define insert statement
        self.cursor.execute(
            """
            INSERT INTO conferences
            (
                id, title, organizer, start_date, end_date, proposal_deadline, city, nation, official_link
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                item['serial'],
                item['title'],
                item['organizer'],
                item['start_date'],
                item['end_date'],
                item['proposal_deadline'],
                item['city'],
                item['nation'],
                item['link']
            )
        )

        #Execute the insert statement
        self.connection.commit()

        return item
    
    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()
        