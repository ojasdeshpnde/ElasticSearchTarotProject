
import random
from elasticsearch import Elasticsearch
from transformers import pipeline
import pandas as pd

path_to_creds = "../../docker/"
df = pd.read_excel(path_to_creds + 'datafiles/PromptCategories.xlsx') # can also index sheet by name or fetch all sheets
candidate_labels = df['Categories'].tolist()
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")
with open(path_to_creds + "cred.txt", encoding="utf8") as file:
    password = file.read()
es = Elasticsearch('https://localhost:9200', ca_certs=path_to_creds + "http_ca.crt", basic_auth=("elastic", "fAhOSOHq_3spLm9ht_tW"))

def searchCardsByName(name, size=10):
    hits = es.search(index="mtgcards", body={"sort": "_score", "size": size, "query": {"bool":
                                                                         {"should": {"match": {"name": {"query": name, "fuzziness": "AUTO"}}},
                                                                          "must": {"match": {"layout": {"query": "normal"}}},
                                                                          }}})['hits']['hits']
    if len(hits) == 0:
        hits = random.choice(es.search(index="mtgcards", body={"query": {"match_all": {}}})['hits']['hits'])
        # print(hits)
    else:
        weights = [0]*len(hits)
        for i, j in enumerate(hits):
            weights[i] = j["_score"]
        # just weighting by the score
        hits = random.choices(hits, weights=weights, k = 1)[0]
    hits=hits['_source']
    if 'image_uris' in hits:
        return hits['image_uris']['large']
    elif 'card_faces' in hits:
        print(hits['card_faces'])
        return random.choice(hits['card_faces'])['image_uris']['large']
    else:
        return searchCardsByName("")
def findHoroscope(sequence_to_classify, number = 10, positivity_threshold = 2, positivity_weight = 2, power = 2, user="User"):
    c = classifier(sequence_to_classify, candidate_labels, multi_label=True)
    # c = {'sequence': 'blah', 'labels': ['a', 'b', 'c', 'd', 'e', 'f'], 'scores': [0.2,0.3,0,0.4,0.5,0.5]}
    c = pd.Series(index = c['labels'], data = c['scores']).sort_values(ascending=False) # .head(number).to_dict()
    print(c)
    a = 1
    var = 10000
    print(c.size)
    print(c.iloc[:a+2].std())
    print(c.iloc[a+1:].std())
    while a < c.size and c.iloc[:a+1].std() + c.iloc[a+1:].std() < var:
        var = c.iloc[:a+1].std() + c.iloc[a+1:].std()
        a += 1
        print(var)
        print(a)
    print(c.iloc[:a+1].std() + c.iloc[a+1:].std())
    c = c.head(a).to_dict()

    def get_list(label_noise):
        l = []
        for key in c:
            # l.append({"range": {key: {"gte": c[key]-label_noise,"lte": c[key]+label_noise}}})
            l.append({"range": {key: {"gte": c[key]-label_noise}}})
        return l
    # s = sentiment_pipeline(sequence_to_classify)
    # if s[0]['label'] == 'POSITIVE':
    #     print("Positive!")
    #     bad = 'negative'
    # else:
    #     print("Negative!")
    #     bad = 'positive'
    bad = 'positive'
    # hits = es.search(index="horoscopepredictedgeneral", body={"query": {"range": {bad: {"lte": 1000}},
    #                                                                                         }})['hits']['hits']
    # hits = es.search(index="horoscopepredictedgeneral", body={"query": {"bool": {"must": l}}})['hits']['hits']
    hits = []
    label_noise = 0.05
    while len(hits) < 10:
        hits = es.search(index="horoscopepredictedgeneral", body={"query": {"bool": {"must": get_list(label_noise)}}}, size= 100)['hits']['hits']
        label_noise += 0.05
    weights = [0] * len(hits)
    print(c)
    for i, j in enumerate(hits):
        print(j["_source"]["horoscope"])
        for k in c:
            print(float(j["_source"][k]))
            weights[i] += float(j["_source"][k])**power
    # print(weights)
    # print(hits)
    for i, a in enumerate(hits):
        print(weights[i])
        print(a["_source"]["horoscope"])
    # just weighting by the score
    hits = random.choices(hits, weights=weights, k=1)[0]
    # print(hits)
    # print(c)
    # print(s)
    return hits["_source"]["horoscope"].replace(hits["_source"]["sign"].lower().title(), user)
print(findHoroscope("I plan to start exercising"))
