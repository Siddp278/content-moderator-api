from django.core.cache import cache
import pickle

# Created to load the model once, so that it stays in cache and called from there.

tokenizer_cache_key = 'vocab_cache'
tokenizer_spanish_cache_key = 'vocab_spanish_cache'

model_key = 'model_cache'
model_spanish_key = 'model_spanish_cache'
# this key is used to `set` and `get` your trained model from the cache

tokenizer = cache.get(tokenizer_cache_key)
tokenizer_spanish = cache.get(tokenizer_spanish_cache_key)

model = cache.get(model_key)
model_spanish = cache.get(model_spanish_key)

if tokenizer is None:
    # your model isn't in the cache
    # so `set` it
    # load the pickle file
    tokenizer = pickle.load(open("polls/vectorizer.pkl", 'rb'))
    cache.set(tokenizer_cache_key, tokenizer, None)


if tokenizer_spanish is None:
    # your model isn't in the cache
    # so `set` it
    # load the pickle file
    tokenizer_spanish = pickle.load(open("polls/vectorizer-spanish.pkl", 'rb'))
    cache.set(tokenizer_spanish_cache_key, model, None)   


if model is None:
    # your model isn't in the cache
    # so `set` it
    # load the pickle file
    model = pickle.load(open("polls/lr_model.pkl", 'rb'))
    cache.set(model_key, model, None)

if model_spanish is None:
    # your model isn't in the cache
    # so `set` it
    # load the pickle file
    model_spanish = pickle.load(open("polls/lr_model_spanish.pkl", 'rb'))
    cache.set(model_spanish_key, model_spanish, None)

