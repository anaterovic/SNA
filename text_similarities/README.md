# Text Similarities
 
This directory includes the project files intended to capture similarity measures that are related to text contents. More particularly, we have decided to base our similarity measures on (i) hyperlinks that users have posted in the articles (ii) w2v vector measures.

## Hyperlink Similarities

"URLs.ipynb" extracts urls from users and saves the comments including URLs into the URLs-Postings*.csv files. It's to be noted that only 3% of posts feature hyperlinks. Only few people have a representative amount of links they post. However, for the subset of users that do post things regularly, it's a good tool to measure similarities.

WIP: Create a database of userpairs and their similarities. However, I believe the file should also feature the amounts of hyperlinks both the users posted. Users with few posts may happen to have high similarity if they only posted one link each which happens to be the same. If you have a bigger sample of what types of hyperlinks users are associated with, we believe that it's more representative and useful for actual measuring of similarity.

## W2V similarities

For word choice similarities we decided to go with W2V embeddings. Those can be either trained manually or ready-to-use embeddings can be used. As our data is relatively limited and there exist embeddings online which are trained on huge datasets, we decided to go for the latter. Making a web search for German word embeddings, we have found https://www.deepset.ai/german-word-embeddings which features W2V vectors that were trained on Wikipedia data. Each word is assigned 300 float values representing directions in a 300 dimensions space.

The original file takes up 1.9 GiB of space. In order to make the embeddings easier to handle, we first considered how to decrease the space the embeddings take up. The lossless method of ZIP-compressing the file managed to reduce the file size to 1.4 GiB. For a next step, we considered lossy compression by reducing the dimensions using PCA while retaining a given amount of variance. We managed to retain 80% of the variance of the original embeddings file with PCA while reducing the dimensionality from 300 down to 50. The scipt make_w2v_pickle.py includes all the relevant code for this.

The w2v_similarities.ipynb notebook implements functions that allow measuring similarities between two users. For more information, refer to the notebook file. The w2v-bootstrap-similarities.ipynb then uses these functions for deriving the relevant findings for the project.
