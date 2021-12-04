import argparse
import pandas as pd
import numpy as np
from binance_defaults import *

def read_csv(filename):
    df = pd.read_csv(filename, )
    labels = np.zeros(df.shape[0])    
    for index, price_mean in enumerate(df.price_mean):
        if index == 0:
            continue
        labels[index] = 1 if price_mean > df.price_mean[index-1] else -1
    df['label'] = labels
        
    return df    

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
        
    df.to_csv(args.output, index=False)


    

if __name__ == '__main__':
    main() 