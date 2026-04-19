
from flask import Flask, render_template, request
import requests
import plotly.graph_objects as go
import plotly.io as pio


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/races')
def races():
    season = request.args.get('season')

    url = f'https://v1.formula-1.api-sports.io/races?season={season}'

    headers = {
        'x-apisports-key': 'bd29202cd43e12e152a8d51c02531016'
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)

    return render_template("races.html", races=data)


@app.route('/circuits')
def circuits():
    url = 'https://v1.formula-1.api-sports.io/circuits'
    headers = {'x-apisports-key': 'bd29202cd43e12e152a8d51c02531016'}

    response = requests.get(url, headers=headers)
    data = response.json()

    # Sort the response list
    # We use float('inf') for None values to push them to the end
    if 'response' in data:
        data['response'].sort(
            key=lambda x: x.get('first_grand_prix') if x.get('first_grand_prix') is not None else float('inf'))

    return render_template("circuits.html", races=data)

@app.route('/teams')
def teams():
    url =  'https://v1.formula-1.api-sports.io/teams?'

    headers = {
        'x-apisports-key': 'bd29202cd43e12e152a8d51c02531016'
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)

    return render_template("teams.html", teams=data)

@app.route('/drivers')
def drivers():
    season = request.args.get('season')

    url = f'https://v1.formula-1.api-sports.io/rankings/drivers?season={season}'

    headers = {
        'x-apisports-key': 'bd29202cd43e12e152a8d51c02531016'
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    return render_template("drivers.html", drivers=data)

@app.route('/driverdetails')
def driver_details():
    driver_name = request.args.get('driver_name')

    url = f'https://v1.formula-1.api-sports.io/drivers?name={driver_name}'

    headers = {
        'x-apisports-key': 'bd29202cd43e12e152a8d51c02531016'
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    return render_template("driver_details.html", drivers_details=data)

@app.route('/visualization')
def visualization():
    race = request.args.get('race')
    season = request.args.get('season')

    headers = {
        'x-apisports-key': 'bd29202cd43e12e152a8d51c02531016'
    }

    url = f'https://v1.formula-1.api-sports.io/races?season={season}'
    response1 = requests.get(url, headers=headers)
    data1 = response1.json()

    return render_template(
        "drivers_visualization.html",
        races=data1.get('response', []),
    )


@app.route('/lap_visualization')
def lap_visualization():
    race = request.args.get('race')
    season = request.args.get('season')
    headers = {
        'x-apisports-key': 'bd29202cd43e12e152a8d51c02531016'
    }
    driver_names = []
    lap_times = []
    avg_speed = []
    lap_numbers = []
    driver_teams=[]

    team_colors = {
        "Scuderia Ferrari": "red",
        "Red Bull Racing": "blue",
        "Mercedes-AMG Petronas": "black",
        "McLaren Racing": "orange",
        "Aston Martin F1 Team": "green",
        "Alpine F1 Team": "pink",
        "Williams F1 Team": "cyan",
        "Stake F1 Team Kick Sauber": "lime",
        "Haas F1 Team": "gray",
        "Racing Bulls": "purple"
    }


    if race:
        url2 = f'https://v1.formula-1.api-sports.io/rankings/fastestlaps?race={race}'
        data2 = requests.get(url2, headers=headers).json()

        for item in data2.get('response', []):
            driver_names.append(item['driver']['name'])
            lap_times.append(item['time'])
            avg_speed.append(item['avg_speed'])
            lap_numbers.append(item['lap'])
            driver_teams.append(item['team']['name'])

    bar_colors = [team_colors.get(team, "white") for team in driver_teams]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=driver_names,
        y=lap_times,
        text=[f"Lap {lap}" for lap in lap_numbers],  # shown on bars
        textposition='auto',
        marker = dict(color=bar_colors),
        hovertext=[
            f"Driver: {driver_names[i]}<br>Lap: {lap_numbers[i]}<br>Time: {lap_times[i]}s"
            for i in range(len(driver_names))
        ],
        hoverinfo='text'
    ))

    fig.update_layout(
        template='plotly_dark',
        xaxis_title="Drivers",
        yaxis_title="Lap Time"
    )

    fig2 = go.Figure()

    fig2.add_trace(go.Bar(
        x=driver_names,
        y=avg_speed,
        text=[f"Lap {lap}" for lap in lap_numbers],  # shown on bars
        textposition='auto',
        marker=dict(color=bar_colors),
        hovertext=[
            f"Driver: {driver_names[i]}<br>Lap: {lap_numbers[i]}<br>Speed: {avg_speed[i]}s"
            for i in range(len(driver_names))
        ],
        hoverinfo='text'
    ))

    fig2.update_layout(
        template='plotly_dark',
        xaxis_title="Drivers",
        yaxis_title="Avg speed"
    )

    time_graph_html = pio.to_html(fig, full_html=False)
    speed_graph_html = pio.to_html(fig2, full_html=False)

    return render_template("lap_visz.html",graph1=time_graph_html,graph2=speed_graph_html)

@app.route('/pit_visualization')
def pit_visualization():
    race = request.args.get('race')
    headers = {
        'x-apisports-key': 'bd29202cd43e12e152a8d51c02531016'
    }

    team_colors = {
        "Scuderia Ferrari": "red",
        "Red Bull Racing": "blue",
        "Mercedes-AMG Petronas": "black",
        "McLaren Racing": "orange",
        "Aston Martin F1 Team": "green",
        "Alpine F1 Team": "pink",
        "Williams F1 Team": "cyan",
        "Stake F1 Team Kick Sauber": "lime",
        "Haas F1 Team": "gray",
        "Racing Bulls": "purple"
    }

    if race:
        url = f'https://v1.formula-1.api-sports.io/pitstops?race={race}'
        response = requests.get(url, headers=headers).json()

        data = response.get('response', [])

        fig = go.Figure()
        fig_box = go.Figure()
        fig_heat=go.Figure()


        teams = {}

        def convert(time):
            try:
                if ":" in time:
                    return float(time.split(":")[1])  # take seconds part only
                else:
                    return float(time)
            except:
                return None


        for item in data:
            team = item['team']['name']
            lap = item['lap']
            pit_time = convert(item['time'])

            if team not in teams:
                teams[team] = {'lap': [], 'time': []}

            teams[team]['lap'].append(lap)
            teams[team]['time'].append(pit_time)




        for team, values in teams.items():
            fig.add_trace(go.Scatter(
                x=values['lap'],
                y=values['time'],
                mode='lines+markers',
                name=team,
                line=dict(color=team_colors.get(team, "grey")),
                hovertemplate=
                f"Team: {team}<br>" +
                "Lap: %{x}<br>" +
                "Pit Time: %{y}s<extra></extra>"
            ))

        fig.update_layout(
            template='plotly_dark',
            xaxis_title="Lap Number",
            yaxis_title="Pit Stop Time (seconds)"
        )

        for team, values in teams.items():
            fig_box.add_trace(go.Box(
                y=values['time'],
                name=team,
                boxmean='sd',
                marker=dict(color=team_colors.get(team, "gray")),

            ))

        fig_box.update_layout(
            template='plotly_dark',
            yaxis_title="Pit Stop Time (seconds)",
            xaxis_title="Teams"
        )


        teams_list = list(teams.keys())

        all_laps = sorted(set(
            lap for values in teams.values() for lap in values['lap']
        ))

        z = []

        for team in teams_list:
            row = []
            for lap in all_laps:
                if lap in teams[team]['lap']:
                    idx = teams[team]['lap'].index(lap)
                    row.append(teams[team]['time'][idx])
                else:
                    row.append(None)  # no pit stop
            z.append(row)


            fig_heat = go.Figure(data=go.Heatmap(
                z=z,
                x=all_laps,
                y=teams_list,
                colorscale='RdYlGn_r',
                colorbar=dict(title="Pit Time (s)")
            ))

            fig_heat.update_layout(
                template='plotly_dark',
                xaxis_title="Lap Number",
                yaxis_title="Teams"
            )

        graph_html = pio.to_html(fig, full_html=False)
        box_html = pio.to_html(fig_box, full_html=False)
        heat_html = pio.to_html(fig_heat, full_html=False)

        return render_template(
            "pit_visz.html",
            graph=graph_html,
            box_plot=box_html,
            heat_plot=heat_html
        )

@app.route("/Team_visualization")
def team_visualization():
    season = request.args.get('season')

    url = f'https://v1.formula-1.api-sports.io/rankings/drivers?season={season}'

    headers = {
        'x-apisports-key': 'bd29202cd43e12e152a8d51c02531016'
    }

    response = requests.get(url, headers=headers).json()
    data = response.get('response',[])

    fig=go.Figure()
    teams = {}

    for item in data:
        team_name = item['team']['name']
        driver = item['driver']['name']
        points = item['points']

        if team_name not in teams:
            teams[team_name] = {}

        teams[team_name][driver] = points

    for team, drivers in teams.items():
        for driver, points in drivers.items():
            fig.add_trace(go.Bar(
                x=[team],
                y=[points],
                name=driver
            ))

    fig.update_layout(
        template='plotly_dark',
        barmode='stack',
        title="Team Points Contribution",
        xaxis_title="Team",
        yaxis_title="Total Points"
    )

    bar_html = pio.to_html(fig, full_html=False)
    return render_template("team_visz.html",team_plot=bar_html)

if __name__ == "__main__":
    app.run(debug=True)