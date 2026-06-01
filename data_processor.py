from __future__ import annotations

from datetime import datetime
from typing import Any
import html
import unicodedata

import pandas as pd

from constants import (
    ACTIVE_PROSPECT_STAGE_PREFIXES,
    ALL_OPTION,
    COLUMN_ALIASES,
    DUE_FILTER_DAYS,
    MAN_YEN_PER_OKU_YEN,
    NO_VALUE,
    PROSPECT_AMOUNT_COLUMN_CANDIDATES,
    SUMMARY_AMOUNT_UNIT_DIVISOR,
)


def find_col(df: pd.DataFrame, key: str) -> str | None:
    """列キーに対応する実列名をエイリアスから探す。"""
    aliases = COLUMN_ALIASES.get(key, [])
    for alias in aliases:
        if alias in df.columns:
            return alias

    normalized_cols = {normalize_column_name(col): col for col in df.columns}
    for alias in aliases:
        match = normalized_cols.get(normalize_column_name(alias))
        if match:
            return match

    for alias in aliases:
        normalized_alias = normalize_column_name(alias)
        if len(normalized_alias) < 3:
            continue
        for normalized_col, col in normalized_cols.items():
            if normalized_alias in normalized_col:
                return col

    return None


def normalize_column_name(value: Any) -> str:
    """列名比較用に改行・半角/全角スペース差異を吸収する。"""
    text = unicodedata.normalize("NFKC", str(value)).strip().lower()
    return "".join(text.split())


def get_raw(row: pd.Series, df: pd.DataFrame, key: str) -> Any | None:
    """行データから列キーに対応する未整形値を取得する。"""
    col = find_col(df, key)
    if col is None:
        return None
    value = row.get(col)
    if value is None or pd.isna(value):
        return None
    return value


def is_blank_text(text: str) -> bool:
    """空欄扱いにする文字列かどうかを判定する。"""
    normalized = unicodedata.normalize("NFKC", text).strip()
    lowered = normalized.lower()
    if lowered in {"", "-", "none", "nan", "nat", "<na>"}:
        return True

    bullet_chars = {"・", "･", "•", "●", "○", "·", "∙", "‧", "⦁", "ㆍ"}
    return all(char in bullet_chars for char in normalized)


def format_value(value: Any, key: str | None = None) -> str:
    """画面表示用に値を整形する。"""
    if value is None:
        return NO_VALUE
    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y/%m/%d")
    if isinstance(value, datetime):
        return value.strftime("%Y/%m/%d")

    if key == "probability":
        try:
            number = float(value)
        except (TypeError, ValueError):
            text = str(value).strip()
            return NO_VALUE if is_blank_text(text) else text
        if pd.isna(number):
            return NO_VALUE
        if number <= 1:
            number *= 100
        return f"{number:.0f}%"

    if isinstance(value, float):
        if pd.isna(value):
            return NO_VALUE
        if value.is_integer():
            return str(int(value))

    text = str(value).strip()
    if is_blank_text(text):
        return NO_VALUE
    return text if text else NO_VALUE


def get_value(row: pd.Series, df: pd.DataFrame, key: str) -> str:
    """行データから列キーに対応する表示用文字列を取得する。"""
    return format_value(get_raw(row, df, key), key)


def markdown_safe(value: str) -> str:
    """Markdownでハイフンが箇条書き化しないように整形する。"""
    if value == NO_VALUE:
        return r"\-"
    return value


def html_safe(value: str) -> str:
    """HTML描画用に文字列をエスケープする。"""
    return html.escape(value, quote=True)


def unique_options(df: pd.DataFrame, key: str) -> list[str]:
    """フィルター用の一意な選択肢を作成する。"""
    col = find_col(df, key)
    if col is None:
        return [ALL_OPTION]

    values = []
    for item in df[col].dropna().tolist():
        text = format_value(item)
        if text != NO_VALUE:
            values.append(text)
    return [ALL_OPTION] + sorted(set(values))


def filter_contains(df: pd.DataFrame, key: str, query: str) -> pd.DataFrame:
    """指定列に検索語を含む行だけを返す。"""
    if not query:
        return df
    col = find_col(df, key)
    if col is None:
        return df
    return df[df[col].astype(str).str.contains(query, case=False, na=False)]


def apply_due_filter(df: pd.DataFrame, due_filter: str) -> pd.DataFrame:
    """次期日フィルターを適用する。"""
    if due_filter == "指定なし":
        return df

    col = find_col(df, "due_date")
    if col is None:
        return df.iloc[0:0]

    today = pd.Timestamp(datetime.today().date())
    due = pd.to_datetime(df[col], errors="coerce")

    if due_filter in DUE_FILTER_DAYS:
        return df[(due >= today) & (due <= today + pd.Timedelta(days=DUE_FILTER_DAYS[due_filter]))]
    if due_filter == "期限超過":
        return df[due < today]

    return df


def parse_amount_number(value: Any) -> float | None:
    """金額文字列からカンマや通貨記号を除去して数値化する。"""
    if value is None or pd.isna(value):
        return None
    text = unicodedata.normalize("NFKC", str(value)).strip()
    if is_blank_text(text):
        return None
    cleaned = (
        text.replace(",", "")
        .replace("円", "")
        .replace("¥", "")
        .replace("￥", "")
        .replace(" ", "")
    )
    try:
        return float(cleaned)
    except ValueError:
        return None


def total_amount_by_columns(df: pd.DataFrame, candidates: list[str]) -> float | None:
    """候補列名のうち最初に見つかった金額列を合計する。"""
    for candidate in candidates:
        if candidate in df.columns:
            return sum(parse_amount_number(value) or 0 for value in df[candidate].tolist())
    return None


def active_prospect_df(df: pd.DataFrame) -> pd.DataFrame:
    """サマリー集計対象となる見込み顧客だけに絞り込む。"""
    stage_col = find_col(df, "stage")
    if stage_col is None:
        return df

    # 00_要確認は営業管理対象から外すため、対象ステージを明示して集計する。
    stages = df[stage_col].astype(str).str.strip()
    return df[stages.str.startswith(ACTIVE_PROSPECT_STAGE_PREFIXES)]


def prospect_amount_total(df: pd.DataFrame) -> float | None:
    """見込み管理データからサマリー用の見込み金額合計を算出する。"""
    amount_col = find_col(df, "amount")
    if amount_col is None:
        amount_col = next((col for col in PROSPECT_AMOUNT_COLUMN_CANDIDATES if col in df.columns), None)
    if amount_col is None:
        return None

    # 見込み金額も見込み顧客数と同じ対象ステージに揃える。
    result = active_prospect_df(df)
    return sum(parse_amount_number(value) or 0 for value in result[amount_col].tolist())


def contract_amount_total(df: pd.DataFrame) -> float | None:
    """契約管理データからサマリー用の契約金額合計を算出する。"""
    target_cols = [
        c for c in df.columns
        if "会員権金額" in str(c)
    ]

    return total_amount_by_columns(df, target_cols)


def format_thousand_yen_amount(amount_thousand_yen: float | None) -> str:
    """千円単位の金額を万円・億円表示へ変換する。"""
    if amount_thousand_yen is None:
        return NO_VALUE
    man_yen = amount_thousand_yen / SUMMARY_AMOUNT_UNIT_DIVISOR
    if man_yen >= MAN_YEN_PER_OKU_YEN:
        oku_yen = man_yen / MAN_YEN_PER_OKU_YEN
        return f"{oku_yen:.2f}".rstrip("0").rstrip(".") + "億円"
    return f"{man_yen:,.0f}万円"
