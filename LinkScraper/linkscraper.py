import time
import random
import sys
import os
import pandas as pd
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

try:
    import pyautogui
except ImportError:
    os.system("pip install pyautogui")
    import pyautogui

def clear_windows_popup():
    """উইন্ডোজের Save As বা প্রিন্ট পপআপ আসলে ESC প্রেস করে ক্যানসেল করবে"""
    try:
        pyautogui.press('esc')
    except:
        pass

def human_mouse_move_and_click(driver, element):
    """হিউম্যানের মতো মাউস মুভ করে ক্যাপচা চেক বক্সে ক্লিক করবে"""
    try:
        actions = ActionChains(driver)
        actions.move_to_element_with_offset(element, random.randint(2, 5), random.randint(2, 5))
        actions.pause(random.uniform(0.3, 0.6))
        actions.click()
        actions.perform()
    except Exception:
        element.click()

def check_and_solve_captcha(driver):
    """ক্যাপচা চেক বক্স ডিটেক্ট করে মাউস দিয়ে হ্যান্ডেল করা"""
    try:
        frames = driver.find_elements(By.TAG_NAME, "iframe")
        captcha_found = False
        
        for frame in frames:
            src = frame.get_attribute("src")
            if src and "recaptcha" in src:
                captcha_found = True
                break
                
        if captcha_found or len(driver.find_elements(By.XPATH, "//*[contains(@id, 'recaptcha')]")) > 0:
            print("\n⚠️ CAPTCHA detected! Moving mouse like a human to check the box...")
            
            iframe_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='recaptcha']"))
            )
            driver.switch_to.frame(iframe_element)
            
            checkbox = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))
            )
            
            human_mouse_move_and_click(driver, checkbox)
            
            driver.switch_to.default_content()
            print("Successfully clicked the CAPTCHA checkbox!")
            time.sleep(30)
            return True
    except:
        driver.switch_to.default_content()
    return False

def is_parameter_matched(url, required_path, required_param):
    """ডাইনামিক্যালি চেক করবে URL-এ নির্দিষ্ট পাথ এবং প্যারামিটার আছে কি না।"""
    try:
        parsed_url = urlparse(url)
        if required_path and required_path not in parsed_url.path:
            return False
        query_params = parse_qs(parsed_url.query)
        if required_param and required_param in query_params:
            return True
        return False
    except Exception:
        return False

def append_to_csv(filename, url):
    """সিঙ্গেল লিংক লাইভ ফাইলে অ্যাপেন্ড (Append) করার ফাংশন"""
    file_exists = os.path.isfile(filename)
    df = pd.DataFrame([{"Raw_URLs": url}])
    df.to_csv(filename, mode='a', index=False, header=not file_exists, encoding='utf-8')

def get_flexible_search_elements(driver):
    """গুগলের স্ট্রাকচার ধরে নিখুঁতভাবে অর্গানিক লিংক এলিমেন্টগুলো তোলার ফাংশন"""
    elements = []
    try:
        search_blocks = driver.find_elements(By.CSS_SELECTOR, 'div.yuRUbf a, div.g a')
        for a in search_blocks:
            try:
                href = a.get_attribute('href')
                if href and href.startswith('http'):
                    if not any(domain in href for domain in ['google.', 'youtube.', 'gstatic.', 'googleapis.com']):
                        if len(a.find_elements(By.TAG_NAME, 'h3')) > 0:
                            if a not in elements:
                                elements.append(a)
            except:
                continue
                
        if not elements:
            h3_tags = driver.find_elements(By.CSS_SELECTOR, 'h3.LC20lb')
            for h3 in h3_tags:
                try:
                    parent_a = h3.find_element(By.XPATH, './ancestor::a')
                    if parent_a not in elements:
                        elements.append(parent_a)
                except:
                    continue
    except Exception as e:
        print(f"Error finding elements: {e}")
        
    return elements

def scrape_search_results(target_path, target_param, max_pages=3):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    options.add_argument("--lang=en-US")
    prefs = {
        "intl.accept_languages": "en,en_US",
        "download.prompt_for_download": True,
        "download.default_directory": "/dev/null",
        "profile.default_content_settings.popups": 0,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    
    print("Launching Chrome browser...")
    driver = webdriver.Chrome(options=options)
    
    raw_csv_filename = "raw_scraped_links.csv"
    if os.path.isfile(raw_csv_filename):
        os.remove(raw_csv_filename)
    
    pd.DataFrame(columns=["Raw_URLs"]).to_csv(raw_csv_filename, index=False, encoding='utf-8')
    print(f"📁 Initialized raw file: {raw_csv_filename}")

    seen_links = set()

    try:
        print("Navigating to Google...")
        driver.get("https://www.google.com/?hl=en")
        
        print("\n" + "="*65)
        
        print("👉 Browser is open. Please type/paste your search query ")
        print("   directly in the browser's search box and press ENTER.")
        print("="*65 + "\n")

        while True:
            try:
                current_url = driver.current_url
                if "/search?" in current_url or "q=" in current_url:
                    print("✅ Search action detected! Starting smart waiting processing...")
                    time.sleep(2)
                    break
            except:
                pass
            time.sleep(1)
        
        current_page = 1
        main_window_handle = driver.current_window_handle
        
        while current_page <= max_pages:
            print(f"\n--- Scraping Page {current_page} (Smart Wait Sequential Order) ---")
            time.sleep(1.5)
            
            check_and_solve_captcha(driver)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.5)
            
            link_elements = get_flexible_search_elements(driver)
            total_results = len(link_elements)
            print(f"Found {total_results} valid results on page {current_page}")

            index = 0
            while index < total_results:
                try:
                    driver.switch_to.window(main_window_handle)
                    
                    link_elements_refresh = get_flexible_search_elements(driver)
                    if index >= len(link_elements_refresh):
                        break
                        
                    elem = link_elements_refresh[index]
                    print(f"Processing Item {index + 1} of {total_results}...")

                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
                    time.sleep(0.3)
                    
                    modifier_key = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL
                    actions = ActionChains(driver)
                    actions.key_down(modifier_key).click(elem).key_up(modifier_key).perform()
                    
                    time.sleep(1.0)
                    
                    all_windows = driver.window_handles
                    if len(all_windows) > 1:
                        new_window = [w for w in all_windows if w != main_window_handle][0]
                        driver.switch_to.window(new_window)
                        
                        clear_windows_popup()

                        # [SOLVED]: about:blank বাইপাস করার জন্য টাইমিং ও লুপ মডিফিকেশন
                        start_wait = time.time()
                        actual_url = driver.current_url
                        while ("google.com" in actual_url or "google/url" in actual_url or "about:blank" in actual_url) and (time.time() - start_wait < 6):
                            time.sleep(0.2)
                            clear_windows_popup() 
                            try:
                                actual_url = driver.current_url
                            except:
                                break
                        
                        if "google.com" in actual_url or "about:blank" in actual_url:
                            try:
                                actual_url = driver.execute_script("return window.location.href;")
                            except:
                                pass

                        # স্টাকড উইন্ডো ফিল্টারিং কন্ডিশন
                        if actual_url and "about:blank" in actual_url:
                            print("   ❌ [Bypassed] Window stuck on about:blank. Skipping link...")
                            driver.close()
                            driver.switch_to.window(main_window_handle)
                            index += 1
                            continue

                        if actual_url and actual_url.startswith('http') and 'google.' not in actual_url and 'download' not in actual_url.lower():
                            if actual_url not in seen_links:
                                seen_links.add(actual_url)
                                append_to_csv(raw_csv_filename, actual_url)
                                print(f"   ↳ [Smart Success] Appended: {actual_url}")
                        driver.close()
                        driver.switch_to.window(main_window_handle)
                        time.sleep(0.5)
                        index += 1
                    
                except Exception as ex:
                    print(f"Error at sequential index {index}: {ex}")
                    try:
                        if len(driver.window_handles) > 1:
                            driver.close()
                        driver.switch_to.window(main_window_handle)
                    except:
                        pass
                    index += 1
                    continue

                    
                except Exception as ex:
                    print(f"Error at sequential index {index}: {ex}")
                    try:
                        if len(driver.window_handles) > 1:
                            driver.close()
                        driver.switch_to.window(main_window_handle)
                    except:
                        pass
                    index += 1
                    continue

            
            try:
                driver.switch_to.window(main_window_handle)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                
                next_button = driver.find_element(By.ID, 'pnnext')
                if next_button and current_page < max_pages:
                    print(f"\nMoving sequentially to next page ({current_page + 1})...")
                    next_button.click()
                    current_page += 1
                    time.sleep(3)
                else:
                    print("Reached the maximum specified pages or no next button found.")
                    break
            except Exception:
                print("No more pages found.")
                break

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        time.sleep(2)
        try:
            driver.quit()
        except:
            pass

    print(f"\nTotal unique external links scraped: {len(seen_links)}")

    if not seen_links:
        print("No links found at all. Exiting process.")
        return

    print("\nApplying parameter filter on collected raw data...")
    
    filtered_links = [
        link for link in seen_links 
        if is_parameter_matched(link, target_path, target_param)
    ]
    print(f"Links matched path '{target_path}' and parameter '{target_param}=' criteria: {len(filtered_links)}")

    if filtered_links:
        safe_name = f"{target_path.replace('.', '_')}_{target_param}"
        filtered_csv_filename = f"filtered_links_{safe_name}.csv"
        
        df_filtered = pd.DataFrame(filtered_links, columns=["Filtered_URLs"])
        df_filtered.to_csv(filtered_csv_filename, index=False, encoding='utf-8')
        print(f"🎯 Filter check OK! Separate filtered file created: {filtered_csv_filename}")
    else:
        print("⚠️ No links matched your precise parameter criteria.")
        print(f"📁 As requested, the raw file '{raw_csv_filename}' is kept as it is, and no separate filtered file was created.")

if __name__ == "__main__":
    print("="*60)
    print(" CLEAN & FAST SMART URL-WAITING SCRAPER ")
    print("="*60)

    path=input("Enter Filter Path: ")
    param=input("Enter Filter Parameter: ")
    TARGET_PATH = path     
    TARGET_PARAM = param       
    MAX_PAGES_TO_SCRAPE = 50       
    
    scrape_search_results(TARGET_PATH, TARGET_PARAM, MAX_PAGES_TO_SCRAPE)