import io
from surprise import Dataset
from surprise import get_dataset_dir
from surprise import KNNBaseline
from collections import defaultdict
from requests import get
from SPARQLWrapper import SPARQLWrapper, JSON
import json

user_id = "12"

data = Dataset.load_builtin('ml-100k')
trainset = data.build_full_trainset()

sim_options = {'name': 'cosine', 'user_based': True, 'min_support': 5}
algo = KNNBaseline(k=4, sim_options=sim_options)
algo.fit(trainset)

testset = trainset.build_anti_testset()
testset = filter(lambda x: x[0] == user_id, testset)
predictions = algo.test(testset)

def get_top_n(predictions, n=5):
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, round(est, 3)))
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]
    return top_n

def read_item_names():
    file_name = get_dataset_dir() + '/ml-100k/ml-100k/u.item'
    rid_to_name = {}
    with io.open(file_name, 'r', encoding='ISO-8859-1') as f:
        for line in f:
            line = line.split('|')
            rid_to_name[line[0]] = (line[1][0:-6]).strip()
    return rid_to_name


def getFilmUri(movie: str):
    json = get('https://www.wikidata.org/w/api.php', {
        'action': 'wbgetentities',
        'titles': movie,
        'sites': 'enwiki',
        'props': '',
        'format': 'json'
    }).json()
    filmUri = list(json['entities'])[0]
    return filmUri

top_n = get_top_n(predictions)
rid_to_name = read_item_names()

print('User ' + user_id)
for movie_rid, raiting in top_n[user_id]:
    print(rid_to_name[movie_rid])
    filmUri = getFilmUri(rid_to_name[movie_rid])
    if filmUri=="-1" : 
        print("Can not find information for current film")
    else:
        sparql = SPARQLWrapper("http://query.wikidata.org/sparql")
        sparql.setQuery("""
        SELECT DISTINCT ?cast ?castName
        WHERE
        {
	         wd:%s wdt:P161 ?cast.
	         ?cast rdfs:label ?castName.
	         FILTER(lang(?castName) = "en")
		
	         ?oscar wdt:P31 wd:Q19020.
  
	        ?cast wdt:P31 wd:Q5 .
	        ?cast wdt:P21 wd:Q6581072 .
	        OPTIONAL{ ?cast wdt:P166 ?award 
				 FILTER(?award != ?oscar) . }
 
        }""" % filmUri)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        print("Query results:")
        for result in results["results"]["bindings"]:
        	print(result["cast"]["value"] , result["castName"]["value"])





