import json
import string
import re

with open('Cell_Phones_and_Accessories_5.json','r') as file:
  data = file.readlines()
  
filtered_data = []
for line in data:
    review = json.loads(line)
    filtered_review = {
        'reviewText': review['reviewText'],
        'rating': review['overall']
    }
    filtered_data.append(filtered_review)
    
punctuation_list = string.punctuation

stop_words = []
with open("NLTK's list of english stopwords", 'r') as file:
        stop_words = [line.strip() for line in file]
        
Acc = ['battery pack','iphone 4s','usb cable','samsung galaxy', 'screen protector','screen protectors', 'phone case', 'micro usb', 'phone case', 'cell phone', 'charge phone']

Reviews = []

for review in filtered_data:
    # Removing punctuation and converting to lowercase
    no_punct = ''.join(char for char in review['reviewText'] if char not in punctuation_list)
    lower = no_punct.lower()

    # filtering stop words and digits
    words = lower.split()
    filtered_words = [word for word in words if word.lower() not in stop_words and not word.isdigit()]

    # Removing ACC
    filtered_words = [word for word in filtered_words if word not in Acc]

    # Create a review dictionary 
    review_dict = {
        'rating': review['rating'],
        'Review': filtered_words
    }

    Reviews.append(review_dict)
    
#Themantic Analysis
positive_reviews = [review['Review'] for review in Reviews if review['rating'] > 3]
negative_reviews = [review['Review'] for review in Reviews if review['rating'] < 3]

positive_word_freq = {}
negative_word_freq = {}

for review in positive_reviews:
    for word in review:
        if word in positive_word_freq:
            positive_word_freq[word] += 1         #calculating frequency of words in +ive and -ive views
        else:
            positive_word_freq[word] = 1

for review in negative_reviews:
    for word in review:
        if word in negative_word_freq:
            negative_word_freq[word] += 1
        else:
            negative_word_freq[word] = 1

positive_words = []
negative_words = []

# Iterate through all words
for word in set(positive_word_freq.keys()) | set(negative_word_freq.keys()):
    # Get frequency counts for each sentiment (default to 0 if not found)
    positive_count = positive_word_freq.get(word, 0)
    negative_count = negative_word_freq.get(word, 0)

    # Finding sentiment with highest count
    if positive_count > negative_count:
        positive_words.append(word)
    elif negative_count > positive_count:
        negative_words.append(word)
        
# Sort word frequencies in positive and negative reviews
sorted_positive_word_freq = sorted(positive_word_freq.items(), key=lambda x: x[1], reverse=True)
sorted_negative_word_freq = sorted(negative_word_freq.items(), key=lambda x: x[1], reverse=True)

# Top 15 words
top_positive_words = [word for word, freq in sorted_positive_word_freq[:15]]
top_negative_words = [word for word, freq in sorted_negative_word_freq[:15]]

neutral_phrases = []
neutral_word_freq = {}

common_words = set(positive_word_freq.keys()) & set(negative_word_freq.keys())

# Move common bigrams to the list of neutral phrases
for word in common_words:
    neutral_phrases.append(word)

    # Remove common bigrams from positive and negative bigram frequencies
    del positive_word_freq[word]
    del negative_word_freq[word]

    neutral_word_freq[word] = positive_word_freq.get(word, 0) + negative_word_freq.get(word, 0)

# Find the maximum frequency in positive and negative reviews
max_positive_freq = max(positive_word_freq.values(), default=1)
max_negative_freq = max(negative_word_freq.values(), default=1)


weighted_phrases = {}

# Assigning weights to positive phrases
for phrase, frequency in positive_word_freq.items():
    weighted_phrases[phrase] = (frequency / max_positive_freq) * 50

# Assigning weights to negative phrases
for phrase, frequency in negative_word_freq.items():
    weighted_phrases[phrase] = (frequency / max_negative_freq) * -50

# Assigning neutral phrases a weight of 0
for phrase in neutral_phrases:
    weighted_phrases[phrase] = 0
    
def rule_based_sentiment_analysis(text, weighted_phrases):
    
    text_lower = text.lower()
    sentiment_score = 0

    # Calculating sentiment score based on weighted phrases
    for phrase, weight in weighted_phrases.items():
        sentiment_score += len(re.findall(phrase, text_lower)) * weight

    # Determine sentiment based on sentiment score
    if sentiment_score >= 3:
        return ("Positive",sentiment_score)
    elif sentiment_score <= -3:
        return ("Negative",sentiment_score)
    else:
        return ("Neutral",sentiment_score)

with open("review_sentiments.txt", "w") as file:

    for review in filtered_data:
        review_text = review['reviewText']
        
        sentiment = rule_based_sentiment_analysis(review_text, weighted_phrases)
        file.write(f"Review: {review_text}\nSentiment: {sentiment}\n\n")

        
