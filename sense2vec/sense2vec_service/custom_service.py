from __future__ import unicode_literals, print_function
try:
    from urllib.parse import unquote
except ImportError:
    from urllib2 import unquote

import ujson as json
import spacy
import sense2vec
import falcon
from falcon_cors import CORS
from .similarity import Similarity
from sense2vec.vectors import VectorMap

VECTORS_DIR = "/home/abhi/Documents/sense2vec_models/vectors"

class SimilarityService(object):
    '''Expose a sense2vec handler as a GET service for falcon.'''
    def __init__(self, vectors_dir):
        self.vectors_dir = vectors_dir
        self.handler = Similarity(
            spacy.load('en', parser=False, entity=False),
            self.load_vectors())
    
    def load_vectors(self):
        v = VectorMap(128)
        v.load(self.vectors_dir)
        return v

    def on_get(self, req, resp, query=''):
        j = json.dumps(self.handler(unquote(query)))
        resp.status = falcon.HTTP_201
        resp.body = j


def load():
    '''Load the sense2vec model, and return a falcon API object that exposes
    the SimilarityService.
    '''
    # cors = CORS(allow_all_origins=True, allow_all_methods=True, allow_all_headers=True)
    # app = falcon.API(middleware=[cors.middleware])
    app = falcon.API()
    app.add_route('/{query}', SimilarityService(VECTORS_DIR))
    return app


