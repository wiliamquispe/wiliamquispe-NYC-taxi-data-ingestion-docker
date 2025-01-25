#!/usr/bin/env python
# coding: utf-8

import os
import argparse
import pandas as pd
from sqlalchemy import create_engine
from time import time

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    database = params.database
    table_name = params.table_name
    url = params.url
    csv_name = 'output.csv.gz'
    
    os.system(f'wget {url} -O {csv_name}')
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    df = next(df_iter)

    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    df['VendorID'] = df['VendorID'].astype('Int64')

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:
        try:
            t_start = time()
            
            df = next(df_iter)
            df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
            df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
            df['VendorID'] = df['VendorID'].astype('Int64')
            
            df.to_sql(name=table_name, con=engine, if_exists='append')
            
            t_end = time()
            
            print('inserted another chunk...., took %.3f seconds' % (t_end - t_start))
        except StopIteration:
            print('finished inserting all chunks')
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', type=str, help='username for postgres')
    parser.add_argument('--password', type=str, help='password for postgres')
    parser.add_argument('--host', type=str, help='host for postgres')
    parser.add_argument('--port', type=str, help='port for postgres')
    parser.add_argument('--database', type=str, help='database name for postgres')
    parser.add_argument('--table_name', type=str, help='table name where we will write the results to')
    parser.add_argument('--url', type=str, help='url of the csv file')

    args = parser.parse_args()
    main(args)











