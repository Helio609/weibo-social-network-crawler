from pydantic import BaseModel, Field
from typing import Literal

class User(BaseModel):
    id: int = Field(description='微博用户ID')
    location: str = Field(description="所在地")
    screen_name: str = Field(description="微博用户名称")
    followers_count: int = Field(description="粉丝数量")
    friends_count: int = Field(description="关注数量")
    description: str = Field(description="个人描述")
    gender: Literal["m", "f"] = Field(description="性别")

class Post(BaseModel):
    id: int = Field(description="帖子ID")
    text_raw: str = Field(description="帖子内容")
    created_at: str = Field(description="发布时间")

class Comment(BaseModel):
    id: int = Field(description="评论ID")
    text_raw: str = Field(description="评论内容")
    source: str = Field(description="发帖人位置")
    created_at: str = Field(description="发布时间")
