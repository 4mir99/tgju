import requests
from bs4 import BeautifulSoup
import time
import os
import sys

# متغیرهای قیمت قبلی
previous_prices = {"gold_18k": None, "coin": None, "dollar": None}

# رنگ‌ها برای ترمینال
RESET = "\033[0m"
GREEN = "\033[32m"
RED = "\033[31m"
BLUE = "\033[34m"

def update_prices():
    try:
        # دریافت محتوای صفحه
        url = "https://www.tgju.org/"
        response = requests.get(url)
        response.raise_for_status()

        # پارس کردن HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # استخراج قیمت‌ها
        gold_18k_price = parse_price(get_price_by_name(soup, 'طلای 18 عیار'))
        coin_price = parse_price(get_price_by_name(soup, 'سکه امامی'))
        dollar_price = parse_price(get_price_by_class(soup, 'market-price'))

        # پاک کردن کنسول
        os.system('cls' if os.name == 'nt' else 'clear')

        # نمایش قیمت‌ها با رنگ تغییرات
        print(f"time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"gold 18: {get_colored_text('gold_18k', gold_18k_price)} ")
        print(f"sekleh: {get_colored_text('coin', coin_price)} ")
        print(f"dollar: {get_colored_text('dollar', dollar_price)} ")

    except Exception as e:
        print(f"error to get data {e}")


def get_price_by_name(soup, item_name):
    """استخراج قیمت بر اساس نام کالای نمایش داده شده"""
    tag = soup.find('th', string=item_name)
    return tag.find_next_sibling('td').text.strip() if tag else "N/A"


def get_price_by_class(soup, class_name):
    """استخراج قیمت بر اساس کلاس HTML"""
    tag = soup.find('td', class_=class_name)
    return tag.text.strip() if tag else "N/A"


def parse_price(price_text):
    """تبدیل متن قیمت به عدد صحیح"""
    try:
        return int(price_text.replace(',', ''))
    except ValueError:
        return None


def get_colored_text(item_name, current_price):
    """بررسی تغییرات و بازگرداندن متن رنگی"""
    global previous_prices
    previous_price = previous_prices[item_name]
    previous_prices[item_name] = current_price

    if current_price is None:
        return "N/A"

    # تعیین رنگ بر اساس تغییرات
    if previous_price is None:
        return f"{current_price:,}"
    elif current_price > previous_price:
        return f"{GREEN}{current_price:,}{RESET}"  # سبز برای افزایش
    elif current_price < previous_price:
        return f"{RED}{current_price:,}{RESET}"  # قرمز برای کاهش
    else:
        return f"{BLUE}{current_price:,}{RESET}"  # آبی برای ثابت ماندن


# تنظیم کدک کنسول به utf-8 (برای ویندوز)
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# اجرای برنامه هر ۱۵ ثانیه یک‌بار
while True:
    update_prices()
    time.sleep(15)  # تاخیر ۱۵ ثانیه
