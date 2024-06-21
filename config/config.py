import os

# VARIABLE CONFIG
OWNER_ID = int(os.getenv("OWNER_ID", "1784606556"))

USERNAME_BOT = os.getenv(
    "USERNAME_BOT",
    "riaa_userbot",
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
    "mongodb+srv://riabot:riabot@cluster0.cxeyxiy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
)

MONGO_UBOT = os.getenv(
    "MONGO_UBOT",
    "mongodb+srv://riaubot:riaubot@cluster0.v8hgjig.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
)

MONGO_CLIENT = os.getenv(
    "MONGO_CLIENT",
    "mongodb+srv://riaclient:riaclient@cluster0.uilbkxf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
)


# MONGODB EXPIRED
MONGO_EXPIRED = os.getenv(
    "MONGO_EXPIRED",
    "mongodb+srv://riaexpired:riaexpired@cluster0.tq0r1xw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
)

# MONGODB REVOKE
MONGO_UTILS = os.getenv(
    "MONGO_UTILS",
    "mongodb+srv://riautils:riautils@cluster0.dntnr3q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
)

# MONGODB TOPCMD
MONGO_TOPCMD = os.getenv(
    "MONGO_TOPCMD",
    "mongodb+srv://riatopcmd:riatopcmd@cluster0.zzikqb2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
)
