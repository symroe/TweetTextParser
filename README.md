# Tweet Text Parser #

This class takes the JSON returned from twitter's API and converts the tweet text in to HTML using the entities from the API, rather than trying to parse the text manually.

## Basic usage ##

    tweet = {
        "text" : "Some tweet",
        "entities" {
            #See the API example https://dev.twitter.com/docs/tweet-entities
        }
    }
    t = TweetTextParser(tweet)
    parsed_tweet = t.parse_all()[0]
    parsed_tweet['html]

Note, the whole tweet is returned, with an additional key called `html`.

Alternatively, a list of tweets can be passed, and each one will have an `HTML` key added to it.

## Templates ##

If you'd like to change the HTML output of the tweet, you can use pythons `string.Template` to edit them.  At the moment, only the first half of the replacement is templated, as the second half is always "&lt;/a&gt;" by default.

There are 4 templates that correspond to the different types of entity:

* media_template
* hashtags_template
* user_mentions_template 
* url_template

To changes a template:

    from string import Template
    t = TweetTextParser(tweet)
    t.media_template = Template("""<a href="$url"><img src="$url" />""")
    
    parsed_tweet = t.parse_all()[0]
    parsed_tweet['html]


    