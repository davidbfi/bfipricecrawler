from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch('localhost', port=9200)


@app.route('/')
def home():
    return render_template('search.html')


# @app.route('/search/results', methods=['GET', 'POST'])
# def search_request():
#     search_term = request.form["input"]
#     res = es.search(
#         index="bficar",
#         size=20,
#         body={
#             "query": {
#                 "multi_match": {
#                     "query": search_term,
#                     "fields": [
#                         "nama",
#                         "url",
#                     ]
#                 }
#             }
#         }
#     )
#     return render_template('results.html', res=res)


@app.route('/search/cars', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]
    res = es.search(
        index=["scrapycar-2021-05", "scrapycar-2021-06"],
        size=20,
        body={
            "query": {
                "multi_match": {
                    "query": " ".join(search_term.split('.')),
                    "fields": [
                        "nama",
                        "merek",
                        'model',
                        'transmisi',
                        'provinsi',
                        'source'
                    ]
                }
            }
        }
    )
    return render_template('car_results.html', res=res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)





