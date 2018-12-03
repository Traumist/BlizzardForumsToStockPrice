# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 04:44:50 2018

@author: traumist
"""

import bs4 as bs
import urllib.request
from textblob import TextBlob
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import time
from urllib.parse import urljoin
# =============================================================================
#  =============================================================================
#  TO DO:
#       go further back on forums
#       naieve bayes sentiment    
#      linear regression line
#  =============================================================================
# =============================================================================

plt.style.use('seaborn-darkgrid')


owGen = 'https://us.forums.blizzard.com/en/overwatch/c/general-discussion'
owComp = 'https://us.forums.blizzard.com/en/overwatch/c/competitive-discussion'
owPTR = 'https://us.forums.blizzard.com/en/overwatch/c/ptr-feedback'
owStory = 'https://us.forums.blizzard.com/en/overwatch/c/story-discussion'
wowGen = 'https://us.forums.blizzard.com/en/wow/c/community/general-discussion'
wowVan = 'https://us.forums.blizzard.com/en/wow/c/community/classic-discussion'
wowDung = 'https://us.forums.blizzard.com/en/wow/c/gameplay/dungeons-raids-scenarios'
wowProf = 'https://us.forums.blizzard.com/en/wow/c/gameplay/professions'
wowPet = 'https://us.forums.blizzard.com/en/wow/c/gameplay/pet-battles'
wowMog = 'https://us.forums.blizzard.com/en/wow/c/gameplay/transmogrification'
wowQuest = 'https://us.forums.blizzard.com/en/wow/c/gameplay/quests'
wowAchieve = 'https://us.forums.blizzard.com/en/wow/c/gameplay/achievements'
wowBgs = 'https://us.forums.blizzard.com/en/wow/c/pvp/battlegrounds'
wowWPvp = 'https://us.forums.blizzard.com/en/wow/c/pvp/warmode-world-pvp'
HSPlay = 'https://us.battle.net/forums/en/hearthstone/22814023/'
HSAdventure = 'https://us.battle.net/forums/en/hearthstone/14927209/'
HSCommunity = 'https://us.battle.net/forums/en/hearthstone/10591463/'
HSArena = 'https://us.battle.net/forums/en/hearthstone/10591717/'
d3Gen = 'https://us.battle.net/forums/en/d3/3354739/'
d3New = 'https://us.battle.net/forums/en/d3/11864305/'
hotsGen = 'https://us.forums.blizzard.com/en/heroes/c/general-discussion'
hotsComp = 'https://us.forums.blizzard.com/en/heroes/c/competitive-discussion'
scGen = 'https://us.battle.net/forums/en/starcraft/22814089/'
scCampaign = 'https://us.battle.net/forums/en/starcraft/22814090/'
sc2Gen = 'https://us.battle.net/forums/en/sc2/40568/'
sc2Campaign = 'https://us.battle.net/forums/en/sc2/21982568/'

forumList = [owGen, owComp, owPTR, owStory, wowGen, wowVan, wowDung, wowProf,
             wowPet, wowMog, wowQuest, wowAchieve, wowBgs, wowWPvp, HSPlay,
             HSAdventure, HSCommunity, HSArena, d3Gen, d3New, hotsGen, hotsComp,
             scGen, scCampaign, sc2Gen, sc2Campaign]

sectionList = ['owGen', 'owComp', 'owPTR', 'owStory', 'wowGen', 'wowVan',
               'wowDung', 'wowProf', 'wowPet', 'wowMog', 'wowQuest',
               'wowAchieve', 'wowBgs', 'wowWPvp', 'HSPlay','HSAdventure',
               'HSCommunity', 'HSArena', 'd3Gen', 'd3New','hotsGen',
               'hotsComp', 'scGen', 'scCampaign', 'sc2Gen', 'sc2Campaign']

differentForums = [ 'HSPlay','HSAdventure','HSCommunity', 'HSArena',
                   'd3Gen', 'd3New', 'scGen', 'scCampaign',
                   'sc2Gen', 'sc2Campaign']

labels = ['threadTitle','datePosted','author','polarity','section']
    
def getThreads(baseForum, section):
    threadLinks = []
    sauce = urllib.request.urlopen(baseForum)
    genSoup = bs.BeautifulSoup(sauce, 'lxml')
    if section in differentForums:
        for useless in genSoup(class_='ForumTopic-details'):
            useless.decompose()
        for useless in genSoup(class_='ForumTopic-timestamp'):
            useless.decompose()
        for useless in genSoup(class_='ForumTopic-type'):
            useless.decompose()
        threads = genSoup.find_all(class_="ForumTopic")
        for th in threads:
            tl = urljoin(baseForum,th['href'])
            threadLinks.append(tl)
        return threadLinks
    else:
        threads = genSoup.find_all(itemprop='url')
        
        for thread in threads:
            if thread.get('content') is not None:
        #        print(thread.get('content'))
                threadLinks.append(thread.get('content'))
        return threadLinks

def analyzeThreads(threadLinks, section):
    posts = []
    for link in threadLinks:
        sauce = urllib.request.urlopen(link)
        soup = bs.BeautifulSoup(sauce, 'lxml')
#        datePosted = soup.find('time')
#        datePosted = datePosted.get('datetime')
#        datePosted = datetime.strptime(datePosted, '%Y-%m-%dT%XZ')
        threadTitle = soup.title.text
        threadTitle = threadTitle.split(' - ')[0]

        if section in differentForums:
            for blockquote in soup("blockquote"):
                blockquote.decompose()
            nav = soup.find_all('div', class_='TopicPost-bodyContent')
            times = soup.find_all(class_='TopicPost-timestamp')
            creators = soup.find_all(class_='Author-name--profileLink')
#            for p in nav:
#                print(p.text)
#                print('*********************************************')
#                print(t.get('data-tooltip-content'))
#                print(a.text)
#            print(len(creators),len(nav),len(times))
            return posts
        else:            
            #Remove all quotes
            for blockquote in soup("blockquote"):
                blockquote.decompose()
       
            ##find all post text
            nav = soup.find_all('div', itemprop='articleBody')
            times = soup.find_all('time', itemprop='datePublished')
            creators = soup.find_all(itemprop='author')
            #create list of post text and polarity/sentiment
    
            for post, t, a in zip(nav, times, creators):
                analysis = TextBlob(post.text)
                datePosted = t.get('datetime')
                datePosted = datetime.strptime(datePosted, '%Y-%m-%dT%XZ')
                author = a.text
                data = [threadTitle, datePosted, author, 
                        analysis.sentiment.polarity, section]
                
                if (analysis.sentiment.subjectivity) > 0.80:
                    posts.append(data)                        
    return posts

#toAnalyze = getThreads(sc2Gen,'sc2Gen')
#analyzeThreads(['https://us.battle.net/forums/en/sc2/topic/20769579839'], 'sc2Gen')
while True:
    print('starting', datetime.now())
    for l in range(len(forumList)):
        toAnalyze = getThreads(forumList[l],sectionList[l])
        data = analyzeThreads(toAnalyze, sectionList[l])
        df = pd.DataFrame.from_records(data, columns=labels)
        with open('75subjectivity.csv', 'a+', encoding='utf-8') as f:
            df.to_csv(f, sep=',', header=False, encoding='utf-8')
        print('added',len(data), 'entries to csv from section:',sectionList[l])
    print('Done',datetime.now())
    time.sleep(1800)
#   
