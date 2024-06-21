import os

# VARIABLE CONFIG
OWNER_ID = int(os.getenv("OWNER_ID", "1784606556"))

USERNAME_BOT = os.getenv(
    "USERNAME_BOT",
    "smallubot",
)

LOGS_DATABASE_UBOT = int(os.getenv("LOGS_DATABASE_UBOT", "-1001805411267"))

SELLER_GROUP = [-1001990595313]

BLACKLIST_CHAT = list(
    map(
        int,
        os.getenv(
            "BLACKLIST_CHAT",
            "-1001874736197 -1001473548283 -1001687155877 -1001830597771",
        ).split(),
    )
)

ADMINS = [int(x) for x in (os.environ.get("ADMINS", "966484443 1784606556").split())]

MONGO_BOT = os.getenv(
    "MONGO_BOT",
    "mongodb+srv://smalbot:smalbot@cluster0.gee3fd7.mongodb.net/?retryWrites=true&w=majority",
)

MONGO_UBOT = os.getenv(
    "MONGO_UBOT",
    "mongodb+srv://ubot:ubot@cluster0.fueonvl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
)

MONGO_CLIENT = os.getenv(
    "MONGO_CLIENT",
    "mongodb+srv://client:client@cluster0.8rgnrxx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
)


# MONGODB EXPIRED
MONGO_EXPIRED = os.getenv(
    "MONGO_EXPIRED",
    "mongodb+srv://expired:expired@cluster0.rnwj7ho.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
)

# MONGODB REVOKE
MONGO_UTILS = os.getenv(
    "MONGO_UTILS",
    "mongodb+srv://tobrut:tobrut@cluster0.wswopzc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
)

# MONGODB TOPCMD
MONGO_TOPCMD = os.getenv(
    "MONGO_TOPCMD",
    "mongodb+srv://tobrut:tobrut@cluster0.sagdcy8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
)
