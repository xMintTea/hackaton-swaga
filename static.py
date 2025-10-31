from enum import Enum


class Roles(Enum):
    USER = "user"
    TEACHER = "teacher"
    ADMIN = "admin"


class Social(Enum):
    YOUTUBE = "youtube"
    VK = "vk"
    TELEGRAM = "telegram"
    GITHUB = "github"
    OTHER = "other"