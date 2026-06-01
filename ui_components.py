from __future__ import annotations

import pandas as pd
import streamlit as st

from constants import (
    ALL_OPTION,
    CONTRACT_DETAIL_SECTIONS,
    DUE_FILTER_OPTIONS,
    NO_VALUE,
    PROSPECT_DETAIL_SECTIONS,
    TAB_MIGRATIONS,
    TAB_OPTIONS,
    TAB_SLUGS,
)
from data_processor import (
    active_prospect_df,
    apply_due_filter,
    contract_amount_total,
    filter_contains,
    find_col,
    format_thousand_yen_amount,
    get_value,
    html_safe,
    markdown_safe,
    prospect_amount_total,
    unique_options,
)


def initialize_state() -> None:
    """Streamlitのセッション状態に初期値を設定する。"""
    defaults = {
        "active_tab": "見込み管理",
        "nav_version": 0,
        "prospect_view": "list",
        "contract_view": "list",
        "prospect_selected_index": None,
        "contract_selected_index": None,
        "detail_target_type": None,
        "detail_target_no": None,
        "detail_target_name": None,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def render_header() -> None:
    """アプリ上部のブランドヘッダーを描画する。"""
    st.markdown(
        """
        <div class="sen-app-header">
            <div class="sen-app-title">HOTEL THE SEN. CRM</div>
            <div class="sen-app-caption">見込み顧客管理・契約管理</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_summary_area(prospect_df: pd.DataFrame, contract_df: pd.DataFrame) -> None:
    """
    サマリーカードを描画する。

    表示内容:
    - 見込み顧客数
    - 見込み金額
    - 契約済み顧客数
    - 契約金額
    """
    prospect_count = len(active_prospect_df(prospect_df))
    contract_count = len(contract_df)
    prospect_amount = format_thousand_yen_amount(prospect_amount_total(prospect_df))
    contract_amount = format_thousand_yen_amount(contract_amount_total(contract_df))

    st.markdown(
        f"""
        <div class="sen-summary-grid">
            <div class="sen-summary-card">
                <div class="sen-summary-label">見込み顧客数</div>
                <div class="sen-summary-value">{prospect_count:,}件</div>
            </div>
            <div class="sen-summary-card">
                <div class="sen-summary-label">見込み金額</div>
                <div class="sen-summary-value">{html_safe(prospect_amount)}</div>
            </div>
            <div class="sen-summary-card">
                <div class="sen-summary-label">契約済み顧客数</div>
                <div class="sen-summary-value">{contract_count:,}件</div>
            </div>
            <div class="sen-summary-card">
                <div class="sen-summary-label">契約金額</div>
                <div class="sen-summary-value">{html_safe(contract_amount)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_search_area(df: pd.DataFrame, prefix: str) -> pd.DataFrame:
    """一覧画面の検索条件エリアを描画し、検索条件を適用したDataFrameを返す。"""
    with st.container(border=True, key=f"{prefix}_search_area"):
        st.markdown('<div class="sen-search-title">検索条件</div>', unsafe_allow_html=True)
        row1 = st.columns(5)
        with row1[0]:
            no = st.text_input("顧客ID / NO", key=f"{prefix}_no")
        with row1[1]:
            name = st.text_input("氏名・会社名", key=f"{prefix}_name")
        with row1[2]:
            stage = st.selectbox("ステージ", unique_options(df, "stage"), key=f"{prefix}_stage")
        with row1[3]:
            tier = st.selectbox("ティア", unique_options(df, "tier"), key=f"{prefix}_tier")
        with row1[4]:
            owner = st.text_input("担当者", key=f"{prefix}_owner")

        awareness_route = ""
        referrer = ""
        next_action = ""
        due_filter = "指定なし"
        if prefix != "contract":
            row2 = st.columns(5)
            with row2[0]:
                awareness_route = st.text_input("認知経路", key=f"{prefix}_awareness_route")
            with row2[1]:
                referrer = st.text_input("紹介者", key=f"{prefix}_referrer")
            with row2[2]:
                next_action = st.text_input("次アクション", key=f"{prefix}_next_action")
            with row2[3]:
                due_filter = st.selectbox("次期日", DUE_FILTER_OPTIONS, key=f"{prefix}_due_filter")
            with row2[4]:
                st.write("")

    result = df.copy()
    result = filter_contains(result, "no", no)
    result = filter_contains(result, "owner", owner)
    if prefix != "contract":
        result = filter_contains(result, "awareness_route", awareness_route)
        result = filter_contains(result, "referrer", referrer)
        result = filter_contains(result, "next_action", next_action)

    if name:
        name_col = find_col(result, "name")
        company_col = find_col(result, "company")
        mask = pd.Series(False, index=result.index)
        for col in [name_col, company_col]:
            if col:
                mask = mask | result[col].astype(str).str.contains(name, case=False, na=False)
        result = result[mask]

    if stage != ALL_OPTION:
        col = find_col(result, "stage")
        if col:
            result = result[result[col].astype(str) == stage]

    if tier != ALL_OPTION:
        col = find_col(result, "tier")
        if col:
            result = result[result[col].astype(str) == tier]

    if prefix != "contract":
        result = apply_due_filter(result, due_filter)
    return result


def parse_probability(value: str) -> float | None:
    """確度表示文字列から数値を取り出す。"""
    if value == NO_VALUE:
        return None
    try:
        return float(value.replace("%", "").strip())
    except ValueError:
        return None


def stage_badge_color(stage: str) -> str:
    """ステージに応じたStreamlitバッジ色を返す。"""
    if "00_要確認" in stage:
        return "gray"
    if "01_アポ取り中" in stage:
        return "blue"
    if "02_面談済" in stage:
        return "primary"
    if "03_提案中" in stage:
        return "orange"
    if "04_サイン待" in stage:
        return "green"
    return "gray"


def tier_badge_color(tier: str) -> str:
    """ティアに応じたStreamlitバッジ色を返す。"""
    if "Imperial Suite" in tier:
        return "yellow"
    if "Sanctuary Suite" in tier:
        return "blue"
    return "gray"


def probability_badge_color(probability: str) -> str:
    """確度に応じたStreamlitバッジ色を返す。"""
    value = parse_probability(probability)
    if value is None:
        return "gray"
    if value >= 100:
        return "green"
    if value >= 80:
        return "blue"
    if value >= 50:
        return "orange"
    return "gray"


def badge_css_class(color: str) -> str:
    """Streamlitバッジ色名をカスタムHTML用CSSクラスへ変換する。"""
    if color == "blue":
        return "crm-badge-blue"
    if color == "orange":
        return "crm-badge-orange"
    if color == "green":
        return "crm-badge-green"
    if color == "yellow":
        return "crm-badge-yellow"
    return "crm-badge-gray"


def select_customer(prefix: str, row_index) -> None:
    """選択顧客をセッションに保存し、詳細画面へ切り替える。"""
    st.session_state[f"{prefix}_selected_index"] = row_index
    st.session_state[f"{prefix}_view"] = "detail"
    st.rerun()


def render_salesforce_header(row: pd.Series, df: pd.DataFrame, show_probability: bool = False) -> None:
    """顧客詳細画面のヘッダーカードを描画する。"""
    name = get_value(row, df, "name")
    company = get_value(row, df, "company")
    stage = get_value(row, df, "stage")
    tier = get_value(row, df, "tier")
    owner = get_value(row, df, "owner")
    probability_html = ""
    if show_probability:
        probability = get_value(row, df, "probability")
        probability_html = (
            '<div><div class="crm-detail-label">見込み確度</div>'
            f'<span class="crm-detail-badge {badge_css_class(probability_badge_color(probability))}">{html_safe(probability)}</span></div>'
        )

    company_html = ""
    if company != NO_VALUE:
        company_html = f'<div class="crm-detail-company">{html_safe(company)}</div>'

    html_block = (
        '<div class="crm-detail-header">'
        '<div class="crm-detail-label">顧客カルテ</div>'
        f'<div class="crm-detail-name">{html_safe(name)}</div>'
        f"{company_html}"
        '<div class="crm-detail-status">'
        '<div><div class="crm-detail-label">ステージ</div>'
        f'<span class="crm-detail-badge {badge_css_class(stage_badge_color(stage))}">{html_safe(stage)}</span></div>'
        '<div><div class="crm-detail-label">ティア</div>'
        f'<span class="crm-detail-badge {badge_css_class(tier_badge_color(tier))}">{html_safe(tier)}</span></div>'
        '<div><div class="crm-detail-label">担当者</div>'
        f'<div class="crm-detail-value">{html_safe(owner)}</div></div>'
        f"{probability_html}"
        "</div></div>"
    )
    st.markdown(html_block, unsafe_allow_html=True)

    st.divider()


def render_customer_card(row: pd.Series, df: pd.DataFrame, prefix: str, contract: bool) -> None:
    """検索結果一覧に表示する顧客カードを描画する。"""
    with st.container(border=True, key=f"{prefix}_customer_card_{row.name}"):
        name = get_value(row, df, "name")
        company = get_value(row, df, "company")
        title = name if name != NO_VALUE else company
        if title == NO_VALUE:
            title = "名称未設定"

        title_col, button_col = st.columns([8, 1])
        title_col.write(f"**{title}**")
        with button_col:
            if st.button("開く", key=f"{prefix}_open_{row.name}", use_container_width=True):
                select_customer(prefix, row.name)

        stage = get_value(row, df, "stage")
        tier = get_value(row, df, "tier")
        badge_cols = st.columns([1, 1, 5] if contract else [1, 1, 1, 5])
        with badge_cols[0]:
            st.badge(stage, color=stage_badge_color(stage))
        with badge_cols[1]:
            st.badge(tier, color=tier_badge_color(tier))
        if not contract:
            with badge_cols[2]:
                probability = get_value(row, df, "probability")
                st.badge(f"確度：{probability}", color=probability_badge_color(probability))

        meta = [
            f"NO: {get_value(row, df, 'no')}",
            f"担当者: {get_value(row, df, 'owner')}",
        ]
        if not contract:
            meta.extend(
                [
                    f"紹介者: {get_value(row, df, 'referrer')}",
                    f"次回アポ: {get_value(row, df, 'next_appointment')}",
                    f"次アクション: {get_value(row, df, 'next_action')}",
                ]
            )
        st.caption(markdown_safe(" / ".join(meta)))


def render_card_list(df: pd.DataFrame, source_df: pd.DataFrame, prefix: str, contract: bool) -> None:
    """検索結果件数と顧客カード一覧を描画する。"""
    st.markdown(
        f'<div class="sen-result-heading"><span>検索結果</span><span class="sen-result-count-text">（{len(df)}件）</span></div>',
        unsafe_allow_html=True,
    )

    if df.empty:
        st.info("条件に一致する顧客が見つかりません。")
        return

    for _, row in df.iterrows():
        render_customer_card(row, source_df, prefix, contract)


def render_section_card(row: pd.Series, df: pd.DataFrame, title: str, fields: list[tuple[str, str]]) -> None:
    """顧客詳細の分類カードをHTMLで描画する。"""
    rows = ""
    for label, key in fields:
        rows += (
            '<div class="crm-field-row">'
            f'<div class="crm-field-label">{html_safe(label)}</div>'
            f'<div class="crm-field-value">{html_safe(get_value(row, df, key))}</div>'
            "</div>"
        )

    html_block = (
        '<div class="crm-section-card">'
        f'<div class="crm-section-title">{html_safe(title)}</div>'
        f'<div class="crm-section-body">{rows}</div>'
        "</div>"
    )
    st.markdown(html_block, unsafe_allow_html=True)


def render_detail_sections(row: pd.Series, df: pd.DataFrame, sections: list[tuple[str, list[tuple[str, str]]]]) -> None:
    """顧客詳細の分類カード群を2列で描画する。"""
    cols = st.columns(2)
    for idx, (title, fields) in enumerate(sections):
        with cols[idx % 2]:
            render_section_card(row, df, title, fields)


def set_detail_target(row: pd.Series, df: pd.DataFrame, prefix: str) -> None:
    """明細タブへ渡す対象顧客情報をセッションに保存する。"""
    st.session_state["detail_target_type"] = prefix
    # 明細タブから戻る際に、元の顧客を再表示するため保持する。
    st.session_state["detail_target_no"] = get_value(row, df, "no")
    st.session_state["detail_target_name"] = get_value(row, df, "name")
    st.session_state["detail_dataset_label"] = "契約管理" if prefix == "contract" else "見込み管理"
    st.session_state["active_tab"] = "明細"
    st.session_state["nav_version"] += 1
    st.rerun()


def render_detail(df: pd.DataFrame, prefix: str, contract: bool) -> None:
    """選択中顧客の詳細画面を描画する。"""
    selected_index = st.session_state.get(f"{prefix}_selected_index")
    if selected_index not in df.index:
        st.session_state[f"{prefix}_view"] = "list"
        st.session_state[f"{prefix}_selected_index"] = None
        st.rerun()

    row = df.loc[selected_index]
    action_cols = st.columns([1, 1, 4])
    if action_cols[0].button("一覧に戻る", key=f"{prefix}_back", use_container_width=True):
        st.session_state[f"{prefix}_view"] = "list"
        st.session_state[f"{prefix}_selected_index"] = None
        st.rerun()
    if action_cols[1].button("この顧客の明細を見る", key=f"{prefix}_detail_tab", use_container_width=True):
        set_detail_target(row, df, prefix)

    render_salesforce_header(row, df, show_probability=(prefix == "prospect"))
    sections = CONTRACT_DETAIL_SECTIONS if contract else PROSPECT_DETAIL_SECTIONS
    render_detail_sections(row, df, sections)


def render_crm_tab(df: pd.DataFrame, prefix: str, contract: bool = False) -> None:
    """見込み管理または契約管理タブの一覧・詳細表示を切り替える。"""
    if df.empty:
        st.warning("表示できるデータがありません。Excelのシート名または明細をご確認ください。")
        return

    if st.session_state.get(f"{prefix}_view") == "detail":
        render_detail(df, prefix, contract)
        return

    filtered = render_search_area(df, prefix)
    render_card_list(filtered, df, prefix, contract)


def clear_detail_target() -> None:
    """明細タブの対象顧客絞り込みを解除する。"""
    st.session_state["detail_target_type"] = None
    st.session_state["detail_target_no"] = None
    st.session_state["detail_target_name"] = None
    st.session_state["detail_clear_requested"] = True


def return_to_customer_detail() -> None:
    """明細タブから元の顧客詳細画面へ戻る。"""
    target_type = st.session_state.get("detail_target_type")
    # 明細へ遷移した元タブを復元し、同じ顧客詳細へ戻す。
    if target_type == "contract":
        st.session_state["active_tab"] = "契約管理"
        st.session_state["contract_view"] = "detail"
    else:
        st.session_state["active_tab"] = "見込み管理"
        st.session_state["prospect_view"] = "detail"
    st.session_state["nav_version"] += 1
    st.rerun()


def reset_detail_search_keys(dataset_key: str) -> None:
    """明細タブの検索条件キーを初期値へ戻す。"""
    for suffix in ["no", "name", "owner", "referrer", "freeword"]:
        st.session_state[f"detail_{dataset_key}_{suffix}"] = ""
    for suffix in ["stage", "tier"]:
        st.session_state[f"detail_{dataset_key}_{suffix}"] = ALL_OPTION


def filter_detail_df(df: pd.DataFrame, filters: dict[str, str]) -> pd.DataFrame:
    """明細タブの検索条件を適用したDataFrameを返す。"""
    result = df.copy()
    result = filter_contains(result, "no", filters["no"])
    result = filter_contains(result, "name", filters["name"])
    result = filter_contains(result, "owner", filters["owner"])
    result = filter_contains(result, "referrer", filters["referrer"])

    if filters["stage"] != ALL_OPTION:
        col = find_col(result, "stage")
        if col:
            result = result[result[col].astype(str) == filters["stage"]]

    if filters["tier"] != ALL_OPTION:
        col = find_col(result, "tier")
        if col:
            result = result[result[col].astype(str) == filters["tier"]]

    freeword = filters["freeword"]
    if freeword:
        mask = pd.Series(False, index=result.index)
        for col in result.columns:
            mask = mask | result[col].astype(str).str.contains(freeword, case=False, na=False)
        result = result[mask]

    return result


def render_detail_search(df: pd.DataFrame, dataset_label: str) -> pd.DataFrame:
    """明細タブの検索条件エリアを描画し、絞り込み結果を返す。"""
    if st.session_state.pop("detail_clear_requested", False):
        reset_detail_search_keys(dataset_label)

    target_no = st.session_state.get("detail_target_no")
    target_name = st.session_state.get("detail_target_name")

    # 顧客詳細から明細へ来た場合は、NOと氏名を検索欄へセットして対象顧客に絞る。
    if target_no and target_no != NO_VALUE:
        default_no = target_no
        default_name = target_name if target_name and target_name != NO_VALUE else ""
        st.session_state[f"detail_{dataset_label}_no"] = default_no
        st.session_state[f"detail_{dataset_label}_name"] = default_name
    elif target_name and target_name != NO_VALUE:
        default_no = ""
        default_name = target_name
        st.session_state[f"detail_{dataset_label}_no"] = default_no
        st.session_state[f"detail_{dataset_label}_name"] = default_name
    else:
        default_no = ""
        default_name = ""

    with st.container(border=True):
        top_cols = st.columns(4)
        with top_cols[0]:
            no = st.text_input("NO", key=f"detail_{dataset_label}_no")
        with top_cols[1]:
            name = st.text_input("氏名", key=f"detail_{dataset_label}_name")
        with top_cols[2]:
            owner = st.text_input("担当者", key=f"detail_{dataset_label}_owner")
        with top_cols[3]:
            referrer = st.text_input("紹介者", key=f"detail_{dataset_label}_referrer")

        bottom_cols = st.columns(4)
        with bottom_cols[0]:
            stage = st.selectbox("ステージ", unique_options(df, "stage"), key=f"detail_{dataset_label}_stage")
        with bottom_cols[1]:
            tier = st.selectbox("ティア", unique_options(df, "tier"), key=f"detail_{dataset_label}_tier")
        with bottom_cols[2]:
            freeword = st.text_input("フリーワード", key=f"detail_{dataset_label}_freeword")
        with bottom_cols[3]:
            st.write("")
            if st.button("絞り込み解除", key=f"detail_{dataset_label}_clear", use_container_width=True):
                clear_detail_target()
                st.rerun()

    return filter_detail_df(
        df,
        {
            "no": no,
            "name": name,
            "owner": owner,
            "stage": stage,
            "tier": tier,
            "referrer": referrer,
            "freeword": freeword,
        },
    )


def render_detail_tab(prospect_df: pd.DataFrame, contract_df: pd.DataFrame) -> None:
    """明細データタブを描画する。"""
    target_type = st.session_state.get("detail_target_type")
    target_name = st.session_state.get("detail_target_name")
    if target_type in {"prospect", "contract"}:
        back_label = "← 顧客情報へ戻る"
        if target_name and target_name != NO_VALUE:
            back_label = f"← {target_name}の顧客情報へ戻る"
        if st.button(back_label, key="detail_back_to_customer"):
            return_to_customer_detail()

    st.subheader("明細")

    target_type = st.session_state.get("detail_target_type")
    if target_type == "contract":
        st.session_state["detail_dataset_label"] = "契約管理"
    elif target_type == "prospect":
        st.session_state["detail_dataset_label"] = "見込み管理"

    dataset_label = st.radio(
        "対象データ",
        ["見込み管理", "契約管理"],
        horizontal=True,
        key="detail_dataset_label",
    )
    df = prospect_df if dataset_label == "見込み管理" else contract_df

    filtered = render_detail_search(df, "prospect" if dataset_label == "見込み管理" else "contract")
    st.write(f"表示件数: {len(filtered)} 件")
    st.dataframe(filtered, use_container_width=True, hide_index=True)


def render_tab_navigation() -> str:
    """上部タブ風ナビゲーションを描画し、選択中タブ名を返す。"""
    # 旧タブ名がセッションに残っている場合でも、現在のタブ名へ移行して表示を保つ。
    active_tab = TAB_MIGRATIONS.get(st.session_state.get("active_tab"), st.session_state.get("active_tab", "見込み管理"))
    if active_tab not in TAB_OPTIONS:
        active_tab = "見込み管理"
    st.session_state["active_tab"] = active_tab

    with st.container(key="sen_tab_navigation"):
        cols = st.columns(3)
        for option, col in zip(TAB_OPTIONS, cols):
            status = "active" if option == active_tab else "inactive"
            slug = TAB_SLUGS[option]
            with col.container(key=f"sen_tab_{status}_{slug}"):
                if st.button(option, key=f"nav_{slug}", use_container_width=True):
                    if option != active_tab:
                        st.session_state["active_tab"] = option
                        st.rerun()

    return st.session_state.get("active_tab", "見込み管理")
