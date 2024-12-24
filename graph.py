from neo4j import AsyncGraphDatabase

from model import Comment, Post, User


class WeiboGraph:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = AsyncGraphDatabase.driver(uri, auth=(user, password))

    async def close(self):
        await self.driver.close()

    async def create_user(self, user: User):
        query = (
            "MERGE (u:User {id: $id}) "
            "SET u.location = COALESCE($location, u.location), u.screen_name = COALESCE($screen_name, u.screen_name), "
            "u.followers_count = COALESCE($followers_count, u.followers_count), u.friends_count = COALESCE($friends_count, u.friends_count), "
            "u.description = COALESCE($description, u.description), u.gender = COALESCE($gender, u.gender)"
        )
        parameters = {
            "id": user.id,
            "location": user.location,
            "screen_name": user.screen_name,
            "followers_count": user.followers_count,
            "friends_count": user.friends_count,
            "description": user.description,
            "gender": user.gender,
        }
        async with self.driver.session() as session:
            await session.run(query, parameters)

    async def create_post(self, post: Post, user_id):
        query = (
            "MERGE (p:Post {id: $id}) "
            "SET p.text_raw = COALESCE($text_raw, p.text_raw), p.created_at = COALESCE($created_at, p.created_at) "
            "WITH p "
            "MATCH (u:User {id: $user_id}) "
            "MERGE (u)-[:POSTED]->(p)"
        )
        parameters = {
            "id": post.id,
            "text_raw": post.text_raw,
            "created_at": post.created_at,
            "user_id": user_id,
        }
        async with self.driver.session() as session:
            await session.run(query, parameters)

    async def create_comment(self, comment: Comment, user_id, post_id):
        query = (
            "MERGE (c:Comment {id: $id}) "
            "SET c.text_raw = COALESCE($text_raw, c.text_raw), c.source = COALESCE($source, c.source), c.created_at = COALESCE($created_at, c.created_at) "
            "WITH c "
            "MATCH (u:User {id: $user_id}), (p:Post {id: $post_id}) "
            "MERGE (u)-[:COMMENTED]->(c) "
            "MERGE (c)-[:COMMENTS]->(p)"
        )
        parameters = {
            "id": comment.id,
            "text_raw": comment.text_raw,
            "source": comment.source,
            "created_at": comment.created_at,
            "user_id": user_id,
            "post_id": post_id,
        }
        async with self.driver.session() as session:
            await session.run(query, parameters)

    async def create_like_relationship(self, user_id, post_id):
        query = (
            "MATCH (u:User {id: $user_id}), (p:Post {id: $post_id}) "
            "MERGE (u)-[:LIKED]->(p)"
        )
        parameters = {"user_id": user_id, "post_id": post_id}
        async with self.driver.session() as session:
            await session.run(query, parameters)

    async def create_repost_relationship(self, user_id, post_id, original_post_id):
        query = (
            "MATCH (u:User {id: $user_id}), (p:Post {id: $post_id}), (op:Post {id: $original_post_id}) "
            "MERGE (u)-[:REPOSTED]->(p) "
            "MERGE (p)-[:REPOST_OF]->(op)"
        )
        parameters = {
            "user_id": user_id,
            "post_id": post_id,
            "original_post_id": original_post_id,
        }
        async with self.driver.session() as session:
            await session.run(query, parameters)
