#!/usr/bin/python
import praw
import re

phrasesToSplitBy = ['chapter ', 'ch ', 'ch. ', '(ch', '- ']
reddit = praw.Reddit('previous_chapter_bot')
subreddit = reddit.subreddit("manga")

def getText(commentToCheck):
    title = commentToCheck.submission.title
    if re.search("[DISC]", title, re.IGNORECASE):
        chapterNumber = getChapterNumber(title)
        previousChapterNumber = int(chapterNumber) -1
        mangaName = getMangaName(title)
        searchResults = getPreviousChapter(mangaName, str(previousChapterNumber))
        # if (len(searchResults) == 0):
        #     return "no link found :("
        # todo - check if empty
        previousChapter = list(searchResults)[0]
        return "[[DISC] {mangaName} {number}]({link})".format(mangaName=mangaName,number=previousChapterNumber,link=previousChapter.permalink)
    else:
        return "not a discussion thread, sorry"


def getPreviousChapter(mangaName, chapterNumber):
    query = mangaName + " " + chapterNumber
    print("searching for " + query)
    return subreddit.search(query)

def getChapterNumber(threadTitle):
    return re.findall("\d+", threadTitle)[-1]

def getMangaName(threadTitle):
    mangaName = threadTitle.split("[DISC]")[1].lower()
    for word in phrasesToSplitBy:
        mangaName = mangaName.split(word)[0]
    return mangaName

print("starting bot")
for comment in subreddit.stream.comments(skip_existing=True):
    if re.search("!previousChapter", comment.body, re.IGNORECASE):
        try:
            previousChapterLink = getText(comment)
            comment.reply(previousChapterLink)
            print(previousChapterLink)
        except Exception:
            print(Exception)

