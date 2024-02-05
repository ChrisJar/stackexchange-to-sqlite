CREATE TABLE Users(
  Id integer not null primary key,
  Reputation int not null,
  Views int not null,
  Upvotes int not null,
  Downvotes int not null,
  CreationDate text not null,
  DisplayName text not null,
  LastAccessDate text not null,
  Location text not null,
  AboutMe text not null,
  WebsiteUrl text not null,
  AccountId int
);

CREATE TABLE Badges(
  Id integer not null primary key,
  UserId int not null references Users(Id),
  Name text not null,
  Date text not null,
  Class int not null,
  TagBased int not null
);

CREATE TABLE Posts(
  Id integer not null primary key,
  -- post_type_id text not null check (post_type_id in ('question', 'answer', 'orphaned-tag-wiki', 'tag-wiki-excerpt', 'tag-wiki', 'moderation-nomination', 'wiki-placeholder', 'privilege-wiki')),
  PostTypeId int not null,
  Score int not null,
  ViewCount int not null,
  AnswerCount int not null,
  CommentCount int not null,
  FavoriteCount int not null,
  CreationDate text not null,
  ClosedDate text,
  AcceptedAnswerId int references Posts(Id),
  ParentId int references Posts(Id),
  OwnerUserId int references Users(Id),
  CommunityOwnedDate text,
  Tags text,
  Title text,
  Body text not null,
  LastEditorUserId int references Users(Id),
  LastEditDate text,
  LastActivityDate text not null,
  OwnerDisplayName text,
  ContentLicense text not null
);

CREATE TABLE PostHistory(
  Id int not null primary key,
  PostHistoryTypeId int not null,
  PostId int not null references Posts(Id),
  RevisionGUID text not null,
  CreationDate text not null,
  UserId  int references Users(Id),
  UserDisplayName text,
  Comment text,
  Text text not null,
  ContentLicense text not null
);

CREATE TABLE PostLinks(
  Id int not null primary key,
  CreationDate text not null,
  PostId int not null references Posts(Id),
  RelatedPostId int not null references Posts(Id),
  LinkTypeId int not null
);

CREATE TABLE Votes(
  Id integer not null primary key,
  PostId int not null references Posts(Id),
  -- VoteTypeId text not null check (vote_type in ('accepted', 'up', 'down', 'offensive', 'favorite', 'close', 'reopen', 'bounty-start', 'bounty-close', 'delete', 'undelete', 'spam', 'mod-review', 'edit-approved')),
  VoteTypeId int not null,
  CreationDate text not null,
  UserId int references Users(Id),
  BountyAmount int
);

CREATE TABLE Comments(
  Id integer not null primary key,
  PostId int not null references Posts(Id),
  UserId int references Users(Id),
  CreationDate text not null,
  Score int not null,
  Text text not null,
  UserDisplayName text,
  ContentLicense text not null
);

CREATE TABLE Tags(
  Id integer not null primary key,
  TagName text not null,
  Count int not null,
  ExcerptPostId int references Posts(Id),
  WikiPostId int references Posts(Id),
  IsModeratorOnly int not null,
  IsRequired int not null
);

-- CREATE VIEW questions AS
-- SELECT
--   id,
--   score,
--   views,
--   answers,
--   comments,
--   favorites,
--   creation_date,
--   closed_date,
--   accepted_answer_id,
--   owner_user_id,
--   community_owned_date,
--   tags,
--   title,
--   body,
--   last_editor_user_id,
--   last_edit_date,
--   last_activity_date
-- FROM posts WHERE post_type = 'question';

-- CREATE VIEW answers AS
-- SELECT
--   id,
--   score,
--   comments,
--   creation_date,
--   parent_id,
--   owner_user_id,
--   community_owned_date,
--   body,
--   last_editor_user_id,
--   last_edit_date,
--   last_activity_date
-- FROM posts WHERE post_type = 'answer';

