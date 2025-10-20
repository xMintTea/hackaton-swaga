from enum import Enum


class Roles(Enum):
    USER = "user"
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"


class Social(Enum):
    YOUTUBE = "youtube"
    VK = "vk"
    TELEGRAM = "telegram"
    GITHUB = "github"
    OTHER = "other"