from __future__ import annotations

# ==================================================
# Import
# ==================================================

import streamlit as st

from config import CONTRACT_SHEET_NAME, PROSPECT_SHEET_NAME
from google_sheets import read_google_sheet
from styles import apply_styles
from ui_components import (
    initialize_state,
    render_crm_tab,
    render_detail_tab,
    render_header,
    render_summary_area,
    render_tab_navigation,
)


# ==================================================
# Configuration
# ==================================================

st.set_page_config(page_title="HOTEL THE SEN CRM", layout="wide")


# ==================================================
# Main Process
# ==================================================


def main() -> None:
    """アプリ全体の初期化、データ取得、タブ別画面描画を実行する。"""
    initialize_state()
    apply_styles()
    render_header()

    try:
        prospect_df, prospect_fetched_at = read_google_sheet(PROSPECT_SHEET_NAME)
        contract_df, contract_fetched_at = read_google_sheet(CONTRACT_SHEET_NAME)
    except Exception as error:
        st.error("Google Sheetsからデータを取得できませんでした。service_account.json、スプレッドシート共有設定、シート名をご確認ください。")
        st.caption(str(error))
        return

    st.caption(f"最終取得時刻：見込み管理 {prospect_fetched_at} / 契約管理 {contract_fetched_at}")

    render_summary_area(prospect_df, contract_df)

    active_tab = render_tab_navigation()

    if active_tab == "見込み管理":
        render_crm_tab(prospect_df, "prospect", contract=False)
    elif active_tab == "契約管理":
        render_crm_tab(contract_df, "contract", contract=True)
    else:
        render_detail_tab(prospect_df, contract_df)


if __name__ == "__main__":
    main()
