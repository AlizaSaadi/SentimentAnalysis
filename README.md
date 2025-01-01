This Python script performs sentiment analysis on customer reviews from the Cell_Phones_and_Accessories_5.json dataset. It uses a rule-based approach to classify reviews as Positive, Negative, or Neutral based on word frequencies and weighted phrases. The results are written to a text file, review_sentiments.txt.

Features
Data Preprocessing:

Extracts relevant fields (reviewText and rating) from the dataset.
Cleans reviews by removing punctuation, stopwords, digits, and specific accessory-related terms.
Thematic Analysis:

Separates reviews into Positive, Negative, and Neutral categories based on ratings.
Calculates word frequencies for each sentiment category.
Weighted Phrases:

Assigns weights to phrases based on their frequency in positive and negative reviews.
Neutral phrases are given a weight of 0.
Rule-Based Sentiment Analysis:

Determines the sentiment of individual reviews using weighted phrase analysis.
Outputs the sentiment and a corresponding score.
Output:

Writes each review's text along with its computed sentiment to a file.

Key Functions
Data Cleaning:

Removes irrelevant terms and prepares reviews for analysis.
Sentiment Classification:

Computes sentiment scores based on weighted phrases.
Result Storage:

Saves processed reviews and their sentiments to a text file for further use.
