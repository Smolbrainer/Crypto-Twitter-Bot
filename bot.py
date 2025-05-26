# bot.py  —  ETH + SOL contract hunter
import os, re, tweepy, time, logging, requests
from dotenv import load_dotenv; load_dotenv()

ETH_RE = re.compile(r"\b0x[a-fA-F0-9]{40}\b")
SOL_RE = re.compile(r"\b[1-9A-HJ-NP-Za-km-z]{43,44}\b")   
TOKEN_QUERY = "(0x OR mint) presale lang:en -is:retweet"

client = tweepy.Client(
    bearer_token=os.environ["TWITTER_BEARER"],
    wait_on_rate_limit=True,
)

# ---------- Explorer helpers ----------
ETHERSCAN_KEY = os.environ["ETHERSCAN_KEY"]
ETH_URL = (
    "https://api.etherscan.io/api"
    "?module=contract&action=getsourcecode&address={addr}&apikey=" + ETHERSCAN_KEY
)

SOL_URL = "https://public-api.solscan.io/account/{addr}"  


def is_fresh_eth(addr: str) -> bool:
    try:
        r = requests.get(ETH_URL.format(addr=addr), timeout=5).json()
        abi = r["result"][0]["ABI"]
        return abi not in ("", "Contract source code not verified")
    except Exception:
        return False


def is_fresh_sol(addr: str) -> bool:
    try:
        r = requests.get(SOL_URL.format(addr=addr), timeout=5).json()
        return bool(r.get("tokenInfo") or r.get("executable"))
    except Exception:
        return False


seen: set[str] = set()

while True:
    try:
        for page in tweepy.Paginator(
            client.search_recent_tweets,
            TOKEN_QUERY,
            max_results=100,
        ):
            for tw in page.data or []:
                eth_addrs = ETH_RE.findall(tw.text)
                sol_addrs = SOL_RE.findall(tw.text)

                for a in eth_addrs:
                    key = f"{tw.id}:eth:{a.lower()}"
                    if key in seen or not is_fresh_eth(a):
                        continue
                    seen.add(key)
                    print(f"🟢 NEW ETH {a}  ↗  https://twitter.com/i/web/status/{tw.id}")

                for a in sol_addrs:
                    key = f"{tw.id}:sol:{a}"
                    if key in seen or not is_fresh_sol(a):
                        continue
                    seen.add(key)
                    print(f"🟠 NEW SOL {a}  ↗  https://twitter.com/i/web/status/{tw.id}")

        time.sleep(60)      
    except Exception:
        logging.exception("bot-error")
        time.sleep(30)