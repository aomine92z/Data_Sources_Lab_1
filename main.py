import streamlit as st
from flask import Flask, request, render_template, render_template_string
import requests
import os
import pandas as pd
import itertools
from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)



app = Flask(__name__, template_folder='template_folder')

@app.route('/')
def hello_world():
    prefix_google = """
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-Z74QSEWTX5">
    </script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-Z74QSEWTX5');
    </script>
    """

    # Adding style to make text fancy
    hello_style = 'font-size: 36px; color: #333; font-family: Arial, sans-serif;'

    # Adding style to change background color
    body_style = 'background-color: #f0f0f0;'

    buttons = """
    <div>
        <a href="/logger"><button style="background-color:#008CBA; color:white; padding:10px 20px;">Logger</button></a>
        <a href="/google_request"><button style="background-color:#4CAF50; color:white; padding:10px 20px;">Google Request</button></a>
        <a href="/moon"><button style="background-color:#f44336; color:white; padding:10px 20px;">Moon</button></a>
    </div>
    """

    return f'<div style="{body_style}">{prefix_google}<h1 style="{hello_style}">Hello World</h1>{buttons}</div>'



@app.route("/logger", methods=['GET', 'POST'])
def logger_page():
    # Print a log on the browser
    path_to_logger_html = '/logger.html'
    # print_on_browser = '<script>console.log("This is a log message on the browser.");</script>'
    if request.method == 'POST':
        message = request.form.get('message')  # Get the message from the form
        app.logger.warning(f"Received message: {message}")  # Log the message
        return render_template(path_to_logger_html, message=message)  # Render the template with the message
    return render_template(path_to_logger_html)  # Render the template without a message


@app.route("/google_request")
def google_request():
    req = requests.get("https://www.google.com/")
    cookies = req.cookies._cookies
    req2 = requests.get("https://analytics.google.com/analytics/web/#/p407503745/reports/intelligenthome")
    content = req2.text

    property_id = "407503745"
    starting_date = "16daysAgo"
    ending_date = "yesterday"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ga4-project-402308-e004e5e27539.json'

    client = BetaAnalyticsDataClient()

    request_api = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[
            Dimension(name="landingPagePlusQueryString")
            ],
            metrics=[
                Metric(name="sessions")
            ],
            date_ranges=[DateRange(start_date=starting_date, end_date=ending_date)],
        )
    
    response = client.run_report(request_api)

    return render_template_string("<pre>{{ cookies }}</pre><pre>{{ content }}</pre>", cookies=cookies, content=content) + f'Number of visitors : {response.rows[0].metric_values[0].value}'

@app.route("/moon")
def mechant():
    return """
    <html>
    <head>
        <style>
            body {
                background-image: url('static/moon.jpg');
                background-size: cover;
                background-repeat: no-repeat;
                color: #fff;
                font-family: Arial, sans-serif;
            }
            .container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
            }
            h1 {
                text-align: center; /* Center the text horizontally */
                position: absolute; /* Position absolutely within the container */
                top: 100; /* Position at the top of the container */
                width: 100%; /* Take up the full width of the container */
                background: rgba(0, 0, 0, 0.5); /* Add a semi-transparent background */
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Are you lost in Space ? 🚀</h1>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)