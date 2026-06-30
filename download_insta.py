import os
import sys
import getpass
import subprocess

def install_dependency(package_name, import_name=None):
    if import_name is None:
        import_name = package_name
    try:
        import importlib
        importlib.import_module(import_name)
    except ImportError:
        print(f"Installing missing dependency: {package_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", package_name, "--break-system-packages"])
        except Exception as e:
            print(f"Failed to install {package_name} automatically: {e}")
            print(f"Please run: pip3 install {package_name} --break-system-packages")
            sys.exit(1)

# Ensure instaloader is present
install_dependency("instaloader")
import instaloader

def import_session_from_browser(browser_name, loader):
    # Dynamically ensure browser_cookie3 is installed
    install_dependency("browser-cookie3", "browser_cookie3")
    import browser_cookie3

    supported_browsers = {
        "brave": browser_cookie3.brave,
        "chrome": browser_cookie3.chrome,
        "chromium": browser_cookie3.chromium,
        "edge": browser_cookie3.edge,
        "firefox": browser_cookie3.firefox,
        "librewolf": browser_cookie3.librewolf,
        "opera": browser_cookie3.opera,
        "opera_gx": browser_cookie3.opera_gx,
        "safari": browser_cookie3.safari,
        "vivaldi": browser_cookie3.vivaldi,
    }

    browser_name = browser_name.lower().strip()
    if browser_name not in supported_browsers:
        print(f"Error: Browser '{browser_name}' is not supported.")
        print(f"Supported browsers: {', '.join(supported_browsers.keys())}")
        sys.exit(1)

    try:
        print(f"\nExtracting Instagram cookies from {browser_name}...")
        browser_cookies = list(supported_browsers[browser_name]())
        
        cookies = {}
        for cookie in browser_cookies:
            if 'instagram' in cookie.domain:
                cookies[cookie.name] = cookie.value
                
        if cookies:
            # Update instaloader session cookies
            loader.context.update_cookies(cookies)
            print(f"Session cookies successfully loaded from {browser_name}!")
        else:
            raise Exception(f"No active Instagram login cookies found in {browser_name}.")
    except Exception as e:
        print(f"\nFailed to load cookies: {e}")
        print("\nTroubleshooting steps:")
        print("1. Make sure you are actively logged into Instagram in that browser.")
        print("2. CLOSE the browser completely before running the script so it can unlock the cookie database file.")
        print("3. If you are on macOS with Chrome or Safari, OS permissions (like Keychain or Full Disk Access) may block it. Try using Firefox.")
        sys.exit(1)

def main():
    target_profile = "arushgore_"
    download_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), target_profile)
    
    # Configure Instaloader to download only images and skip metadata files
    loader = instaloader.Instaloader(
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False,
        post_metadata_txt_pattern="",
        dirname_pattern=download_dir
    )
    
    print("=================================================================")
    print("   Instagram Photo Downloader for @arushgore_")
    print("=================================================================")
    print("Choose login method:")
    print("1. Interactive Login (Password + 2FA / Verification code support)")
    print("2. Import Session from Browser (Firefox, Chrome, Safari, etc.)")
    print("=================================================================\n")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        username = input("Enter your Instagram username: ").strip()
        if not username:
            print("Username required.")
            sys.exit(1)
        try:
            print(f"\nLogging in as {username}...")
            # interactive_login handles password prompt and 2FA codes in the local terminal!
            loader.interactive_login(username)
            print("Login successful!")
        except Exception as e:
            print(f"Login failed: {e}")
            sys.exit(1)
            
    elif choice == "2":
        print("\nAvailable browsers: chrome, firefox, safari, edge, opera")
        browser = input("Enter browser name (e.g. firefox, chrome): ").strip().lower()
        if not browser:
            print("Browser name required.")
            sys.exit(1)
        import_session_from_browser(browser, loader)
    else:
        print("Invalid choice.")
        sys.exit(1)
        
    try:
        print(f"\nRetrieving profile @{target_profile}...")
        profile = instaloader.Profile.from_username(loader.context, target_profile)
        print(f"Starting download of photos to: {download_dir}...\n")
        
        count = 0
        for post in profile.get_posts():
            if not post.is_video:
                loader.download_post(post, target=target_profile)
                count += 1
            
        print(f"\nSuccess! Downloaded {count} photos to: {download_dir}")
    except Exception as e:
        print(f"\nAn error occurred while downloading: {e}")

if __name__ == "__main__":
    main()
