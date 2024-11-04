import requests
import time
import random
import urllib3
import json
import os
from dotenv import load_dotenv
from colorama import init, Fore, Style

# 初始化 colorama
init(autoreset=True)

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 加载配置
load_dotenv()
config = {
    'useProxy': os.getenv('USE_PROXY', 'false').lower() == 'true',
    'minDelay': int(os.getenv('MIN_DELAY', 3)),
    'maxDelay': int(os.getenv('MAX_DELAY', 10)),
    'restartDelay': int(os.getenv('RESTART_DELAY', 241)),
    'accountDelay': int(os.getenv('ACCOUNT_DELAY', 121))
}

class AeropresBot:
    def __init__(self):
        self.api_endpoints = {
            'keepalive': "https://www.aeropres.in/chromeapi/dawn/v1/userreward/keepalive",
            'getPoints': "https://www.aeropres.in/api/atom/v1/userreferral/getpoint"
        }
        self.session = requests.Session()
        self.session.verify = False
        self.load_accounts()

    def load_accounts(self):
        try:
            with open('accounts.json', 'r', encoding='utf-8') as f:
                self.accounts = json.load(f)
        except FileNotFoundError:
            print(f"{Fore.RED}错误: 未找到 accounts.json 文件")
            exit(1)
        except json.JSONDecodeError:
            print(f"{Fore.RED}错误: accounts.json 格式不正确")
            exit(1)

    def display_welcome(self):
        print(f"{Fore.CYAN}{Style.BRIGHT}"+"""
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                         Script Freedom Bot                            ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    """)
        print(f"{Fore.YELLOW}Telegram Channel:{Style.RESET_ALL} https://t.me/ScriptFreedom")
        print(f"{Fore.YELLOW}Telegram Group:{Style.RESET_ALL} https://t.me/ScriptFreedomGroup\n")

    def fetch_points(self, headers):
        try:
            response = self.session.get(self.api_endpoints['getPoints'], headers=headers)
            if response.status_code == 200 and response.json()['status']:
                data = response.json()['data']
                reward_point = data['rewardPoint']
                referral_point = data['referralPoint']
                
                total_points = sum([
                    reward_point.get('points', 0),
                    reward_point.get('registerpoints', 0),
                    reward_point.get('signinpoints', 0),
                    reward_point.get('twitter_x_id_points', 0),
                    reward_point.get('discordid_points', 0),
                    reward_point.get('telegramid_points', 0),
                    reward_point.get('bonus_points', 0),
                    referral_point.get('commission', 0)
                ])
                
                print(f"\n{Fore.GREEN}💰 积分:{Style.BRIGHT} {total_points}")
                return total_points
            else:
                print(f"{Fore.RED}❌ 获取积分失败: {response.json().get('message', '未知错误')}")
        except Exception as e:
            print(f"{Fore.RED}⚠️ 获取积分时出错: {str(e)}")
        return 0

    def keep_alive_request(self, headers, email):
        payload = {
            "username": email,
            "extensionid": "fpdkjdnhkakefebpekbdhillbhonfjjp",
            "numberoftabs": 0,
            "_v": "1.0.8"
        }
        
        try:
            response = self.session.post(self.api_endpoints['keepalive'], json=payload, headers=headers)
            if response.status_code == 200:
                try:
                    json_response = response.json()
                    print(f"{Fore.GREEN}✅ 成功保持存活 {Fore.YELLOW}{email}{Fore.GREEN}: {json_response.get('message', 'Success')}")
                    return True
                except json.JSONDecodeError:
                    print(f"{Fore.GREEN}✅ 成功保持存活 {Fore.YELLOW}{email}{Fore.GREEN}")
                    return True
            else:
                print(f"{Fore.RED}🚫 未能保持存活 {Fore.YELLOW}{email}{Fore.RED}: {response.status_code}")
        except Exception as e:
            print(f"{Fore.RED}⚠️ 请求错误: {str(e)}")
        return False

    def countdown(self, seconds, message="⏳ 下一个过程"):
        for i in range(seconds, 0, -1):
            print(f"{Fore.CYAN}{message}: {Style.BRIGHT}{i} 秒...{Style.RESET_ALL}", end='\r')
            time.sleep(1)
        print(f"\n{Fore.GREEN}🔄 重启中...\n")

    def process_accounts(self):
        self.display_welcome()

        while True:
            total_points = 0

            for account_id, account in self.accounts.items():
                email = account['email']
                token = account['token']
                proxy = account['proxy']

                if config['useProxy'] and not proxy:
                    print(f"{Fore.RED}警告: 账号 {email} 未配置代理")
                    continue

                headers = {
                    "Accept": "*/*",
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
                }

                if config['useProxy'] and proxy:
                    headers['Proxy'] = proxy

                print(f"{Fore.CYAN}{'='*64}")
                print(f"{Fore.YELLOW}📧 账号: {email}")
                print(f"{Fore.BLUE}🌐 代理: {proxy if config['useProxy'] else '未使用代理'}")
                
                points = self.fetch_points(headers)
                total_points += points

                if points > 0:
                    success = self.keep_alive_request(headers, email)
                    if not success:
                        print(f"{Fore.GREEN}✅ 保持存活 {email} 账号\n")
                else:
                    print(f"{Fore.RED}❌ 账号 {email} 没有可用积分")
                    print(f"{Fore.CYAN}{'='*64}")

                self.countdown(config['accountDelay'], "⏳ t.me/ScriptFreedom")

            print(f"{Fore.GREEN}📋 所有账号总积分: {Style.BRIGHT}{total_points}")
            self.countdown(config['restartDelay'])

def main():
    try:
        bot = AeropresBot()
        bot.process_accounts()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}程序已被用户终止{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}程序发生错误: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    main() 