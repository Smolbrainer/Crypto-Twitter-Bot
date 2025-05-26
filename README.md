# Crypto-Contract-Hunter 🕵️‍♂️🚀  
Real-time Twitter bot that surfaces *brand-new* Ethereum and Solana contract addresses so you can spot tokens the moment they launch.

<div align="center">
  
| ETH (mainnet) | SOL (mainnet) |
|---------------|--------------|
| `0x…` regex →   Etherscan API check (verified ABI) | Base-58 regex →   Solscan API check (tokenInfo ∥ executable) |

</div>

---

## ✨ Features
* **Dual-chain support** – picks up both `0x…` (ERC-20 / ERC-721) and Solana SPL addresses  
* **Explorer validation** – calls Etherscan / Solscan to ignore EOAs and spam mints  
* **Plug-and-play output** – currently `print()`s hits, but you can swap in tweeting, DMs, Google Sheets, a DB, etc.

---

## 🚀 Quick start

```bash
# 1. Clone
git clone https://github.com/Smolbrainer/Crypto-Twitter-Bot/

# 2. Install Python deps
pip install -r requirements.txt

# 3. Add your secrets (see below)
make your .env file

# 4. Run
python bot.py
