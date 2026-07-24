import requests
import time
from datetime import datetime
import os
import getpass
import json
import subprocess
import pandas as pd
import threading  # 新增：用于推送线程
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ================== Git 推送配置 ==================
GITHUB_REPO = "Juineii/kangmin_br0517"        # 请替换为您的仓库名
GITHUB_BRANCH = "main"                   # 分支名（main 或 master）
PUSH_INTERVAL = 60                       # 推送检查间隔（秒）
# GitHub Personal Access Token 优先从环境变量 GITHUB_TOKEN 读取

# ========== 原有配置信息 ==========
api_url = "https://en.beatroad.co.kr/exec/front/order/Formproductmileage/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ko;q=0.5     ",
    "Cache-Control": "no-cache",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://en.beatroad.co.kr",
    "Pragma": "no-cache",
    "Referer": "https://en.beatroad.co.kr/order/orderform.html?basket_type=A0000&delvtype=B",
    "X-Requested-With": "XMLHttpRequest"
}

# ========== Cookies ==========
cookies = {
    "siteLT": "2c2070bd-2adf-57e8-7ac3-c88321d56aa4",
    "analytics_longterm": "analytics_longterm.beatroad_1.A9D8587.1761646491020",
    "CVID_Y": "CVID_Y.535755404a5a515d6c01.1761398385605",
    "CUK45": "cuk45_beatroad_i9su07l70fsn7odnmnek7l2ju0g400e4",
    "CUK2Y": "cuk2y_beatroad_i9su07l70fsn7odnmnek7l2ju0g400e4",
    "CFAE_CUK1Y": "CFAE_CUK1Y.beatroad_1.2AOFQYF.1761398385605",
    "_fwb": "221VxiFuyH1dDfFFf4urJMG.1761228602224",
    "wcs_bt": "unknown:1778402930",
    "fb_event_id": "event_id.beatroad.2.D4Y3260S186WWJR7GLL7ZH93YZW7V9TD8",
    "fb_external_id": "1205e5b26fe16f08d555a1916a3707c7da283256836f4a84d8cf06e3dc28aff0",
    "siteSID": "d89799d3-cb26-be8b-639c-c311b1275883",
    "analytics_session_id": "analytics_session_id.beatroad_2.37A5068.1784729331239",
    "CVID": "CVID.535755404a5a515d6c02.1784729411205",
    "CID": "CIDRb8f70a28b152d6d21802d89c039eae3e",
    "CIDRb8f70a28b152d6d21802d89c039eae3e": "58388221199fee25d1d7257c82b66ff3%3A%3A%3A%3A%3A%3A%3A%3A%3A%3A%3A%3A%3A%3A%3A%3A%3A%3A%3A%3A%2F%3A%3A1784729323%3A%3A%3A%3Appdp%3A%3A1784729323%3A%3A%3A%3A%3A%3A%3A%3A",
    "ECSESSID": "lou3vhmfp10ddh2aqrgqc40n89q52lni",
    "basketcount_1": "0",
    "basketprice_1": "%26%238361%3B0",
    "wish_id": "df92a92359a56391801a5163bb12611a",
    "wishcount_1": "0",
    "isviewtype": "pc",
    "ec_ipad_device": "F",
    "CFAE_CID": "CFAE_CID.beatroad_2.CQ66R8Z.1784729332345",
    "recent_plist2": "9880%7C9909%7C9960%7C9955%7C10038%7C10075%7C10124%7C10132%7C10152%7C10181%7C10180%7C10212%7C10294%7C10388%7C10418%7C10461%7C10494%7C10532%7C10514%7C10511%7C10579%7C10594%7C10607%7C10769%7C10756%7C10807%7C10812%7C10842%7C10843%7C10884%7C10883%7C10930%7C10956%7C10972%7C10996%7C11068%7C11153%7C11165%7C11249%7C11284%7C11283%7C11323%7C11371%7C11390%7C11475",
    "org_phpsess_id_2": "lou3vhmfp10ddh2aqrgqc40n89q52lni",
    "return_url": "%2Forder%2Forderform.html%3Fbasket_type%3DA0000%26delvtype%3DB",
    "login_provider_2": "%7B%22member_id%22%3A%22qq35142634547855%22%2C%22provider%22%3Anull%2C%22client_id%22%3Anull%7D",
    "iscache": "F",
    "ec_mem_level": "2",
    "PHPSESSVERIFY": "20e96222e0ffcc88c21857b8dd855c45",
    "couponcount_2": "0",
    "atl_epcheck": "1",
    "atl_option": "1%2C1%2CH",
    "basketprice_2": "%26%2336%3B14.40",
    "ec_async_cache_avail_mileage_2": "0.00",
    "ec_async_cache_used_mileage_2": "0.00",
    "ec_async_cache_returned_mileage_2": "0",
    "ec_async_cache_unavail_mileage_2": "0",
    "ec_async_cache_used_deposit_2": "0",
    "ec_async_cache_all_deposit_2": "0",
    "ec_async_cache_deposit_refund_wait_2": "0",
    "ec_async_cache_member_total_deposit_2": "0",
    "wishcount_2": "0",
    "basketcount_2": "1",
    "CFAE_LC": "CFAE_LC.beatroad_2.JJVAZ6F.1784729411205"
}

# ========== 本地日志输出配置 ==========
current_user = getpass.getuser()
if os.name == "nt":  # Windows
    LOG_FILE = r"D:\fansign\local-ing\SEONGBIN_DIY.csv"
else:  # Linux / macOS
    LOG_FILE = os.path.expanduser("~/yena线下签售.csv")

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# ========== requests 会话配置 ==========
session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=2,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["POST"]
)
adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)
session.mount("http://", adapter)

# ========== 全局线程安全变量 ==========
lines_since_last_push = 0          # 自上次推送后新增的CSV行数
lines_lock = threading.Lock()      # 保护计数器的锁
file_lock = threading.Lock()       # 保护CSV文件读写的锁


# ================== Git 推送函数 ==================
def git_push_update():
    """
    将最新的 CSV 文件提交并推送到 GitHub
    返回: True 表示推送成功, False 表示失败
    """
    try:
        token = os.environ.get('GITHUB_TOKEN')
        if not token:
            print("⚠️ 环境变量 GITHUB_TOKEN 未设置，跳过 Git 推送")
            return False

        remote_url = f"https://{token}@github.com/{GITHUB_REPO}.git"

        # 添加 CSV 文件到暂存区
        subprocess.run(['git', 'add', LOG_FILE], check=True, capture_output=True, timeout=30)

        # 检查是否有文件变化（避免空提交）
        result = subprocess.run(['git', 'diff', '--cached', '--quiet'], capture_output=True, timeout=30)
        if result.returncode != 0:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_msg = f"自动更新数据 {timestamp}"
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True, capture_output=True, timeout=30)
            subprocess.run(
                ['git', 'push', remote_url, f'HEAD:{GITHUB_BRANCH}'],
                check=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            print(f"✅ 已推送到 GitHub: {commit_msg}")
            return True
        else:
            print("⏭️ CSV 文件无变化，跳过推送")
            return True   # 无变化也视为成功

    except subprocess.TimeoutExpired:
        print("❌ Git 操作超时 (30秒)，推送失败")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Git 操作失败: {e.stderr if e.stderr else e}")
        return False
    except Exception as e:
        print(f"❌ 推送过程中发生错误: {e}")
        return False


# ========== 写入本地CSV文件（使用pandas，线程安全） ==========
def write_to_csv_file(time_str, product_name, stock_change, single_sale):
    """
    将监控结果写入本地CSV文件（使用pandas concat方式），并增加计数器
    不在此处触发Git推送
    """
    global lines_since_last_push
    try:
        columns = ["时间", "商品名称", "库存变化", "单笔销量"]

        with file_lock:   # 防止与推送线程同时访问文件
            # 1. 如果文件存在，读取现有数据；否则创建空DataFrame
            if os.path.exists(LOG_FILE):
                df_existing = pd.read_csv(LOG_FILE, encoding='utf-8-sig')
            else:
                df_existing = pd.DataFrame(columns=columns)

            # 2. 将新数据行转换为DataFrame并拼接
            new_row = pd.DataFrame([[time_str, product_name, stock_change, single_sale]], columns=columns)
            df_updated = pd.concat([df_existing, new_row], ignore_index=True)

            # 3. 保存回CSV（覆盖原文件），使用utf-8-sig编码
            df_updated.to_csv(LOG_FILE, index=False, encoding='utf-8-sig')

        # 4. 打印存储的内容（与原格式保持一致）
        print(f"{time_str} 商品[{product_name}] 库存变化: {stock_change}, 单笔销量: {single_sale}")

        # 5. 增加计数器（线程安全）
        with lines_lock:
            lines_since_last_push += 1

    except Exception as e:
        print(f"❌ 写入CSV文件失败: {e}")


# ========== 推送工作线程 ==========
def push_worker():
    global lines_since_last_push
    while True:
        time.sleep(PUSH_INTERVAL)
        with lines_lock:
            pending = lines_since_last_push
        if pending > 0:
            print(f"⏰ 定时推送：有 {pending} 条新数据待推送")
            with file_lock:   # 推送期间禁止写入，保证文件完整
                success = git_push_update()
            if success:
                with lines_lock:
                    lines_since_last_push = 0
                print("✅ 推送成功，计数器已归零")
            else:
                print("⚠️ 推送失败，下次再试")


# ========== 获取库存 ==========
def get_stock_from_api():
    """调用 API 获取 Beatroad 商品库存"""
    try:
        response = session.post(api_url, headers=headers, cookies=cookies, timeout=30)
        response.raise_for_status()
        data = response.json()

        product_list = data.get("product", [])
        stocks = {}
        for product in product_list:
            product_no = product.get("product_no")
            product_name = product.get("product_name", "未知商品")
            stock = product.get("stock_number", None)
            if product_no and stock is not None:
                stocks[product_no] = {"name": product_name, "stock": int(stock)}

        return stocks

    except Exception as e:
        print(f"{datetime.now()} ❌ API请求失败: {e}")
        return {}


# ========== 主监控函数 ==========
def monitor_stock():
    print(f"📄 日志输出路径: {LOG_FILE}")

    previous_stocks = {}
    initial_stocks = {}

    while True:
        current_stocks = get_stock_from_api()
        if not current_stocks:
            print("⚠️ 无法获取库存数量")
        else:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for product_no, info in current_stocks.items():
                product_name = info["name"]
                current_stock = info["stock"]

                # 第一次记录初始库存
                if product_no not in initial_stocks:
                    initial_stocks[product_no] = current_stock
                    previous_stocks[product_no] = current_stock

                    # CSV存储（商品名称硬编码为"beatroad"，保持与原代码一致）
                    write_to_csv_file(current_time, "beatroad", str(current_stock), str(abs(current_stock)))

                    # 打印（打印时使用真实商品名称）
                    log_message = f"{current_time} 商品[{product_name}]({product_no}) 初始库存: {current_stock}"
                    print(log_message)

                # 检测库存变化
                elif current_stock != previous_stocks[product_no]:
                    stock_diff = previous_stocks[product_no] - current_stock

                    # CSV存储（商品名称硬编码为"beatroad"）
                    stock_change_str = f"{previous_stocks[product_no]} -> {current_stock}"
                    write_to_csv_file(current_time, "beatroad", stock_change_str, str(stock_diff))

                    # 打印（打印时使用真实商品名称）
                    change_message = (
                        f"{current_time} 商品[{product_name}]({product_no}) "
                        f"库存变化： {previous_stocks[product_no]} -> {current_stock}, 销量:{stock_diff}"
                    )
                    print(change_message)
                    previous_stocks[product_no] = current_stock

        time.sleep(10)


# ========== 程序入口 ==========
if __name__ == "__main__":
    print(f"启动监控，日志输出到: {LOG_FILE}")
    # 启动推送守护线程
    push_thread = threading.Thread(target=push_worker, daemon=True)
    push_thread.start()

    try:
        monitor_stock()
    except KeyboardInterrupt:
        print("\n监控程序被用户终止")
        # 退出前推送剩余数据
        with lines_lock:
            pending = lines_since_last_push
        if pending > 0:
            print(f"正在推送剩余的 {pending} 条数据...")
            with file_lock:
                success = git_push_update()
            if success:
                print("✅ 剩余数据已推送")
            else:
                print("⚠️ 剩余数据推送失败，请手动检查")
        else:
            print("无待推送数据")