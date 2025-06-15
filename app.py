from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    selected_site = 'eztvx'  # valor padrão
    if request.method == 'POST':
        query = request.form['query']
        selected_site = request.form['site']
        url = f'https://trnt.librey.org/api.php?query={query}&site={selected_site}'

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()

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
            else:
                app.logger.error(f"Erro HTTP: {response.status_code}")
        except Exception as e:
            app.logger.error(f"Erro ao buscar dados da API: {e}")

    # Lista de sites para o dropdown
    sites = [
        'yts', 'academic_torrents', 'piratebay',
        '1337x', 'rarbg', 'kiwi_torrent_research', 'eztvx'
    ]

    return render_template('index.html', results=results, sites=sites, selected_site=selected_site)

if __name__ == '__main__':
    app.run(debug=True)