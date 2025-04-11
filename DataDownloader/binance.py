import sys
import os
import ccxt
import pandas as pd
from pathlib import Path


def download_klines(
    symbol: str, timeframe: str, start_date: str, output_dir: str = None
):
    """
    从币安下载K线数据并保存为CSV

    Args:
        symbol: 交易对符号，如 "BTC/USDT"
        timeframe: K线周期，如 "1d", "1h", "15m" 等
        start_date: 起始日期，格式为 "YYYY-MM-DD"
        output_dir: 输出目录，默认为脚本所在目录
    """
    # 初始化币安接口
    exchange = ccxt.binance()

    # 转换timeframe到文件名格式
    timeframe_map = {
        "1d": "day",
        "1h": "60m",
        "30m": "30m",
        "15m": "15m",
        "5m": "5m",
        "1m": "1m",
    }

    if timeframe not in timeframe_map:
        raise ValueError(
            f"Unsupported timeframe: {timeframe}. Supported: {list(timeframe_map.keys())}"
        )

    # 转换交易对格式，如 BTC/USDT -> btcusdt
    symbol_formatted = symbol.lower().replace("/", "")

    # 构建输出文件路径
    if output_dir is None:
        output_dir = os.path.dirname(os.path.realpath(__file__))

    filename = f"{symbol_formatted}_{timeframe_map[timeframe]}.csv"
    filepath = Path(output_dir) / filename

    # 下载数据
    since = exchange.parse8601(f"{start_date}T00:00:00")
    klines = []

    print(f"Downloading {symbol} {timeframe} klines from {start_date}...")

    while True:
        try:
            data = exchange.fetch_ohlcv(
                symbol,
                timeframe=timeframe,
                since=since,
                limit=1000,  # 币安每次最多返回1000根K线
            )

            if not data:
                break

            klines.extend(data)
            since = data[-1][0] + 1  # 更新获取下一批的起始时间

            print(f"Downloaded {len(klines)} klines...", end="\r")

        except Exception as e:
            print(f"\nError: {e}")
            break

    print(f"\nTotal downloaded: {len(klines)} klines")

    if not klines:
        print("No data downloaded")
        return

    # 转换为DataFrame并格式化
    df = pd.DataFrame(
        klines, columns=["timestamp", "open", "high", "low", "close", "volume"]
    )

    # 转换时间戳为datetime格式
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")

    # 仅保留需要的列并按csvAPI.py的格式排序
    df = df[["timestamp", "open", "high", "low", "close"]]

    # 保存为CSV
    df.to_csv(filepath, index=False)
    print(f"Data saved to {filepath}")


def main():
    if len(sys.argv) < 4:
        print(
            "Usage: python download_binance.py <symbol> <timeframe> <start_date> [output_dir]"
        )
        print("Example: python download_binance.py BTC/USDT 1d 2020-01-01")
        sys.exit(1)

    symbol = sys.argv[1]
    timeframe = sys.argv[2]
    start_date = sys.argv[3]
    output_dir = sys.argv[4] if len(sys.argv) > 4 else None

    download_klines(symbol, timeframe, start_date, output_dir)


if __name__ == "__main__":
    main()