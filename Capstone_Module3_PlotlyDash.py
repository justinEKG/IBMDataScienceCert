# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("./data/spacex_launch_dash.csv")
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

# Create a dash application
app = dash.Dash(__name__)

dropdown_options = [
    {"label": "All Sites", "value": "ALL"},
    {"label": "CCAFS LC-40", "value": "CCAFS LC-40"},
    {"label": "CCAFS SLC-40", "value": "CCAFS SLC-40"},
    {"label": "KSC LC-39A", "value": "KSC LC-39A"},
    {"label": "VAFB SLC-4E", "value": "VAFB SLC-4E"},
]

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        dcc.Dropdown(
            id="site-dropdown",
            options=dropdown_options,
            value="ALL",
            placeholder="Select a Launch Site",
            searchable=True,
        ),
        html.Br(),
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),
        html.P("Payload range (Kg):"),
        dcc.RangeSlider(
            id="payload-slider",
            min=min_payload,
            max=max_payload,
            step=1000,
            marks={
                i: f"{i}" for i in range(int(min_payload), int(max_payload) + 1, 1000)
            },
            value=[min_payload, max_payload],
        ),
        html.Br(),
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ]
)


@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
)
def get_pie_chart(selected_site):
    if selected_site == "ALL":
        fig = px.pie(
            spacex_df,
            values="class",
            names="Launch Site",
            title="Total Success Launches By Site",
        )
    else:
        filtered_spacex_df = spacex_df[spacex_df["Launch Site"] == selected_site]
        fig = px.pie(
            filtered_spacex_df,
            names="class",
            title=f"Total Success Launches for Site: {selected_site}",
        )

    return fig


@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [
        Input(component_id="site-dropdown", component_property="value"),
        Input(component_id="payload-slider", component_property="value"),
    ],
)
def get_scatter_chart(selected_site, payload_range):
    filtered_spacex_df = spacex_df[
        (spacex_df["Payload Mass (kg)"] >= payload_range[0])
        & (spacex_df["Payload Mass (kg)"] <= payload_range[1])
    ]

    if selected_site == "ALL":
        fig = px.scatter(
            filtered_spacex_df,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title="Correlation of Payload vs. Success for All Sites",
        )
        return fig

    else:
        filtered_spacex_df = filtered_spacex_df[
            filtered_spacex_df["Launch Site"] == selected_site
        ]
        fig = px.scatter(
            filtered_spacex_df,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title=f"Correlation of Payload vs. Success for Site: {selected_site}",
        )

    return fig


# Run the app
if __name__ == "__main__":
    app.run_server()
