import requests
import os
import sys
import shutil
import platform

GITHUB_API_URL = "https://api.github.com/repos/Einzieg/AutoNovaGui/releases/latest"
LOCAL_VERSION_FILE = "version.txt"
UPDATE_DIR = "updates"
WINDOWS_EXECUTABLE_NAME = "AutoNovaGui.exe"
MACOS_ZIP_NAME = "AutoNovaGui.zip"


def get_latest_release_info():
    response = requests.get(GITHUB_API_URL)
    response.raise_for_status()
    return response.json()


def get_local_version():
    if os.path.exists(LOCAL_VERSION_FILE):
        with open(LOCAL_VERSION_FILE, "r") as f:
            return f.read().strip()
    return None


def download_file(url, local_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(local_path, 'wb') as f:
        shutil.copyfileobj(response.raw, f)


def extract_zip(file_path, extract_to):
    shutil.unpack_archive(file_path, extract_to)


def check_for_update():
    latest_release = get_latest_release_info()
    latest_version = latest_release['tag_name']
    local_version = get_local_version()

    if latest_version != local_version:
        asset_name = WINDOWS_EXECUTABLE_NAME if platform.system() == "Windows" else MACOS_ZIP_NAME
        asset = next(asset for asset in latest_release['assets'] if asset['name'] == asset_name)
        download_url = asset['browser_download_url']
        local_file_path = os.path.join(os.getcwd(), asset_name)

        print(f"Downloading latest version: {latest_version}")
        download_file(download_url, local_file_path)

        if platform.system() == "Windows":
            # 替换旧的exe文件
            os.replace(local_file_path, WINDOWS_EXECUTABLE_NAME)
        else:
            # 解压并替换旧的.app文件
            extract_zip(local_file_path, os.getcwd())
            app_dir = os.path.join(os.getcwd(), "AutoNovaGui.app")
            target_app_dir = "你的macos_app目标目录"
            if os.path.exists(target_app_dir):
                shutil.rmtree(target_app_dir)
            shutil.move(app_dir, target_app_dir)

        # 更新本地版本文件
        with open(LOCAL_VERSION_FILE, "w") as f:
            f.write(latest_version)

        print("更新完成。请重新启动应用程序。")
        sys.exit()
    else:
        print("当前已是最新版本。")


if __name__ == "__main__":
    check_for_update()

