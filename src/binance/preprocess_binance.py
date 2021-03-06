import argparse
import pandas as pd
from binance_defaults import *

def read_csv(filename):
    df = pd.read_csv(filename, header=None)    
    headers =  TRADES_HEADER
    df.columns = headers
    
    # convert time column to datetime
    df['time'] = pd.DatetimeIndex( pd.to_datetime(df['time'], unit='ms') )

    # set the index    
    df.set_index('time', inplace=False)        
    return df    

def process_df(df, rule):
    df_hourly = df.resample(rule,on="time")
    mean_df = df_hourly.mean()
    std_df = df_hourly.std()    
    sum_df = df_hourly.sum()
    data = {
        'time' : mean_df.index,
        'price_mean' : mean_df.price,
        'price_std' : std_df.price,
        'qty' : sum_df.qty,
    }
    
    # Create DataFrame
    df_processed = pd.DataFrame(data)
    return df_processed

def main():
    parser = argparse.ArgumentParser()    
    parser.add_argument('--data', help='CSV Binance file', type=str) 
    parser.add_argument('--output', help='CSV Binance file', type=str) 
    parser.add_argument('--rule', help='H for hours, D for days', type=str, default ="D") 
    args = parser.parse_args()    

    if args.rule not in ["H","D"]:
        print("Invalid rule parameter")
        exit(1)


    df = read_csv(args.data)
    df = process_df(df, args.rule)

    df.to_csv(args.output, index=False)


    

if __name__ == '__main__':
    main() 