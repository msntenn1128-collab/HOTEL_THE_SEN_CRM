from datetime import datetime
from pathlib import Path

import gspread
import pandas as pd
import streamlit as st

from config import GOOGLE_SHEETS_ID, SERVICE_ACCOUNT_FILE
from constants import (
    GOOGLE_SHEETS_CACHE_TTL_SECONDS,
    MIN_SHEET_ROW_COUNT,
    SHEET_DATA_START_ROW_INDEX,
    SHEET_HEADER_ROW_INDEX,
)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """空行を除外し、列名の改行と前後空白を取り除く。"""
    df = df.dropna(how="all").copy()
    df.columns = [str(col).replace("\n", "").strip() for col in df.columns]
    return df


@st.cache_data(ttl=GOOGLE_SHEETS_CACHE_TTL_SECONDS)
def read_google_sheet(sheet_name: str) -> tuple[pd.DataFrame, str]:
    """Google Sheetsから指定シートを取得し、DataFrameと取得時刻を返す。"""
    print("Google Sheets取得")
    fetched_at = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    # サービスアカウントJSONを使い、ユーザー操作なしで本番運用できる接続方式にしている。
    client = gspread.service_account(filename=str(Path(SERVICE_ACCOUNT_FILE)))
    spreadsheet = client.open_by_key(GOOGLE_SHEETS_ID)
    worksheet = spreadsheet.worksheet(sheet_name)
    values = worksheet.get_all_values()

    if len(values) < MIN_SHEET_ROW_COUNT:
        return pd.DataFrame(), fetched_at

    # Google Sheetsは1-2行目がタイトル/集計、3行目がヘッダーという前提。
    header = values[SHEET_HEADER_ROW_INDEX]
    rows = values[SHEET_DATA_START_ROW_INDEX:]
    normalized_rows = [(row + [""] * len(header))[: len(header)] for row in rows]
    df = pd.DataFrame(normalized_rows, columns=header)
    return normalize_columns(df), fetched_at
