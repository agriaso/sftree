import requests, os, pandas as pd

def get_tree_data():
    url = 'https://data.sfgov.org/resource/qrwx-q4gg.json?$limit=500000'
    response = requests.get(url)
    data = response.json()
    return pd.DataFrame(data)

def save_tree_data(dataframe):
    dataframe.to_csv('tree_data.csv', index=False)

if __name__ == '__main__':

    if os.path.exists('tree_data.csv'):
        # nothing
        df = pd.read_csv('tree_data.csv')
    else:
        df = get_tree_data()
        save_tree_data(df)
    
    print(df.head())