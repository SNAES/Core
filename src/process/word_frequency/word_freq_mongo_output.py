from typing import Union, List
from collections import Counter

class WordFrequencyMongoOutputDAO():
    # Important to distinguish between new entry and update
    def __init__(self):
        self.global_word_count_vector_collection = None
        self.user_word_count_vector_collection = None
        self.global_word_frequency_vector_collection = None
        self.user_word_frequency_vector_collection = None
        self.relative_user_word_frequency_vector_collection = None
        self.global_processed_tweets_collection = None
        self.user_processed_tweets_collection = None

    def store_global_word_count_vector(self, global_wc_vector):
        # Check whether an existing entry exists, update if so
        existing_global_wc_vector = self.global_word_count_vector_collection.find_one()
        if existing_global_wc_vector:
            existing_global_wc_vector = Counter(existing_global_wc_vector)
            global_wc_vector = Counter(global_wc_vector)
            updated_global_wc_vector = existing_global_wc_vector + global_wc_vector
            self.global_word_count_vector_collection.replace_one({}, updated_global_wc_vector)
        else:
            # Add global_wc_vector as a new entry
            self.global_word_count_vector_collection.insert_one(global_wc_vector)
    
    def store_user_word_count_vector(self, user_wc_vector):
        for user in user_wc_vector:
            wc_vector = Counter(user_wc_vector[user])

            user_doc = self.user_word_count_vector_collection.find_one({
                'user': user
            })
            if user_doc:
                # Update
                existing_wc_vector = Counter(user_doc['word_count_vector'])
                updated_wc_vector = existing_wc_vector + wc_vector
                self.user_word_count_vector_collection.replace_one({
                    'user': user
                }, {
                    'user': user,
                    'word_count_vector': updated_wc_vector 
                })
            else:
                # Add new entry
                self.user_word_count_vector_collection.insert_one({
                    'user': user,
                    'word_count_vector': wc_vector 
                })

    def store_global_word_frequency_vector(self, global_wf_vector):
        # Check whether an existing entry exists, update if so
        existing_global_wf_vector = self.global_word_frequency_vector_collection.find_one()
        if existing_global_wf_vector:
            global_wf_vector = Counter(global_wf_vector)
            self.global_word_frequency_vector_collection.replace_one({}, global_wf_vector)
        else:
            # Add global_wf_vector as a new entry
            self.global_word_frequency_vector_collection.insert_one(global_wf_vector)
    
    def store_user_word_frequency_vector(self, user_wf_vector):
        for user in user_wf_vector:
            wf_vector = Counter(user_wf_vector[user])

            user_doc = self.user_word_frequency_vector_collection.find_one({
                'user': user
            })
            if user_doc:
                # Update
                self.user_word_frequency_vector_collection.replace_one({
                    'user': user
                }, {
                    'user': user,
                    'word_frequency_vector': wf_vector
                })
            else:
                # Add new entry
                self.user_word_frequency_vector_collection.insert_one({
                    'user': user,
                    'word_frequency_vector': wf_vector 
                })
        
    def store_relative_user_word_frequency_vector(self, relative_user_wf_vector):
        for user in relative_user_wf_vector:
            relative_wf_vector = Counter(relative_user_wf_vector[user])

            user_doc = self.relative_user_word_frequency_vector_collection.find({
                'user': user
            })
            if user_doc:
                # Update
                self.relative_user_word_frequency_vector_collection.replace_one({
                    'user': user
                }, {
                    'user': user,
                    'relative_word_frequency_vector': relative_wf_vector 
                })
            else:
                # Add new entry
                self.relative_user_word_frequency_vector_collection.insert_one({
                    'user': user,
                    'relative_word_frequency_vector': relative_wf_vector 
                })

    def update_global_processed_tweet_state(self):
        """
        Assume that all tweets in the global processed tweets collection 
        have their words counted and word count vectors stored.
        Update is_counted field in global processed tweet docs to reflect this.
        """

        for global_tweet_doc in self.global_processed_tweets_collection.find():
            id = global_tweet_doc['_id']
            global_tweet_doc['is_counted'] = True
            self.global_processed_tweets_collection.replace_one({'_id': id}, global_tweet_doc)

    def update_user_processed_tweet_state(self):
        """
        Assume that all tweets in the user processed tweets collection 
        have their words counted and word count vectors stored.
        Update is_counted field in user processed tweet docs to reflect this.
        """

        for user_doc in self.user_processed_tweets_collection.find():
            user = user_doc['user']
            processed_tweet_list = user_doc['processed_tweets']

            for tweet in processed_tweet_list:
                tweet['is_counted'] = True

            self.user_processed_tweets_collection.replace_one({'user': user}, user_doc)