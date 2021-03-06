from src.dao.social_graph.getter.social_graph_getter import SocialGraphGetter
from src.model.social_graph.social_graph import SocialGraph
from typing import Dict, Optional
from src.dao.mongo.mongo_dao import MongoDAO
import bson
import networkx as nx


class MongoSocialGraphGetter(SocialGraphGetter, MongoDAO):
    def get_social_graph(self, seed_id: str, params: Optional[Dict] = None):
        doc = None

        if params is not None:
            doc = self.collection.find_one({"seed_id": bson.int64.Int64(seed_id)})
        else:
            doc = self.collection.find_one({
                "seed_id": bson.int64.Int64(seed_id),
                "params": params})

        return SocialGraph.fromDict(doc)
