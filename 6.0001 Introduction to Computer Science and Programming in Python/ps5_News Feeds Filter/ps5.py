# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = getattr(entry, 'guid', '')
        title = translate_html(getattr(entry, 'title', ''))
        link = getattr(entry, 'link', '')
        description = translate_html(getattr(entry, 'description', ''))
        pubdate = translate_html(getattr(entry, 'published', ''))

        # UPDATED DATE PARSING LOGIC
        try:
            # Try the old standard format (RFC 822)
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
        except ValueError:
            try:
                # Try format with numeric timezone offset
                pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")
            except ValueError:
                # Try the MODERN ISO format (e.g., 2025-12-31T21:45:26Z)
                try:
                    pubdate = datetime.strptime(pubdate, "%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    # If all else fails, just use the current time so it doesn't crash
                    pubdate = datetime.now()

        # Ensure the date is timezone-aware (assume GMT/UTC if missing)
        if pubdate.tzinfo is None:
            pubdate = pubdate.replace(tzinfo=pytz.timezone("GMT"))

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_description(self):
        return self.description
    def get_link(self):
        return self.link
    def get_pubdate(self):
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__ (self, phrase):
        Trigger.__init__(self)
        self.phrase = phrase.lower()
    def is_phrase_in (self, text):
        cleaned_text = ""
        for char in text.lower():
            if char in string.punctuation:
               cleaned_text += " " 
            else:
                cleaned_text += char
        phrase_list = self.phrase.split()
        text_list = cleaned_text.split()
        for i in range(len(text_list) - len(phrase_list) + 1):
            if text_list[i : i + len(phrase_list)] == phrase_list:
                return True
        return False
                   

# Problem 3
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)
    def evaluate(self, story):
        title = story.get_title()
        return self.is_phrase_in(title)
        

# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)
    def evaluate(self, story):
        description = story.get_description()
        return self.is_phrase_in(description)

# TIME TRIGGERS

# Problem 5
# TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, time):
        dt = datetime.strptime(time, '%d %b %Y %H:%M:%S')
        self.time = dt
        self.time = dt.replace(tzinfo=pytz.timezone("EST"))
# Problem 6
# BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def __init__(self, time):
       TimeTrigger. __init__(self, time)
    def evaluate(self, story):
        story_date = story.get_pubdate()
        if story_date.tzinfo is None:
            story_date = story_date.replace(tzinfo=pytz.timezone("EST"))   
        return story_date < self.time

class AfterTrigger(TimeTrigger):
    def __init__(self, time):
       TimeTrigger. __init__(self, time)
    def evaluate(self, story):
        story_date = story.get_pubdate()
        if story_date.tzinfo is None:
            story_date = story_date.replace(tzinfo=pytz.timezone("EST"))   
        return story_date > self.time
# COMPOSITE TRIGGERS

# Problem 7
# NotTrigger
class NotTrigger(Trigger):
    def __init__ (self, other_trigger):
        Trigger.__init__(self)
        self.other_trigger = other_trigger
    def evaluate(self, story):
        return not self.other_trigger.evaluate(story)
# Problem 8
# AndTrigger
class AndTrigger(Trigger):
    def __init__ (self, trigger1, trigger2):
        Trigger.__init__(self)
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)

# Problem 9
# OrTrigger
class OrTrigger(Trigger):
    def __init__ (self, trigger1, trigger2):
        Trigger.__init__(self)
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate(self, story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    filtered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered_stories.append(story)
    return filtered_stories

#======================
# User-Specified Triggers
#======================
# Problem 11
# Problem 11
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    trigger_dict = {}
    trigger_list = []

    for line in lines:
        parts = line.split(',')
        
        # SAFETY CHECK: If a line doesn't have enough parts, skip it
        if len(parts) < 2:
            print(f"Skipping malformed line: '{line}'")
            continue

        if parts[0] == 'ADD':
            for name in parts[1:]:
                # SAFETY CHECK: Only add if the trigger actually exists
                if name in trigger_dict:
                    trigger_list.append(trigger_dict[name])
                else:
                    print(f"Warning: Trigger '{name}' not found in definitions.")
        else:
            name = parts[0]
            type = parts[1]
            args = parts[2:]
            
            # Create the triggers based on type
            if type == 'TITLE':
                trigger_dict[name] = TitleTrigger(args[0])
            elif type == 'DESCRIPTION':
                trigger_dict[name] = DescriptionTrigger(args[0])
            elif type == 'AFTER':
                trigger_dict[name] = AfterTrigger(args[0])
            elif type == 'BEFORE':
                trigger_dict[name] = BeforeTrigger(args[0])
            elif type == 'NOT':
                trigger_dict[name] = NotTrigger(trigger_dict[args[0]])
            elif type == 'AND':
                trigger_dict[name] = AndTrigger(trigger_dict[args[0]], trigger_dict[args[1]])
            elif type == 'OR':
                trigger_dict[name] = OrTrigger(trigger_dict[args[0]], trigger_dict[args[1]])
    
    return trigger_list


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

