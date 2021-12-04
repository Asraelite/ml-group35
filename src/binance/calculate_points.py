import argparse
import pandas as pd
import os

def main():
    parser = argparse.ArgumentParser()    
    parser.add_argument('--data-dir', help='CSV Binance file', type=str)     
    args = parser.parse_args()        

    data_dir = args.data_dir
    print(data_dir)

    total_data_points = 0 
    for file in sorted(os.listdir(data_dir)):
        if not file.endswith('.csv'):
            continue
        df = pd.read_csv(os.path.join(data_dir,file))
        data_points = len(df.index)
        total_data_points += data_points
        print("%s %d"%(file, data_points)) 
        print("Total data points %d"%(total_data_points))


    

if __name__ == '__main__':
    main() 