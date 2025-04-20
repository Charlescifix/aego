# check_pub.py

from solders.pubkey import Pubkey

address = "6GwF3K8v9VtGzZHzNyM3rrgE5fg3MfFJNv2rVxC9FZDc"
pubkey = Pubkey.from_string(address)
print(f"✅ Converted to Pubkey: {pubkey}")
