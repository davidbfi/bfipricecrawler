import requests
import json

def check_if_index_is_present(url):
    response = requests.request("GET", url, data="")
    json_data = json.loads(response.text)
    return json_data


if __name__ == "__main__":
    url = "http://localhost:9200/_template/search_engine_template/"
    response = requests.request("GET", url, data="")

    if(len(response.text)>2):
        print("1. Deleted template: search_engine_template")
        response_delete = requests.request("DELETE", url)
    payload = {
          "template": "searchcar",
          "settings": {
            "number_of_shards": 1
          },
          "mappings": {
            "priceaggregator": {
                "_source": {
                    "enabled": True
                },
                "properties": {
                    "nama": {
                        "type": "text"
                    },
                    "merek": {
                        "type": "text"
                    },
                    "model": {
                        "type": "text"
                    },
                    "varian": {
                        "type": "text"
                    },
                    "harga": {
                        "type": "text"
                    },
                    "url": {
                        "type": "text"
                    },
                    "provinsi": {
                        "type": "text"
                    },
                    "kabupaten_kecamatan": {
                        "type": "text"
                    },
                    "tanggal_diperbaharui_sumber": {
                        "type": "text"
                    }
                }
            }

          }
    }
    payload = json.dumps(payload)
    headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }
    response = requests.request("PUT", url, data=payload, headers=headers)
    if (response.status_code == 200):
        print("2. Created a new template: search_engine_template")

    url = "http://localhost:9200/searchcar"
    json_data = check_if_index_is_present(url)

    if(not 'error' in json_data):
        print("3. Deleted an index: searchcar")
        response = requests.request("DELETE", url)

    response = requests.request("PUT", url)
    if (response.status_code == 200):
        print("4. Created an index: searchcar")

    url = "http://localhost:9200/autocomplete_car"
    json_data = check_if_index_is_present(url)

    if(not 'error' in json_data):
        print("5. Deleting index: autocomplete")
        response = requests.request("DELETE", url)

    payload = {
      "mappings": {
        "titles": {
          "properties": {
            "title": {"type": "string"},
            "title_suggest": {
              "type": "completion",
              "analyzer": "standard",
              "search_analyzer": "standard",
              "preserve_position_increments": False,
              "preserve_separators": False
            }
          }
        }
      }
    }
    payload = json.dumps(payload)
    response = requests.request("PUT", url, data=payload, headers=headers)

    if(response.status_code==200):
        print("6. Created a new index: autocomplete")


"""
find end point mapping in elasticsearch
http://localhost:9200/carsearchengine/_mapping

send parameter

{
  "properties": {
    "my_field": { 
      "type":     "text",
      "fielddata": true
    }
  }
}

curl -X DELETE "localhost:9200/carsearchengine?pretty"

"""