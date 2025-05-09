from environs import Env

env = Env()
env.read_env()


ALLOWED_ORIGINS = env.list("ALLOWED_ORIGINS", default=["http://localhost:8001"])
