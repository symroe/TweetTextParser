import unittest

from tweet_text_parser import TweetTextParser

import urllib2
import urllib
import json


class TestParseFunctions(unittest.TestCase):

    def test_from_api(self):
        base_url = "https://api.twitter.com/1/statuses/user_timeline.json"
        prams = {
            'include_entities' : 'true',
            'include_rts' : 'true',
            'screen_name' : 'symroe',
            'count' : 10,
            'trim_user' : 'true',
            'exclude_replies' : 'false',
        }
        url = "%s?%s" % (base_url, urllib.urlencode(prams))        

        r = urllib2.urlopen(url)
        p = json.loads(r.read())
        t = TweetTextParser(p)

        self.assertEqual(len(t.parse_all()), 10)
        self.assertTrue('html' in t.parse_all()[0])

    def test_single_tweet(self):
        tweet = {
            "text": "@test is this working? #hopeful",
            "entities": {
              "urls": [
              ],
              "user_mentions": [
                  {
                      "id" : 123,
                      "id_str" : "123",
                      "screen_name" : "test",
                      "name" : "Testing",
                      "indices": [0,5],
                  },
              ],
              "hashtags": [
                  {
                      "text" : "#hopeful",
                      "indices" : [23,31],
                  }
              ]
            }
        }
        t = TweetTextParser(tweet)
        self.assertEqual(
            t.parse_all()[0]['html'], 
            u'<a href="http://twitter.com/test">@test</a> is this working? <a href="http://twitter.com/search/?q=%23#hopeful">#hopeful</a>'
            )
    
if __name__ == '__main__':
    unittest.main()