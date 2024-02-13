from elasticsearch import Elasticsearch

with open("cred.txt", encoding="utf8") as file:
    password = file.read()
es = Elasticsearch('https://localhost:9200', ca_certs="http_ca.crt", basic_auth=("elastic", password))

print(es.search())
es.delete_by_query(index="mtgcards", body={"query": {"match_all": {}}})
es.delete_by_query(index="tarotimages", body={"query": {"match_all": {}}})
es.delete_by_query(index="horoscopesaved", body={"query": {"match_all": {}}})
es.delete_by_query(index="tarotreadings", body={"query": {"match_all": {}}})
print(es.search())
