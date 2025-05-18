from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        query = request.form['query']
        url = f'https://trnt.librey.org/api.php?query={query}&site=yts'

        try:
            response = requests.get(url)
            data = response.json()

            # A resposta é um dicionário com keys "0", "1", ..., por isso percorremos os valores
            for entry in data.values():
                movie_data = entry.get("data", [])
                torrents = entry.get("torrents", [])

                for movie in movie_data:
                    results.append({
                        "title": movie.get("title", "Sem título"),
                        "year": movie.get("year", ""),
                        "rating": movie.get("rating", ""),
                        "summary": movie.get("summary", "Sem sinopse"),
                        "img": movie.get("img", ""),
                        "trailer": movie.get("yt_trailer_code", ""),
                        "torrents": torrents
                    })

        except Exception as e:
            print("Erro ao buscar dados da API:", e)

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
