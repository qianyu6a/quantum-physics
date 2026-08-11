import yaml, os, subprocess, json, urllib.request

# Get GitHub token
config_paths = [
    r"D:\Hermes\Hermes Agent CN Desktop Portable\data\hermes-home\config.yaml",
    r"D:\Hermes\HermesPortable\data\hermes-home\config.yaml",
]
token = ''
for cp in config_paths:
    if os.path.exists(cp):
        with open(cp, 'r', encoding='utf-8') as f:
            cfg = yaml.safe_load(f)
        for k,v in cfg.get('mcp_servers',{}).items():
            if 'github' in k.lower():
                token = v.get('env',{}).get('GITHUB_PERSONAL_ACCESS_TOKEN','')
                break
        if token:
            break

if not token:
    print("NO TOKEN FOUND")
    exit(1)

print(f"Token found, length: {len(token)}")

PROJECT = r"D:\知识库\quantum-physics"
REPO_NAME = "quantum-physics"

# Step 1: Create GitHub repo
data = json.dumps({"name": REPO_NAME, "description": "量子物理交互科普 — 从紫外灾难到标准模型", "homepage": f"https://qianyu6a.github.io/{REPO_NAME}/", "auto_init": False}).encode()
req = urllib.request.Request("https://api.github.com/user/repos", data=data, method="POST")
req.add_header("Authorization", f"token {token}")
req.add_header("User-Agent", "hermes")
req.add_header("Accept", "application/vnd.github.v3+json")
try:
    resp = urllib.request.urlopen(req)
    print(f"Repo created: {resp.status}")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"Create: HTTP {e.code} - {body[:200]}")

# Step 2: Init git + push
os.chdir(PROJECT)

# Copy to root for Pages
import shutil
shutil.copy("static/index.html", "index.html")

with open(".gitignore", "w") as f:
    f.write("__pycache__/\n*.pyc\n")

subprocess.run(["git", "init"], capture_output=True)
subprocess.run(["git", "checkout", "-b", "main"], capture_output=True)
subprocess.run(["git", "add", "-A"], capture_output=True)
subprocess.run(["git", "commit", "-m", "⚛️ 量子物理交互科普 — 15概念 + Canvas动画"], capture_output=True)

url = f"https://qianyu6a:{token}@github.com/qianyu6a/{REPO_NAME}.git"
result = subprocess.run(["git", "push", url, "main"], capture_output=True, text=True, timeout=30)
print("PUSH:", result.stdout[-300:] if result.stdout else result.stderr[-300:])

# Step 3: Enable Pages
ghp_data = json.dumps({"source": {"branch": "main", "path": "/"}}).encode()
req2 = urllib.request.Request(f"https://api.github.com/repos/qianyu6a/{REPO_NAME}/pages", data=ghp_data, method="POST")
req2.add_header("Authorization", f"token {token}")
req2.add_header("User-Agent", "hermes")
req2.add_header("Accept", "application/vnd.github.v3+json")
try:
    resp2 = urllib.request.urlopen(req2)
    print(f"Pages: {resp2.status}")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"Pages: HTTP {e.code} - {body[:200]}")

print(f"\n✅ https://qianyu6a.github.io/{REPO_NAME}/")
