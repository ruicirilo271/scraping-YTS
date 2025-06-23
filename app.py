from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_URL = "https://trnt.librey.org/api.php"

@app.route("/", methods=["GET", "POST"])
def index():
    movies = []
    error = None
    query = ""
    site = "yts"

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        site = request.form.get("site", "yts").strip()

        if not query:
            error = "Insira um termo de pesquisa."
        else:
            try:
                response = requests.get(API_URL, params={"query": query, "site": site}, timeout=10)
                try:
                    parsed_json = response.json()
                except ValueError:
                    error = f"A API não retornou JSON válido para o site '{site}'."
                    parsed_json = {}
                else:
                    for key, block in parsed_json.items():
                        if not isinstance(block, dict):
                            continue

                        data = block.get("data", [])
                        torrents = block.get("torrents", [])

                        for movie in data:
                            filtered_torrents = [t for t in torrents if t.get("seeders", 0) > 0]
                            if not filtered_torrents:
                                continue

                            original_img_url = movie.get("img", "")

                            if site in ["thepiratebay", "1337"]:
                                movie["img"] = None
                            elif site == "yts" and original_img_url:
                                movie["img"] = "https://images.weserv.nl/?url=" + original_img_url.replace("https://", "")
                            elif original_img_url and original_img_url.endswith((".jpg", ".png")):
                                movie["img"] = original_img_url
                            else:
                                movie["img"] = None

                            movie["torrents"] = filtered_torrents
                            movies.append(movie)

            except Exception as e:
                error = f"Erro ao buscar dados: {e}"

    return render_template("index.html", movies=movies, error=error, query=query, site=site)

if __name__ == "__main__":
    app.run(debug=True)

