from datetime import timedelta
import json
import pandas as pd
from pyodide.http import open_url

url = "https://raw.githubusercontent.com/onlyphantom/miband/main/data/jan2022_to_june2022.csv"
df = pd.read_csv(open_url(url), 
    parse_dates=['startTime'])
df ['date'] = (df ['startTime'] 
    + timedelta(hours=7)).dt.strftime("%Y-%m-%d %H:%M")
walks = df[df['type']==6].copy()
runs = df[(df['type']==1) 
    & (df['distance(m)']>=1000)].copy()
runs = runs.drop(
    columns=['type',
    'maxPace(/meter)', 
    'minPace(/meter)', 
    'avgPace(/meter)'])

# for top row statistics
# =======================    
num_of_runs = runs.shape[0]
run_distance_km = (sum(runs['distance(m)']))/1000
walks_distance_km = (sum(walks['distance(m)']))/1000

toprows=[
    round(num_of_runs,3),
    round(run_distance_km, 3),
    round(walks_distance_km, 3),
    round(run_distance_km + walks_distance_km, 3),
    [
        runs['startTime'].min().strftime('%Y-%m-%d'),
        runs['startTime'].max().strftime('%Y-%m-%d'),
    ]
    ]
    
print(json.dumps(toprows))

# =======================
runs['seconds_per_km'] = (1000 / runs['distance(m)']) * runs['sportTime(s)']

def create_m_s(seconds):
    m, s = divmod(seconds, 60)
    return "{:02.0f}:{:02.2f}".format(m, s)

runs['speed_per_km'] = runs['seconds_per_km'].map(lambda x : create_m_s(x))
runs = runs.sort_values(by='seconds_per_km')
runs['distance_rounded'] = (runs['distance(m)']//1000).astype('category')
bestruns=runs.groupby('distance_rounded').head(3)
print(bestruns[['date', 'speed_per_km', 'calories(kcal)', 'distance_rounded']].set_index(
    'date').reset_index().to_html(col_space=[100, 50, 50, 50], 
    table_id="bestruns", index=False, justify="justify",
    classes=['table table-dark table-bordered']))

print("<h4> Personal Best</h4>")
pb = runs.groupby('distance_rounded')['seconds_per_km'].agg(['mean', 'min'])
print(pb.reset_index().to_html(col_space=[50, 50, 50], index=False, table_id="personalbest", justify="justify",
classes=['table table-dark table-bordered']))
