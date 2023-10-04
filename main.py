from flask import Flask, request, render_template

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
    return prefix_google + "Hello World"

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


@app.route("/moon")
def mechant():
    return "Hello from Space! 🚀"

if __name__ == '__main__':
    app.run(debug=True)