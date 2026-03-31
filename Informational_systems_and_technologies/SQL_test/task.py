import sqlite3
import pandas as pd

trade_df = pd.read_csv('csvs/trade.csv')
trade_df.columns = ['trade_ID', 'date', 'shop_ID', 'product_ID', 'trade_type', 'quantity', 'price']
print(trade_df.head())
print("---")
product_df = pd.read_csv('csvs/product.csv')
product_df.columns = ['product_ID', 'product_type', 'product_name', 'measurement', 'amount_in_bag', 'provider']
print(product_df.head())
print("---")
shop_df = pd.read_csv('csvs/shop.csv')
shop_df.columns = ['shop_ID', 'district']
print(shop_df.head())

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `product` (
        `product_ID` integer primary key NOT NULL UNIQUE,
        `product_type` TEXT NOT NULL,
        `product_name` TEXT NOT NULL,
        `measurement` TEXT NOT NULL,
        `amount_in_bag` FLOAT NOT NULL,
        `provider` TEXT NOT NULL
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `shop` (
        `shop_ID` text primary key NOT NULL UNIQUE,
        `district` TEXT NOT NULL
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `trade` (
        `trade_ID` integer primary key NOT NULL UNIQUE,
        `date` TEXT NOT NULL,
        `shop_ID` TEXT NOT NULL,
        `product_ID` INTEGER NOT NULL,
        `trade_type` TEXT NOT NULL,
        `quantity` INTEGER NOT NULL,
        `price` INTEGER NOT NULL,
        FOREIGN KEY(`shop_ID`) REFERENCES `shop`(`shop_ID`),
        FOREIGN KEY(`product_ID`) REFERENCES `product`(`product_ID`)
    );
""")

connection.commit()
'''
product_df.to_sql('product', connection, if_exists = 'append', index = False)
shop_df.to_sql('shop', connection, if_exists = 'append', index = False)
trade_df.to_sql('trade', connection, if_exists = 'append', index = False)

connection.commit()
'''
cursor.execute("""
    SELECT SUM(trade.price * trade.quantity) as total_cost
    FROM trade
    JOIN product ON trade.product_ID = product.product_ID
    JOIN shop ON trade.shop_ID = shop.shop_ID
    WHERE product.product_type = 'Meat delicatessen' AND shop.district = 'Central' AND trade.trade_type = "Out" AND trade.date BETWEEN '07.06.2021' AND '13.06.2021'
""")

summ = cursor.fetchall()
print(summ)
    
cursor.close()
connection.close()