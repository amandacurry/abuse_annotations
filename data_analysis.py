import argparse
import pandas as pd
from nltk.stem import WordNetLemmatizer


def init_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset",
                        help="one of [slurp, fluent, snips]",
                        default="slurp",
                        required=True)
    parser.add_argument("-p", "--path",
                        help="path to the dataset",
                        required=True)
    return parser.parse_args()



# Function to tokenize the tweets
def custom_tokenize(text):
    """Function that tokenizes text"""
    from nltk.tokenize import word_tokenize
    if not text:
        print('The text to be tokenized is a None type. Defaulting to blank string.')
        text = ''
    return word_tokenize(text)

# Function that applies the cleaning steps
def clean_up(data):
    """Function that cleans up the data into a shape that can be further used for modeling"""
    english = data#[data['lang']=='en'] # extract only tweets in english language
    english.drop_duplicates() # drop duplicate tweets
    english['Input.user'].dropna(inplace=True) # drop any rows with missing tweets
    tokenized = english['Input.user'].apply(custom_tokenize) # Tokenize tweets
    lower_tokens = tokenized.apply(lambda x: [t.lower() for t in x]) # Convert tokens into lower case
    alpha_only = lower_tokens.apply(lambda x: [t for t in x if t.isalpha()]) # Remove punctuations
    no_stops = alpha_only.apply(lambda x: [t for t in x if t not in stopwords.words('english')]) # remove stop words
    no_stops.apply(lambda x: [x.remove(t) for t in x if t=='rt']) # remove acronym "rt"
    no_stops.apply(lambda x: [x.remove(t) for t in x if t=='https']) # remove acronym "https"
    no_stops.apply(lambda x: [x.remove(t) for t in x if t=='twitter']) # remove the word "twitter"
    no_stops.apply(lambda x: [x.remove(t) for t in x if t=='retweet']) # remove the word "retweet"
    return no_stops
    

def main():
    #args = init_argparse()
    # Read and clean the data
    #warnings.filterwarnings("ignore")
    use_cols = ['text', 'lang'] # specify the columns
    path = 'tweets.csv' # path to the raw dataset
    data_iterator = pd.read_csv(path, usecols=use_cols, chunksize=50000)
    #chunk_list = []
    #for data_chunk in data_iterator:
    tidy_data = clean_up(data_chunk)
    #chunk_list.append(filtered_chunk)
    #idy_data = pd.concat(chunk_list)


if __name__ == "__main__":
    main()
