# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter
import mysql.connector
import logging
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class ScrapyprojectPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='pavan@1234567',
                database='mydata'
            )
            self.curr = self.conn.cursor()
            logging.info("Connected to MySQL database successfully")
        except mysql.connector.Error as e:
            logging.error("Error connecting to MySQL database: %s", e)

    def create_table(self):
        try:
            self.curr.execute("DROP TABLE IF EXISTS quotes_tb")
            self.curr.execute("""CREATE TABLE quotes_tb ( 
                                 id INT AUTO_INCREMENT PRIMARY KEY,
                                 product_name TEXT,
                                 product_price FLOAT,
                                 timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
            logging.info("Table 'quotes_tb' created successfully")
        except mysql.connector.Error as e:
            logging.error("Error creating table: %s", e)

    def process_item(self, item, spider):
        try:
            self.storedb(item)
            self.check_and_send_notification(item)
            logging.info("Item stored in database successfully: %s", item)
        except Exception as e:
            logging.error("Error storing item in database: %s", e)
        return item

    def storedb(self, item):
        product_names = item.get("product_name", [])
        product_prices = item.get("product_price", [])

        # Ensure that product_prices is always a list
        if not isinstance(product_prices, list):
            product_prices = [product_prices]

        for product_name, product_price in zip(product_names, product_prices):
            try:
                # Remove commas from product_price string and convert to float
                product_price = float(product_price.replace(',', ''))
                self.curr.execute("""INSERT INTO quotes_tb (product_name, product_price) VALUES (%s, %s)""",
                                  (product_name, product_price))
            except mysql.connector.Error as e:
                logging.error("Error executing SQL query: %s", e)
        self.conn.commit()

    def retrieve_product_from_db(self, product_id):
        try:
            # Construct SQL query
            query = "SELECT * FROM quotes_tb WHERE id = %s"
            self.curr.execute(query, (product_id,))

            # Fetch data
            result = self.curr.fetchone()
            if result:
                return result  # Return the product details
            else:
                logging.error("Product with id %s not found", product_id)
                return None
        except mysql.connector.Error as e:
            logging.error("Error retrieving product from MySQL:", e)

    def check_and_send_notification(self, item):
        threshold_price = 30000
        product_id = 2  # Retrieve product with id 2

        # Retrieve product from the database
        product = self.retrieve_product_from_db(product_id)
        if product:
            product_name, product_price = product[1], product[2]
            if product_price < threshold_price:
                self.send_notification(product_name)

    def send_notification(self, product_name):
        # Email configuration
        email_host = 'smtp.gmail.com'
        email_port = 587
        email_username = 'pavankumarm1908@gmail.com'
        email_password = 'qslkcivjxwupwkue'
        recipient_email = 'navapmaruk45.34@gmail.com'
        # Email content
        subject = 'Product Price Notification'
        body = f'The price of product "{product_name}" has reached the threshold.'

        # Create message
        msg = MIMEMultipart()
        msg['From'] = email_username
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Connect to SMTP server and send email
        try:
            with smtplib.SMTP(email_host, email_port) as server:
                server.starttls()
                server.login(email_username, email_password)
                server.send_message(msg)
                logging.info("Notification email sent successfully")
        except Exception as e:
            logging.error("Error sending notification email: %s", e)