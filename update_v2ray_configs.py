import requests
import base64
import os

class Updater:
    def __init__(self, token, owner, repo, branch="main"):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.branch = branch
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.base_url = f"https://api.github.com/repos/{owner}/{repo}"

    def delete_old_file(self):
        """فایل قدیمی را کامل حذف می‌کند"""
        url = f"{self.base_url}/contents/all_v2ray_configs.txt"
        resp = requests.get(url, headers=self.headers)
        
        if resp.status_code == 200:
            sha = resp.json()["sha"]
            delete_data = {
                "message": "Delete old configs file",
                "sha": sha,
                "branch": self.branch
            }
            requests.delete(url, json=delete_data, headers=self.headers)
            print("🗑️ فایل قدیمی حذف شد")

    def get_all_configs(self):
        urls = [
            "https://raw.githubusercontent.com/V2RAYCONFIGSPOOL/V2RAY_SUB/refs/heads/main/v2ray_configs_no1.txt",
            "https://raw.githubusercontent.com/V2RAYCONFIGSPOOL/V2RAY_SUB/refs/heads/main/v2ray_configs_no2.txt",
            "https://raw.githubusercontent.com/V2RAYCONFIGSPOOL/V2RAY_SUB/refs/heads/main/v2ray_configs_no3.txt",
            "https://raw.githubusercontent.com/V2RAYCONFIGSPOOL/V2RAY_SUB/refs/heads/main/v2ray_configs_no4.txt",
            "https://raw.githubusercontent.com/V2RAYCONFIGSPOOL/V2RAY_SUB/refs/heads/main/v2ray_configs_no5.txt",
            "https://raw.githubusercontent.com/V2RAYCONFIGSPOOL/V2RAY_SUB/refs/heads/main/v2ray_configs_no6.txt",
            "https://raw.githubusercontent.com/V2RAYCONFIGSPOOL/V2RAY_SUB/refs/heads/main/v2ray_configs_no7.txt",
            "https://raw.githubusercontent.com/V2RAYCONFIGSPOOL/V2RAY_SUB/refs/heads/main/v2ray_configs_no8.txt",
            "https://raw.githubusercontent.com/V2RAYCONFIGSPOOL/V2RAY_SUB/refs/heads/main/v2ray_configs_no9.txt",
            "https://raw.githubusercontent.com/V2RAYCONFIGSPOOL/V2RAY_SUB/refs/heads/main/v2ray_configs_no10.txt"
        ]
        
        all_content = []
        for i, url in enumerate(urls, 1):
            try:
                r = requests.get(url, timeout=20)
                r.raise_for_status()
                content = r.text.strip()
                if content:
                    all_content.append(f"===== CONFIG NO {i} =====\n{content}\n\n")
                    print(f"✅ کانفیگ {i} دریافت شد")
            except Exception as e:
                print(f"❌ خطا در کانفیگ {i}: {e}")
        
        return "".join(all_content)

    def upload_new_file(self, content):
        """آپلود فایل جدید"""
        if not content.strip():
            print("⚠️ محتوا خالی است!")
            return False

        encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
        
        data = {
            "message": "Update v2ray configs - Fresh file",
            "branch": self.branch,
            "content": encoded
        }

        url = f"{self.base_url}/contents/all_v2ray_configs.txt"
        response = requests.put(url, json=data, headers=self.headers)

        if response.status_code in [200, 201]:
            print("🎉 فایل جدید با موفقیت ایجاد/آپدیت شد")
            return True
        else:
            print(f"❌ خطا: {response.status_code}")
            print(response.text[:300])
            return False


# ===================== تنظیمات =====================
if __name__ == "__main__":
    TOKEN = os.getenv("GITHUB_TOKEN")
    OWNER = "Sa1lark"
    REPO = "Sailark-mire"
    BRANCH = "main"

    if not TOKEN:
        print("❌ توکن پیدا نشد!")
        exit(1)

    updater = Updater(TOKEN, OWNER, REPO, BRANCH)
    
    print("🗑️ در حال حذف فایل قدیمی...")
    updater.delete_old_file()
    
    print("📥 در حال دریافت کانفیگ‌های جدید...")
    new_content = updater.get_all_configs()
    
    print("📤 در حال آپلود فایل تازه...")
    updater.upload_new_file(new_content)
