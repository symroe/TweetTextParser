#-*- coding: utf-8 -*-
from string import Template

class TweetTextParser():
    """
    
    Requires a dict or list of dicts, each containing at least two key/value
    pairs:
    
        * test:         the tweet text
        * entities:     a mapping of entities, as specified in the API docs: 
                        https://dev.twitter.com/docs/tweet-entities

    """
    
    def __init__(self, tweets):
        if isinstance(tweets, dict):
            tweets = [tweets,]
        self.tweets = tweets
        self.parsed = []
        
        self.media_template = Template("""<a href="$url">""")
        self.hashtags_template = Template("""<a href="http://twitter.com/search/?q=%23$text">""")
        self.user_mentions_template = Template("""<a href="http://twitter.com/$screen_name">""")
        self.url_template = Template("""<a href="$url">""")
    
    def parse_all(self):
        for tweet in self.tweets:
            self.parsed.append(self.parse_tweet(tweet))
        return self.parsed

    def parse_tweet(self, tweet):
        if tweet.get('retweeted_status'):
            tweet_text = tweet['retweeted_status']['text']
            entities = tweet['retweeted_status']['entities']
        else:
            tweet_text = tweet['text']
            entities = tweet['entities']
        
        
        text_list = list(tweet_text)
        text_list.append('') # So the offsets work properly
                    
        for url in entities['urls']:
            indices = tuple(url['indices'])
            text_list[indices[0]] =  self.url_template.substitute(url) + text_list[indices[0]]
            text_list[indices[1]] = "</a>%s" % text_list[indices[1]]
                
        for url in entities['user_mentions']:
            indices = tuple(url['indices'])
            text_list[indices[0]] = self.user_mentions_template.substitute(url) + text_list[indices[0]]
            text_list[indices[1]] = "</a>%s" % text_list[indices[1]]
                
        for url in entities['hashtags']:
            indices = tuple(url['indices'])
            text_list[indices[0]] = self.hashtags_template.substitute(url) + text_list[indices[0]]
            text_list[indices[1]] = "</a>%s" % text_list[indices[1]]

        for url in entities.get('media', []):
            indices = tuple(url['indices'])
            text_list[indices[0]] = self.media_template.substitute(url) + text_list[indices[0]]
            text_list[indices[1]] = "</a>%s" % text_list[indices[1]]
        
        tweet['html'] = u"".join(text_list)
        return tweet

