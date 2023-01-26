# Setup
Place CSVs from [here](https://sna22w.jupyter.hpc.tuwien.ac.at) in the `/input` directory and run `notebook.ipnyb`

# Running the code
Our group project code consists of various approaches related to how to measure similarities for our project's purposes. The following walks you through how to run the code to be found in this repository.

Our project code is written in Python 3 in the form of .ipynb Jupyter Notebook files and .py plain text Python script files.

## Data analysis 
To be found in **/scripts/data_analysis.ipynb**. Run notebook in order to reproduce.

## Similarity Functions and Article Similarity
To be found in **similarity_functions_and_article_similarity.ipynb**. Run notebook in order to reproduce.

## Weighted Similarity and Votes Similarity
To be found in **weighted_and_votes_similarity.ipynb**. Run notebook in order to reproduce.

## Graph analysis
To be found in **graph_analysis.ipynb**. Run notebook in order to reproduce.

## Text Similarities
This section is more thorough because it requires multiple steps to reproduce.

The text similarities related research and code can be categoriezed into two categories which are also reflected in the split in the following subsections: URL similarities and W2V similarities.

### URL Similarities
The initial step in the URL Similarities related research was to extract the user posts containing web links from the Postings_\*.csv files. This step can be reproduced running the **text_similarities/URLs-preprocess.ipynb** file. Running the code produces the URLs-Postings_\*.csv files that can also be found in the text_similarities/ directory.

The next step is to implement calculating the Jaccard coefficient between a user pair. The code for that can be found in the **text_similarities/URLs-similarities.ipynb** file. The code requires the URLs-Postings_\*.csv files that were generated in the initial step which are also included in the project folder.

### W2V Similarities
For this research, we downloaded an already trained dictionary of words and their corresponding vector weights from the https://www.deepset.ai/german-word-embeddings website. The exact link to the download of the weights is https://int-emb-word2vec-de-wiki.s3.eu-central-1.amazonaws.com/vectors.txt . As of the time of writing (26th January 2023) this README file, both these links are working properly. A guarantee cannot be made for these links to be working. In order to reproduce the research, the vectors.txt file from the second link needs to be copied into the project directory as text_similarities/w2v/vectors.txt . In case the link no longer works, please contact Waldemar Schewzow for him to provide you with the file he used. This file was not put into the repository because it is too big (2.25 GiB).

For the reason that the file is too big, we have created the **text_similarities/make_w2v_pickle.py** script file. This script effectively compresses the data in a lossy way such that it retains 80% of its variability. This compression reduces the file size of the information in the vector.txt file down to 336 MiB. Because Gitlab won't accept a file as big as 336 MiB, the script further splits up the resulting data into 9 files: /text_similarities/w2v/vectors_\*.pkl. These files are included in this repository.

The **text_similarities/w2v_similarities.ipynb** file documents the functions that were written to make user-user w2v comparisons. This file is not necessary to run in order to reproduce any relevant results for the research.

The w2v comparisons relevant for this research are to be found in **text_similarities/w2v-bootstrap-similarities.ipynb**. Seeds were set in this file in order to ensure reproducibility.
