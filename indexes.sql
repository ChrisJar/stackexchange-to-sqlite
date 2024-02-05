CREATE INDEX idx_badges_user_id ON Badges(UserId);

CREATE INDEX idx_posts_owner_user_id ON Posts(OwnerUserId);
CREATE INDEX idx_posts_last_editor_user_id ON Posts(LastEditorUserId);
CREATE INDEX idx_posts_accepted_answer_id ON Posts(AcceptedAnswerId) WHERE AcceptedAnswerId IS NOT NULL;
CREATE INDEX idx_posts_parent_id ON Posts(ParentId) WHERE ParentId IS NOT NULL;

CREATE INDEX idx_votes_user_id ON Votes(UserId);
CREATE INDEX idx_votes_post_id ON Votes(PostId);

CREATE INDEX idx_comments_user_id ON Comments(UserId);
CREATE INDEX idx_comments_post_id ON Comments(PostId);
