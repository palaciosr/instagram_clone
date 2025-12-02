# app/domains/posts/service.py
from app.domains.posts.repository import PostRepository
from app.domains.posts.models import Post
from app.domains.posts.schemas import PostCreate
from app.shared.exceptions import NotFoundError

from app.domains.users.repository import UserRepository


class PostService:
    def __init__(self, repo: PostRepository, users: UserRepository):
        self.repo = repo
        self.users = users

    async def create_post(self, username: str, caption: str):
        user = await self.users.get_by_username(username)
        return await self.repo.create(user.id, caption)


    async def feed(self):
        posts = await self.repo.get_feed()
        results = []

        if posts:

            for post in posts:
                results.append({
                    "id": post.id,
                    "username": post.user.username,
                    "caption": post.caption,
                    "likes": len(post.likes),
                    "comments": [
                        {
                            "username": c.user.username,
                            "text": c.text
                        } for c in post.comments
                    ],
                    "created_at": post.created_at,
                })

        return results

    async def like(self, username: str, post_id: int):
        user = await self.users.get_by_username(username)
        return await self.repo.like_post(post_id, user.id)

    async def comment(self, username: str, post_id: int, text: str):
        user = await self.users.get_by_username(username)
        return await self.repo.comment_post(post_id, user.id, text)
