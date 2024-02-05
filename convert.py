#!/usr/bin/env python3
import os
import json
import sqlite3
import xml.etree.ElementTree as ET

def go():
    remove_old_db()

    conn = sqlite3.connect('stack.db')
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA synchronous = normal')


    create_schema(conn)

    import_users(conn)
    import_badges(conn)
    import_posts(conn)
    import_post_history(conn)
    import_post_links(conn)
    import_votes(conn)
    import_comments(conn)
    import_tags(conn)
    create_indexes(conn)
    conn.commit()
    conn.close()


def remove_old_db():
    try:
        os.remove('stack.db')
    except FileNotFoundError:
        pass

def create_schema(conn):
    f = open('schema.sql')
    conn.executescript(f.read())
    f.close()

def create_indexes(conn):
    f = open('indexes.sql')
    conn.executescript(f.read())
    f.close()


def timestamp(ts):
    # Switch from ISO8601 to SQL format
    return ts.replace('T', ' ')

def import_badges(conn):
    tree = ET.parse('input/Badges.xml')
    rows = tree.getroot()
    for row in rows:
        attrs = row.attrib
        cur = conn.execute('INSERT INTO Badges(Id, UserId, Name, Date, Class, TagBased) VALUES (?, ?, ?, ?, ?, ?)',
                     [
                         int(attrs['Id']),
                         int(attrs['UserId']),
                         attrs['Name'],
                         timestamp(attrs['Date']),
                         int(attrs['Class']),
                         int(attrs['TagBased'] == 'True')
                     ])


def import_users(conn):
    tree = ET.parse('input/Users.xml')
    rows = tree.getroot()
    for row in rows:
        attrs = row.attrib
        # print(attrs)
        cur = conn.execute('INSERT INTO Users(Id, Reputation, CreationDate, DisplayName, LastAccessDate, Location, AboutMe, Views, Upvotes, Downvotes, WebsiteUrl, AccountId) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                     [
                         int(attrs['Id']),
                         int(attrs['Reputation']),
                         timestamp(attrs['CreationDate']),
                         attrs['DisplayName'],
                         timestamp(attrs['LastAccessDate']),
                         attrs.get('Location', ''),
                         attrs.get('AboutMe', ''),
                         int(attrs['Views']),
                         int(attrs['UpVotes']),
                         int(attrs['DownVotes']),
                         attrs.get('WebsiteUrl', ''),
                         None if 'AccountId' not in attrs else int(attrs['AccountId'])
                     ])

def post_type(ptid):
    if ptid == 1: return 'question'
    if ptid == 2: return 'answer'
    if ptid == 3: return 'orphaned-tag-wiki'
    if ptid == 4: return 'tag-wiki-excerpt'
    if ptid == 5: return 'tag-wiki'
    if ptid == 6: return 'moderation-nomination'
    if ptid == 7: return 'wiki-placeholder'
    if ptid == 8: return 'privilege-wiki'
    raise Exception('unknown ptid {}'.format(ptid))

def tags(x):
    return json.dumps([tag.strip('>') for tag in x.split('<') if tag])

def import_posts(conn):
    tree = ET.parse('input/Posts.xml')
    rows = tree.getroot()
    for row in rows:
        attrs = row.attrib
        cur = conn.execute('INSERT INTO Posts(Id, PostTypeID, AcceptedAnswerId, ParentID, CreationDate, CommunityOwnedDate, ClosedDate, Score, ViewCount, Body, OwnerUserId, LastEditorUserId, LastEditDate, LastActivityDate, Title, Tags, AnswerCount, CommentCount, FavoriteCount, OwnerDisplayName, ContentLicense) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                     [
                         int(attrs['Id']),
                         int(attrs['PostTypeId']),
                         int(attrs['AcceptedAnswerId']) if 'AcceptedAnswerId' in attrs else None,
                         int(attrs['ParentId']) if 'ParentId' in attrs else None,
                         timestamp(attrs['CreationDate']),
                         timestamp(attrs['CommunityOwnedDate']) if 'CommunityOwnedDate' in attrs else None,
                         timestamp(attrs['ClosedDate']) if 'ClosedDate' in attrs else None,
                         int(attrs['Score']),
                         int(attrs.get('ViewCount', 0)),
                         attrs['Body'],
                         int(attrs['OwnerUserId']) if 'OwnerUserId' in attrs else None,
                         int(attrs['LastEditorUserId']) if 'LastEditorUserId' in attrs else None,
                         timestamp(attrs['LastEditDate']) if 'LastEditDate' in attrs else None,
                         timestamp(attrs['LastActivityDate']),
                         attrs['Title'] if 'Title' in attrs else None,
                         tags(attrs['Tags']) if 'Tags' in attrs else None,
                         int(attrs['AnswerCount']) if 'AnswerCount' in attrs else 0,
                         int(attrs['CommentCount']) if 'CommentCount' in attrs else 0,
                         int(attrs['FavoriteCount']) if 'FavoriteCount' in attrs else 0,
                         attrs.get('OwnerDisplayName'),
                         attrs['ContentLicense']
                     ])


def import_post_history(conn):
    tree = ET.parse('input/PostHistory.xml')
    rows = tree.getroot()
    for row in rows:
        attrs = row.attrib
        cur = conn.execute('INSERT INTO PostHistory(Id, PostHistoryTypeId, PostId, RevisionGUID, CreationDate, UserId, UserDisplayName, Comment, Text, ContentLicense) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                     [
                         int(attrs['Id']),
                         int(attrs['PostHistoryTypeId']),
                         int(attrs['PostId']),
                         attrs['RevisionGUID'],
                         timestamp(attrs['CreationDate']),
                         None if 'UserId' not in attrs else int(attrs['UserId']),
                         attrs.get('UserDisplayName'),
                         attrs.get('Comment'),
                         attrs.get('Text', ''),
                         attrs.get('ContentLicense', '')
                     ])


def import_post_links(conn):
    tree = ET.parse('input/PostLinks.xml')
    rows = tree.getroot()
    for row in rows:
        attrs = row.attrib
        cur = conn.execute('INSERT INTO PostLinks(Id, CreationDate, PostId, RelatedPostId, LinkTypeId) VALUES (?, ?, ?, ?, ?)',
                     [
                         int(attrs['Id']),
                         timestamp(attrs['CreationDate']),
                         int(attrs['PostId']),
                         int(attrs['RelatedPostId']),
                         int(attrs['LinkTypeId'])
                     ])



def vote_type(vtid):
    if vtid == 1: return 'accepted'
    if vtid == 2: return 'up'
    if vtid == 3: return 'down'
    if vtid == 4: return 'offensive'
    if vtid == 5: return 'favorite'
    if vtid == 6: return 'close'
    if vtid == 7: return 'reopen'
    if vtid == 8: return 'bounty-start'
    if vtid == 9: return 'bounty-close'
    if vtid == 10: return 'delete'
    if vtid == 11: return 'undelete'
    if vtid == 12: return 'spam'
    if vtid == 15: return 'mod-review'
    if vtid == 16: return 'edit-approved'

    raise Exception('unknown vtid {}'.format(vtid))

def import_votes(conn):
    tree = ET.parse('input/Votes.xml')
    rows = tree.getroot()
    for row in rows:
        attrs = row.attrib
        cur = conn.execute('INSERT INTO Votes(Id, PostId, VoteTypeId, CreationDate, UserId, BountyAmount) VALUES (?, ?, ?, ?, ?, ?)',
                     [
                         int(attrs['Id']),
                         int(attrs['PostId']),
                         int(attrs['VoteTypeId']),
                         timestamp(attrs['CreationDate']),
                         int(attrs['UserId']) if 'UserId' in attrs else None,
                         int(attrs['BountyAmount']) if 'BountyAmount' in attrs else None
                     ])


def import_comments(conn):
    tree = ET.parse('input/Comments.xml')
    rows = tree.getroot()
    for row in rows:
        attrs = row.attrib

        # 487 of 19,651 rows lack a user id, skip em.
        # if not 'UserId' in attrs:
        #     continue
        cur = conn.execute('INSERT INTO Comments(Id, PostId, Score, Text, CreationDate, UserId, UserDisplayName, ContentLicense) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                     [
                         int(attrs['Id']),
                         int(attrs['PostId']),
                         int(attrs.get('Score', 0)),
                         attrs['Text'],
                         timestamp(attrs['CreationDate']),
                         None if 'UserId' not in attrs else int(attrs['UserId']),
                         None if 'UserDisplayName' not in attrs else attrs['UserDisplayName'],
                         attrs['ContentLicense']
                     ])

def import_tags(conn):
    tree = ET.parse('input/Tags.xml')
    rows = tree.getroot()
    for row in rows:
        attrs = row.attrib
        cur = conn.execute('INSERT INTO Tags(Id, TagName, Count, ExcerptPostId, WikiPostId, IsModeratorOnly, IsRequired) VALUES (?, ?, ?, ?, ?, ?, ?)',
                     [
                         int(attrs['Id']),
                         attrs['TagName'],
                         int(attrs['Count']),
                         None if 'ExcerptPostId' not in attrs else int(attrs['ExcerptPostId']),
                         None if 'WikiPostId' not in attrs else int(attrs['WikiPostId']),
                         int(attrs.get("IsModeratorOnly") == 'True'),
                         int(attrs.get("IsRequired") == 'True'),
                     ])

if __name__ == '__main__':
    go()

