from environs import Env

env = Env()
env.read_env()


env.str("API_DOMAIN", default="http://localhost:8000")
