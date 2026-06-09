import requests
import base64
import os
import hashlib

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

    def get_current_file_sha_and_content(self, path="all_v2ray_configs.txt"):
        """دریافت محتوای فعلی فایل برای مقایسه"""
        url = f"{self.base_url}/contents/{path}"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200:
            data = resp.json()
            content = base64.b64decode(data["content"]).decode('utf-8')
            return data["sha"], content
        return None, None

    def get_all_configs(self):
        urls = [
            "https://raw.githubusercontent.com/V2RAYCONFIGSPOOL/V2RAY_SUB/refs/heads/main/v2ray_configs_no1.txt",
            # ... (بقیه لینک‌ها)
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

    def upload_combined_file(self):
        new_content = self.get_all_configs()
        if not new_content.strip():
            print("⚠️ هیچ محتوایی دریافت نشد!")
            return False

        # دریافت محتوای قبلی
        old_sha, old_content = self.get_current_file_sha_and_content()

        # مقایسه محتوا (اگر تغییری نکرده، آپلود نکن)
        if old_content and hashlib.md5(old_content.encode()).hexdigest() == hashlib.md5(new_content.encode()).hexdigest():
            print("🔄 هیچ تغییری در کانفیگ‌ها ایجاد نشده. آپلود انجام نشد.")
            return True

        print("🔄 تغییر تشخیص داده شد → در حال آپلود...")

        encoded = base64.b64encode(new_content.encode('utf-8')).decode('utf-8')

        data = {
            "message": "Update v2ray configs - Auto (changed detected)",
            "branch": self.branch,
            "content": encoded
        }

        if old_sha:
            data["sha"] = old_sha

        url = f"{self.base_url}/contents/all_v2ray_configs.txt"
        response = requests.put(url, json=data, headers=self.headers)

        if response.status_code in [200, 201]:
            print("🎉 آپدیت موفق! محتوا تغییر کرده بود.")
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
    updater.upload_combined_file()
