from flask import Flask
import codecs
from flask import request, render_template
from Sample import searchtext
from highlight1 import highlight

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def HomePage():
    file = codecs.open("Search Desk Home.html", "r", "utf-8")
    return file


@app.route('/Search', methods=['POST', 'GET'])
def Search():
    if request.method == "POST":
        Search.text = request.form.get("text")
        links = searchtext(Search.text)
        return render_template('header.html', links=links, text=Search.text)


@app.route('/Results', methods=['POST', 'GET'])
def Results():
    if request.method == "POST":
        link = request.form.get("f")
        print(link)
        print(Search.text)
        htmllink = highlight(Search.text, link)
        print(htmllink)
        file = codecs.open(htmllink, "r", "utf-8")
        return file


if __name__ == '__main__':
    app.run(debug=True)
