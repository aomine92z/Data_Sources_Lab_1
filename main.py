from flask import Flask

def hello_world():
    prefix_google = """
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=YOUR_GA_CODE">
    </script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'UA-285804915-2');
    </script>
        """
    return prefix_google + "Hello World"




app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)


@app.route("/mechantmechant")
def mechant():
    return "Hello from Space! 🚀"