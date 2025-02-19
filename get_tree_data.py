import requests, os, pandas as pd, matplotlib.pyplot as plt, seaborn as sns, geopandas as gpd

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
    
    removals = gpd.read_file('removals.geojson')
    neighborhoods = gpd.read_file('districts.geojson')
    neighborhoods = neighborhoods.to_crs(epsg=4326)
    removals = removals.to_crs(epsg=4326)
    bounding_box = (-122.6, 37.6, -122.34, 37.84)  # Adjust as needed

# Clip the GeoDataFrame to exclude Farallon Islands
    sf_mainland = neighborhoods.clip(bounding_box)

    '''#rename column in neighborhoods
    neighborhoods.rename(columns={'sup_dist':'supervisordistrict'}, inplace=True)
    print(neighborhoods)

    merged = neighborhoods.merge(removals, on='supervisordistrict')
    merged.plot()'''

    fig, ax = plt.subplots(figsize=(10,10))
    sf_mainland.plot(ax=ax, column='sup_dist_pad', legend=True)
    #adjust removal dots to be transparent and smaller
    removals.plot(ax=ax, color='green', alpha=0.5, markersize=10)
    plt.title('Tree Removals by Supervisor District')

    plt.show()

    '''
    trees_by_district = df.groupby('supervisordistrict').size()
    print(trees_by_district)

    df.sort_values(by='actiondate', inplace=True, ascending=False)

    # convert action date into today, next 7 days, or next 30 days
    df['action_date'] = pd.to_datetime(df['actiondate'])
    print("What are the times?: ", df['action_date'].head(15))
    today = pd.Timestamp.today()
    next_week = today + pd.DateOffset(7)
    next_month = today + pd.DateOffset(30)
    df['action_date'] = df['action_date'].apply(
    lambda x: 'complete' if x < today
    else 'today' if x == today
    else 'next 7 days' if x < next_week
    else 'next 30 days' if x < next_month
    else 'future'
    )

    
    print(df['action_date'])

    by_district_and_district = df.groupby(['supervisordistrict', 'action_date']).size()
    print(by_district_and_district)

    by_action = df.groupby('action_date').size()
    print(by_action)

    tree_info = df[['actiondate','planttype', 'scientificname', 'commonname']]
    print(tree_info.sort_values('actiondate', ascending=False).head(10))

    by_tree = df.groupby(['supervisordistrict', 'commonname']).size()
    by_tree.to_csv('by_tree.csv')
    print(by_tree)

    by_tree_type = df.groupby('commonname').size()
    print("by common names\n",by_tree_type)

    by_action = df.groupby('actiontype').size()
    print(by_action)'''