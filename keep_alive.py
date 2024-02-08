from flask import Flask, render_template
from threading import Thread

app = Flask(__name__)

BOT_NAME = "Uslum Delisi"


@app.route('/')
def main():
  return render_template('index.html', bot_name=BOT_NAME)


def run():
  app.run(host='0.0.0.0', port=8080)


def keep_alive():
  server = Thread(target=run)
  server.start()


if __name__ == "__main__":
  keep_alive()
  app.run(host='0.0.0.0', port=8080)
