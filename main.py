import subprocess
import tempfile

import flask


app = flask.Flask(__name__)


def render(source):
    script = 'library("rmarkdown")\nrender("{}", output_file="{}")\n'
    with tempfile.NamedTemporaryFile('r', prefix='rdowner-', suffix='.html') as f:
        proc = subprocess.run(
            ['R', '--vanilla'],
            input=script.format(source, f.name).encode('utf-8'),
            stdout=subprocess.PIPE,
        )

        return f.read(), proc.stdout


@app.route('/')
def index():
    return flask.send_file('index.html')


@app.route('/render', methods=['POST'])
def rendering():
    with tempfile.NamedTemporaryFile('w', prefix='rdowner-', suffix='.Rmd') as f:
        f.write(flask.request.data.decode('utf-8'))
        f.flush()
        result, log = render(f.name)

    return flask.jsonify(html=result, log=log.decode('utf-8'))


if __name__ == '__main__':
    app.run(debug=True)
