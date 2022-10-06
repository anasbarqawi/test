import json
import plotly.graph_objs as go
from plotly.offline import plot as off_plot
import os
from read_json_files import read_json_files
import pandas as pd
import ast


def colorchecker(value, max_value):
    if value < round(max_value / 7, 4):
        color = "#1607ed"
    elif round(max_value / 7, 4) <= value < 2 * round(max_value / 7, 4):
        color = "#07b7ed"
    elif 2 * round(max_value / 7, 4) <= value < 3 * round(max_value / 7, 4):
        color = "#07ed7a"
    elif 3 * round(max_value / 7, 4) <= value < 4 * round(max_value / 7, 4):
        color = "#82ed07"
    elif 4 * round(max_value / 7, 4) <= value < 5 * round(max_value / 7, 4):
        color = "#ede907"
    elif 5 * round(max_value / 7, 4) <= value < 6 * round(max_value / 7, 4):
        color = "#ed7607"
    else:
        color = "#ed0707"

    return color


def room_heat_map(plots, polygon_a, room_name_a, room_center_point_a):
    color_scale_x_a = []
    color_scale_y_a = []
    color_scale_values_a = []

    for room in range(len(polygon_a)):

        room_a = polygon_a[room]
        name = room_name_a[room]
        centerpoint = room_center_point_a[room]

        x_a = []
        y_a = []

        for coordinate in room_a:
            x_a.append(coordinate[0])
            y_a.append(coordinate[1])
        x_a.append(x_a[0])
        y_a.append(y_a[0])

        # Create Room Circumfence

        line_marker = dict(color="black", width=5)
        traceLine = go.Scatter(x=x_a, y=y_a, mode='lines', line=line_marker, fill="none",
                               text=None, name=None,
                               showlegend=False)
        plots.append(traceLine)

        fillcolor = "rgb(255,255,255)"

        # plots.append(traceLine)

        try:
            x_a = [centerpoint[0]]
            y_a = [centerpoint[1]]

            color_scale_x_a.append(centerpoint[0])
            color_scale_y_a.append(centerpoint[1])
        except:
            print("missing coordinates")
        text_data = name
        traceLine = go.Scatter(x=x_a, y=y_a, mode='markers+text',
                               marker={'symbol': 'diamond-wide', 'size': 50, "color": 'rgb(173,216,230)'},
                               textfont={"color": "#ffffff", "size": 8}, name="TEST", hoverinfo="skip", line=None,
                               text=text_data, showlegend=False)
        plots.append(traceLine)

        # color_scale_x_a.append(room["Insertion"][index][0])
    return plots


def setup_room_footprints(plots, plotting_data_a, maximum_data_d, relevant_value):
    color_scale_x_a = []
    color_scale_y_a = []
    color_scale_values_a = []
    colorscale_a = ["#0087FF", "#416CF5", "#5D5FEF", "#825FDE", "#A95FCB", "#EF5DA8"]
    colorscale_rgb_a = ["rgba(0, 135, 255, 0.5)", "rgba(65, 108, 245, 0.5)", "rgba(93, 95, 239, 0.5)",
                        "rgba(130, 95, 222, 0.5)", "rgba(169, 95, 203, 0.5)", "rgba(239, 93, 168, 0.5)"]

    for room in plotting_data_a:

        print(room)
        x_a = []
        y_a = []

        for coordinate in room["geometry"]['coordinates'][0]:
            x_a.append(coordinate[0])
            y_a.append(coordinate[1])
        x_a.append(x_a[0])
        y_a.append(y_a[0])

        # Create Room Circumfence

        line_marker = dict(color="black", width=1)
        traceLine = go.Scatter(x=x_a, y=y_a, mode='lines', line=line_marker, fill="none",
                               text=None, hoverinfo="skip", name=None,
                               showlegend=False)
        plots.append(traceLine)

        # create Room filling
        try:
            room_value = room["Data"][relevant_value]
        except:
            room_value = 0
        try:
            data_text = room["Data"]["Room id"]
        except:
            data_text = "Name missing"

        maximum_value = maximum_data_d[relevant_value]
        print(maximum_value, room_value)
        fillcolor = colorchecker(room_value, maximum_value)
        # fillcolor="rgb(0, 135, 255)"
        line_marker = dict(color=fillcolor, width=0)
        traceLine = go.Scatter(x=x_a,
                               y=y_a,
                               mode='lines',
                               line=line_marker,
                               fill="toself",
                               text=str(room_value),
                               name=str(room["Data"]["Room area"]) + " sqm",
                               showlegend=False)
        plots.append(traceLine)
        plots.append(traceLine)
        plots.append(traceLine)

        for index in range(len(room["Data"])):
            try:
                data_text = room["Data"]["Room id"]
            except:
                data_text = "Not Transferred"
            try:
                x_a = [room["Insertion"][index][0]]
                y_a = [room["Insertion"][index][1]]

                color_scale_x_a.append(room["Insertion"][index][0])
                color_scale_y_a.append(room["Insertion"][index][1])
                color_scale_values_a.append(room_value)
            except:
                print("missing coordinates")

            traceLine = go.Scatter(x=x_a, y=y_a, mode='text', name=None, hoverinfo="skip", line=None, text=data_text,
                                   showlegend=False)
        plots.append(traceLine)

        # color_scale_x_a.append(room["Insertion"][index][0])

    traceLine = go.Scatter(x=color_scale_x_a,
                           y=color_scale_y_a,

                           name=None,
                           text=None,
                           hoverinfo="skip",

                           mode='markers',
                           marker=dict(
                               size=0,
                               opacity=0,
                               line=dict(
                                   color="black",
                                   width=0.0
                               ),
                               color=color_scale_values_a,
                               colorbar=dict(
                                   title=relevant_value

                               ),
                               colorscale="jet",
                               cmin=0,
                               cmax=maximum_data_d[relevant_value]), showlegend=False)
    plots.append(traceLine)

    return plots


def setup_wall_footprints(plots, plotting_data_a):
    for line in plotting_data_a["walls"]:

        try:
            x_a = []
            y_a = []

            for coordinate in line:
                x_a.append(coordinate[0])
                y_a.append(coordinate[1])

            line_marker = dict(color="grey", width=2)

            traceLine = go.Scatter(x=x_a, y=y_a, mode='lines', line=line_marker, fill="none",
                                   name=None,
                                   text=None,
                                   hoverinfo="skip",
                                   showlegend=False)
            plots.append(traceLine)
        except:
            print(line)

    return plots


def setup_window_footprints(plots, plotting_data_a):
    for window in plotting_data_a["windows"]:

        x_a = []
        y_a = []

        for coordinate in window:
            x_a.append(coordinate[0])
            y_a.append(coordinate[1])

        line_marker = dict(color="cyan", width=1)

        traceLine = go.Scatter(x=x_a, y=y_a, mode='lines', line=line_marker, fill="none",
                               name=None,
                               text=None,
                               hoverinfo="skip",
                               showlegend=False)
        plots.append(traceLine)

    return plots


def get_relevant_data(data_a):
    return [room for room in data_a if 'values' in room.keys()]


def room_data_prep(room_data_df, floor):
    room_data_d = []
    for i, j in room_data_df.iterrows():
        if j['Level'] == floor:
            x_coordinates = ast.literal_eval(j['Heatmaps X coordinates'])
            y_coordinates = ast.literal_eval(j['Heatmaps Y coordinates'])
            polygon = [[x, y_coordinates[xx]] for xx, x in enumerate(x_coordinates)]
            centerpoint = [j['Heatmaps X center point'], j['Heatmaps Y center point']]
            room_data_d.append({'text': j['Name'],
                                'polygon': polygon,
                                'coordinates': centerpoint})
    polygon_a = [room['polygon'] for room in room_data_d]
    room_name_a = [room['text'] for room in room_data_d]
    room_center_point_a = [room['coordinates'] for room in room_data_d]
    return polygon_a, room_name_a, room_center_point_a


def Building_Plot_doublecheck(title, polygon_a, room_name_a, room_center_point_a, target_fp):
    '''
    Hardcoded limit definition
    '''

    plots = []

    plots = room_heat_map(plots, polygon_a, room_name_a, room_center_point_a)
    # plots = setup_wall_footprints(plots, plotting_data_a)
    # plots = setup_window_footprints(plots, plotting_data_a)

    layout = go.Layout(title={"text": 'Room data double check', 'y': 0.9, 'x': 0.5, 'xanchor': 'center',
                              'yanchor': 'top'},
                       showlegend=True, grid=None, plot_bgcolor="rgba(0,0,0,0)",
                       paper_bgcolor="rgba(0,0,0,0)",
                       legend=dict(orientation="h", yanchor='bottom', xanchor='center', y=-0.1, x=0.5,
                                   font=dict(size=15)))

    fig = go.Figure(data=plots, layout=layout)
    fig.update_yaxes(
        scaleanchor="x",
        scaleratio=1,
        visible=False,
    )
    fig.update_xaxes(visible=False)

    title = title.replace("/", "per")
    off_plot(fig, filename=target_fp + "//" + title + ".html", auto_open=False)


project_folder = r"G:\Shared drives\04_Sales_and_Projects\03_Operations\Twin_Hatten\2022\Development Projects\Testing"
data_set_title = 'Visual confirmation room data'
room_data_df = pd.read_csv(os.path.join(project_folder, 'Room data template testing.csv'))
floor = '3.OG'
polygon_a, room_name_a, room_center_point_a = room_data_prep(room_data_df, floor)

Building_Plot_doublecheck(data_set_title, polygon_a, room_name_a, room_center_point_a, project_folder)
