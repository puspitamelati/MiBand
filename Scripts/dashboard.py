from datetime import timedelta
import pandas as pd
import altair as alt
from pyodide.http import open_url

alt.renderers.set_embed_options(theme='dark')

url = "https://raw.githubusercontent.com/onlyphantom/miband/main/data/run_1km.csv"
run_1km = pd.read_csv(open_url(url), parse_dates=['startTime'])

highlight= alt.selection(
    type='single', on='mouseover', fields=['day'], nearest=True 
)

base = alt.Chart(run_1km).mark_line().encode(
    alt.X('startTime:T'),
    alt.Y('seconds_per_km:Q'),
    color=alt.Color(
        'day:N',
        legend=alt.Legend(
            title = 'Day of Week',
            orient='bottom-left',
            formatType='time',
            format='%A'
        )
    )
).transform_timeunit(
    day='day(startTime)')

points = base.mark_circle().encode(
    opacity=alt.value(1),
    tooltip=['monthdate(startTime)','distance(m)', 'calories(kcal)', 'speed_per_km']
).add_selection(highlight)



lines = base.mark_line().encode(
    size=alt.condition(~highlight, alt.value(1), alt.value(4))
)


grid = alt.Chart(run_1km).mark_rect().encode(
    alt.X('date(startTime):O', title='Date'),
    alt.Y('month(startTime):O', axis=alt.Axis(title='')),
    color=alt.Color(
        'mean(seconds_per_km):Q',
        legend=alt.Legend(title='Avg_Speed')),
    tooltip=['monthdate(startTime)', 'distance(m)', 'calories(kcal)', 'speed_per_km' ]
).interactive()

bubble = alt.Chart(run_1km).mark_circle().encode(
    alt.X('date(startTime):O', title='Date'),
    alt.Y('month(startTime):O', axis=alt.Axis(title='')),
    size=alt.Size('seconds_per_km:Q',
        legend=None,
        scale=alt.Scale(range=[1,500], domain=[300, run_1km['seconds_per_km'].min()])
    ), 
    color=alt.Color(
        'seconds_per_km:Q'
    ),
    tooltip=['monthdate(startTime)', 'distance(m)', 'calories(kcal)', 'speed_per_km' ]
).interactive()

(points+lines).interactive() | alt.vconcat(grid, bubble)
#(points+lines).interactive() | grid