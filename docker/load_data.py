from elasticsearch import Elasticsearch, helpers
import json
import csv

with open("cred.txt", encoding="utf8") as file:
    password = file.read()
es = Elasticsearch('https://localhost:9200', ca_certs="http_ca.crt", basic_auth=("elastic", password))
def load(filepath, index, type="json"):
    with open(filepath, encoding="utf8") as file:
        if type == "json":
            docs = json.loads(file.read())
        elif type == "csv":
            docs_helper = csv.DictReader(file)
            docs = []
            for x in docs_helper:
                docs.append(x)
        else:
            print("ERROR")
            exit()
        for x in docs:
            x['_index'] = index
        # docs = [{'_op_type': 'index', '_index': 'mtgcards', 'title': 'Testitle', 'doc': 'testDoc'}]
        print(docs[0:10])
        helpers.bulk(es, docs)
    print(filepath + " loaded")

fname = "datafiles/"
# load mtgcards
# load(fname + "cards.json", "mtgcards")
# # load tarotimages
# load(fname + "tarot-images.json", "tarotimages")
# # load horoscopesaved
# load(fname + "horoscope_saved.csv", "horoscopesaved", type="csv")
# # load tarotreadings
# load(fname + "tarot_readings.csv", "tarotreadings", type="csv")
# load analyzed horoscopes
# load(fname + "horoscope_predicted_general.csv", "horoscopepredictedgeneral", type="csv")
filepath = fname + "horoscope_predicted_general.csv"
index = "horoscopepredictedgeneral"
type = "csv"
with open(filepath, encoding="utf-8-sig") as file:
    if type == "json":
        docs = json.loads(file.read())
    elif type == "csv":
        docs_helper = csv.DictReader(file)
        docs = []
        for x in docs_helper:
            docs.append(x)
    else:
        print("ERROR")
        exit()
    for x in docs:
        x['_index'] = index
    # docs = [{'_op_type': 'index', '_index': 'mtgcards', 'title': 'Testitle', 'doc': 'testDoc'}]
    print(docs[0:10])
    helpers.bulk(es, docs)
print(filepath + " loaded")