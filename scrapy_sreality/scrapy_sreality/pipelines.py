import logging
import os
import time

import psycopg2


class ScrapySrealityPipeline:
    def process_item(self, item, spider):
        return item

    def __init__(self):
        # get env variables
        dbname = os.environ.get('DB_NAME')
        user = os.environ.get('DB_USER')
        password = os.environ.get('DB_PASSWORD')
        host = os.environ.get('DB_HOST')
        port = os.environ.get('DB_PORT')
        # wait until db is up
        while True:
            try:
                self.conn = psycopg2.connect(
                    dbname=dbname, user=user, password=password, host=host, port=port
                )
            except:
                logging.error('Unable to reach db. Retrying in 5s...')
                time.sleep(5)
                continue
            break
        # create tables if not exist
        self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = self.conn.cursor()
        self.cur.execute("""
                        CREATE TABLE IF NOT EXISTS apartments (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(100)
                        );
                        
                        CREATE TABLE IF NOT EXISTS apartments_images (
                            apartment_id INTEGER,
                            FOREIGN KEY(apartment_id)
	                        REFERENCES apartments(id),
                            image VARCHAR(100)
                        )
                        
                    """)
        self.conn.commit()

    def process_item(self, item, spider):
        '''
        Insert item into db
        :param item: is dict with keys name and value (list of images)
        :param spider: spider that is running
        :return: item
        '''
        name = item['name']
        self.cur.execute("""
            INSERT INTO apartments (name) VALUES (%s)
        """, (name,))
        # get id of inserted name
        self.cur.execute("""
            SELECT MAX(id) FROM apartments WHERE name = %s
        """, (name,))
        apartment_id = self.cur.fetchone()[0]

        images = item['images']
        # insert multiple images
        for image in images:
            self.cur.execute("""
                INSERT INTO apartments_images (apartment_id, image) VALUES (%s, %s)
            """, (apartment_id, image))

        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
