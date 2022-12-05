#downloaded w2v/vectors.txt from https://www.deepset.ai/german-word-embeddings, Word2Vec Vectors: https://int-emb-word2vec-de-wiki.s3.eu-central-1.amazonaws.com/vectors.txt
 
import pandas as pd
import pickle
from sklearn.decomposition import PCA
 
#open file in chunks to be easy on the memory
chunksize=16384
list_of_dataframes = []
for df in pd.read_csv('w2v/vectors.txt', chunksize=chunksize, delimiter=" ", header=None, encoding="utf-8"):
    list_of_dataframes.append(df)
result = pd.concat(list_of_dataframes)

#result[0] column has a bytestring saved as a string. I struggled finding a solution that could convert that to a usable format. The only way I found to deal with that is to use eval(), which is bad practice, so beware
result[0] = result[0].apply(lambda x: eval(x).decode())

#filesize: if we save this as a pickle file now, it will have a size of 1.9 GiB. The zipped file still takes up 1.4 GiB.
#Idea: Use PCA: Using dimensionality reduction, it's possible to retain 80% of the dimensions' variance while only storing 50 variables (and not 300):

w2v_voc = result[0]
w2v = result.iloc[:,1:]
pca = PCA(n_components=50).fit_transform(w2v)

print("Original variance: " + str(sum(w2v.var(axis=0))))
print("PCA reduced variance: " + str(sum(pca.var(axis=0))))

#reduced file will take 336 MiB which is much more managable. Zipping the file doesn't reduce the file size substantially.

out = pd.concat([w2v_voc, pd.DataFrame(pca)], axis=1) #merge vocabulary with new dimensions
out.columns = range(out.columns.size) #reset index

#Splitting everything up in multiple chunks to save it in multiple files. Reason: Git only allows files up to 50MB.
def split_dataframe(df, chunk_size = 100000): 
    chunks = list()
    num_chunks = len(df) // chunk_size + 1
    for i in range(num_chunks):
        chunks.append(df[i*chunk_size:(i+1)*chunk_size])
    return chunks

outs = split_dataframe(out)

#save pickle to (hopefully) load in data more easily/quickly later
for i in range(len(outs)):
    with open('w2v/vectors_'+str(i)+'.pkl', 'wb') as file:
        pickle.dump(outs[i], file)
