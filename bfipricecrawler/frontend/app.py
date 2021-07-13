from flask import Flask, render_template, request

from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch('localhost', port=9200)


@app.template_filter()
def currency_format(value):
    value = float(value)
    return "Rp {:,.2f}".format(value)


@app.route('/')
def home():
    return render_template('search.html')


@app.route('/search/cars', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]
    try:
        parsing_search = search_term.split('.')
        merek = parsing_search[0]
        model = parsing_search[1]
        varian = parsing_search[2]

        if varian.find('AT') != -1:
            transmisi = 'Automatic'
        elif varian.find('MT') != -1:
            transmisi = 'Manual'

        res = es.search(
            index=["carsearchengine"],
            size=10000,
            body={
                "query": {
                    "bool": {
                        "must": {
                            "term": {"merek": merek.lower()}
                        },
                        "filter": {
                            "term": {"model": model.lower()}
                        },
                        "should": [
                            {"term": {"transmisi": transmisi.lower()}},
                            {"term": {"varian": varian.lower()}}
                        ],
                        "minimum_should_match": "95%",
                        "boost": 1.0
                    }
                },
                "aggs": {
                    "price_stats": {"stats": {"field": "harga"}},
                    "agg_lokasi": {
                        "terms": {"field": "provinsi.keyword"},
                        "aggs": {
                            "price_stats": {"stats": {"field": "harga"}}
                        }
                    },
                    "model_merek_tahun": {
                        "multi_terms": {
                            "terms": [{
                                "field": "merek.keyword"
                            }, {
                                "field": "model.keyword"
                            },
                                {
                                    "field": "varian.keyword"
                                },
                                {
                                    "field": "transmisi.keyword"
                                }
                                ,
                                {
                                    "field": "tahun.keyword"
                                }

                            ]
                        },
                        "aggs": {"price_stats": {"stats": {"field": "harga"}}}
                    }
                }
            }
        )

        return render_template('car_results.html', res=res)
    except:
        res = es.search(
            index=["carsearchengine"],
            size=10000,
            body={
                "query": {
                    "multi_match": {
                        "query": search_term,
                        "fields": [
                            'merek',
                            "model",
                            "tahun",
                            "warna"
                        ]
                    }
                },
                "aggs": {
                    "price_stats": {"stats": {"field": "harga"}},
                    "agg_lokasi": {
                        "terms": {"field": "provinsi.keyword"},
                        "aggs": {
                            "price_stats": {"stats": {"field": "harga"}}
                        }
                    },
                    "model_merek_tahun": {
                        "multi_terms": {
                            "terms": [{
                                "field": "merek.keyword"
                            }, {
                                "field": "model.keyword"
                            },
                                {
                                    "field": "varian.keyword"
                                },
                                {
                                    "field": "transmisi.keyword"
                                }
                                ,
                                {
                                    "field": "tahun.keyword"

                                }

                            ],
                            "order": {"_term": "asc"}
                        },
                        "aggs": {"price_stats": {"stats": {"field": "harga"}}}
                    }
                }
            }
        )

        return render_template('car_results.html', res=res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
