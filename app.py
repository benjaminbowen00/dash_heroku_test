# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import dash_auth
import pandas as pd
import os

app = Dash(__name__)
server = app.server

user_value = os.getenv("test_user")
password_value = os.getenv("test_password")
valid_username_pairs = [[user_value, password_value]]
auth=dash_auth.BasicAuth(app, valid_username_pairs)


app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-TYV2KCYLG2"></script>
        <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'G-TYV2KCYLG2');
        </script>

        <!-- Google Tag Manager -->
        <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
        new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
        j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
        'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
        })(window,document,'script','dataLayer','GTM-NMHFHLG');</script>
        <!-- End Google Tag Manager -->


        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-NMHFHLG"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''
df = pd.read_csv("data.csv")
df2 = pd.read_csv("crime_data.csv")
districts = sorted(df2.District.unique().tolist()[:9])

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        df['year'].min(),
        df['year'].max(),
        step=None,
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        id='year-slider'
    ),
    dcc.Dropdown(['NYC', 'MTL', 'SF'], 'NYC', id='demo-dropdown', style={'width':'200px'}),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.H4(id="output-text"),
    dcc.Dropdown(options=[{'label':d, 'value':d} for d in districts], value=districts[0], id="district-dd", style={"width":"400px"}),
    dcc.Graph(id="graph2")

])

@app.callback(
    Output('output-text', 'children'),
    Input('submit-val', 'n_clicks'), State('demo-dropdown', 'value'))
def update_text(n_clicks, city):
    if n_clicks != 0:
        return city
    else:
        return "no value selected yet"


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55,
                     range_y=[df['lifeExp'].min(), df['lifeExp'].max()],
                     range_x=[df['gdpPercap'].min(), df['gdpPercap'].max()])

    fig.update_layout(transition_duration=500)

    return fig


@app.callback(
    Output('graph2', 'figure'),
    Input('district-dd', 'value'))
def update_figure(district):
    filtered_df = df2[df2.District == district]
    data = filtered_df.groupby("Description").size().reset_index().rename(columns={0:"count"})
    fig = px.bar(data, x="Description", y="count")

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)