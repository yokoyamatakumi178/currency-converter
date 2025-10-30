import os
import requests

PRECISION = 5

# モード番号と通貨ペアを辞書で管理
MODES = {
    "1": ("JPY", "KRW"),
    "2": ("JPY", "SGD"),
    "3": ("KRW", "JPY"),
    "4": ("SGD", "JPY")
}

# APIキーの読み込み（ローカルの config.py または環境変数）
try:
    from config import API_KEY  # ローカル専用
except ImportError:
    API_KEY = os.getenv("EXCHANGE_API_KEY")  # 環境変数対応

def get_exchange_rates(api_key):
    """APIから日本円を基準としたレートを取得"""
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/JPY"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["conversion_rates"]
    except requests.exceptions.RequestException as e:
        print("❌ レート情報の取得に失敗しました:", e)
        return None

def convert_currency(amount, from_currency, to_currency, rates):
    """金額を通貨換算する"""
    if from_currency == "JPY":
        return amount * rates[to_currency]
    elif to_currency == "JPY":
        return amount / rates[from_currency]
    else:
        raise ValueError("対応していない通貨ペアです。")

def fmt(value, currency):
    """通貨ごとに出力フォーマットを調整"""
    if currency == "KRW":
        return f"{int(value):,}"  # ウォンは小数なし
    else:
        return f"{value:,.{PRECISION}f}"

def main():
    if not API_KEY:
        print("❌ APIキーが設定されていません。config.py または環境変数を確認してください。")
        return

    rates = get_exchange_rates(API_KEY)
    if rates is None:
        return
    print("✅ 為替レート取得完了")

    while True:
        print("\n=== 通貨換算モード ===")
        print("1: 円 → ウォン")
        print("2: 円 → シンガポールドル")
        print("3: ウォン → 円")
        print("4: シンガポールドル → 円")
        print("0: 終了")
        mode = input("番号を選んでください: ")

        if mode == "0":
            print("終了します。")
            break

        if mode not in MODES:
            print("⚠ 無効な選択です。")
            continue

        try:
            amount = float(input("金額を入力してください: "))
            if amount <= 0:
                print("⚠ 0より大きい金額を入力してください。")
                continue
        except ValueError:
            print("⚠ 数字を入力してください。")
            continue

        from_currency, to_currency = MODES[mode]
        try:
            result = convert_currency(amount, from_currency, to_currency, rates)
            print(f"{fmt(amount, from_currency)} {from_currency} = {fmt(result, to_currency)} {to_currency}")
        except ValueError as e:
            print("⚠", e)

if __name__ == "__main__":
    main()
