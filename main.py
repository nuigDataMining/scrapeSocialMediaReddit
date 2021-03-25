# to time our class
import time
# separate file with reddit credentials
import creds
# api for reading reddit
import praw

import pprint as pp
import pandas as pd
import pickle

from praw.models import MoreComments
from operator import attrgetter

start = time.time()

# initialise the instance of reddit
reddit = praw.Reddit(client_id = creds.client_id, \
                        client_secret = creds.client_secret, \
                        user_agent = creds.user_agent, \
                        username = creds.username, \
                        password = creds.password)

# create a class for holding each thread
# included is sample desireable characteristics + the commment content
class commentClass:
    def __init__(self, title = "title"):
        self._title = title
        self._comments = []
        self._created = 0
        self._score = 0
        self._id = 0
        self._num_comments = 0

    def __len__(self):
        return (len(self._comments))

    def __getitem__(self, position):
        return self._comments[position]

# class for holding each instance of the threads
class masterClass:

    def __init__(self):
        self._classes = []
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._classes):
            raise StopIteration

        index = self._index
        self._index += 1
        return self._classes[index]._comments

    def __getitem__(self, position):
        return self._classes[position]


    def sort_length(self, attri_key):
        sorted_comments = sorted(self._classes, key = attrgetter(attri_key))

        return sorted_comments


# running the main methods
def main():
    #harvestCommentReplies()
    # methods creates the class list and extracts information
    megaClass = createClass()
    # pickle the class so can be run just once then saved for later inspection
    # f = open("pickleMegaClass", "wb")
    # pickle.dump(megaClass, f)

    # file = open("pickleMegaClass", "rb")
    # megaClass = pickle.load(file)
    # print(len(megaClass._classes[0]))

# methods creates a class per thread instance and populates a masterclass with resulting threads
def createClass():
    list_of_sub_ids = lookAtSubreddit()
    megaClass = masterClass()
    for comment in list_of_sub_ids:
        # new instance of thread class
        cls = commentClass()
        # meta data
        cls._title = comment.title
        # method extracts all comment content
        cls._comments = breathTraverse(comment)
        cls._created = comment.created_utc
        cls._score = comment.score
        cls._id = comment.id
        cls._num_comments = comment.num_comments
        megaClass._classes.append(cls)

    # list of classes can be sorted by thread_class_attributes for required task
    ordered_list_created = megaClass.sort_length(attri_key = "_created")

    return megaClass


# this method iterates over each comment per submission, opens all replies and returns a list of content
def breathTraverse(id):
    sub = reddit.submission(id = id)

    # to avoid commentForest issue - destructive call only once
    sub.comments.replace_more(limit = None)
    # opens out all of the initial comments
    comment_queue = sub.comments[:]
    # list for holding all text
    all_comments = []
    # iterate over comment queue
    # loop increase in size as new replies are added until all comments are found
    while comment_queue:
        # extract comment
        comment = comment_queue.pop(0)
        # add comment to class comment list
        all_comments.append(comment.body)
        # expand on any replies
        comment_queue.extend(comment.replies)

    return all_comments





def harvestCommentReplies():
    #print("going in here")
    id = "kqedi9"
    sub = reddit.submission(id = id)
    sub.comments.replace_more(limit = None)

    print(sub.url)

    for comment in sub.comments[:1]:
        print(pp.pprint(dir(comment)))
        #print(comment.author)
        #print(comment.body)
        #print(comment.created)
        #print(comment.id)
        #print(comment.parent_id)
        #print(comment.replies)
        #print(comment.score)
        #print(sub.comments[0].replies[0].score)
        #print(comment.ups)

        # for reply in comment.replies:
        #     print()
        #     print(reply.body)
        #     print(10*"-")

    # for comment in sub.comments[:1]:
    #     print(comment.replies)
    #
    # print(sub.comments[0].body)





# method extracts from hot desired num of comments 
def lookAtSubreddit(limit = 1000 ):
    # top // new // hot
    sub = reddit.subreddit("coronavirus").hot(limit= limit)

    return sub



if __name__ == "__main__":
    main()


print("\n"  + 50*"#")
print(time.time() - start)
print(50*"#")
