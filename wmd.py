from time import time
import os

start_nb = time()

# Define sentences
sent_a = 'Modi had a chat with Bear Grylls in Jim Corbett'
sent_b = 'Modi had a chat with Bear Grylls in Jim Corbett'
sent_a = sent_a.lower().split()
sent_b = sent_b.lower().split()
print(sent_a)
print(sent_b)

from nltk.corpus import stopwords
from nltk import download

download('stopwords')  # Download stopwords

# Remove stopwords
stop_words = stopwords.words('english')
sent_a = [w for w in sent_a if w not in stop_words]
sent_b = [w for w in sent_b if w not in stop_words]

start = time()

import gensim
from gensim.models import Word2Vec

model = gensim.models.KeyedVectors.load_word2vec_format("GoogleNews-vectors-negative300.bin", binary=True)
distance = model.wmdistance(sent_a, sent_b)  # Compute WMD as normal

print('Cell took %.2f seconds to run' % (time() - start))

distance = model.wmdistance(sent_a, sent_b)
print('Distance = %.4f' % distance)
