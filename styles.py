import streamlit as st


CSS = """
<style>
:root {
    --sen-navy: #1F2D4A;
    --sen-navy-soft: #2B3B5E;
    --sen-gold: #B89B5E;
    --sen-gold-soft: #F6F0E3;
    --sen-border: #E5E7EB;
    --sen-text: #1F2937;
    --sen-muted: #6B7280;
}
.sen-app-header {
    background: #1F2D4A;
    border: 1px solid rgba(184, 155, 94, 0.38);
    border-radius: 14px;
    padding: 28px 32px;
    margin: 4px 0 18px 0;
    box-shadow: 0 10px 24px rgba(31, 45, 74, 0.16);
}
.sen-app-title {
    color: #FFFFFF;
    font-size: 34px;
    font-weight: 800;
    line-height: 1.2;
    margin: 0;
}
.sen-app-caption {
    color: #E5E7EB;
    font-size: 14px;
    font-weight: 600;
    margin-top: 8px;
}
.sen-summary-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 14px;
    margin: 8px 0 18px 0;
}
.sen-summary-card {
    background: #FFFFFF;
    border: 1px solid var(--sen-border);
    border-radius: 12px;
    padding: 16px 18px;
    box-shadow: 0 6px 18px rgba(31, 45, 74, 0.08);
    border-top: 3px solid var(--sen-gold);
}
.sen-summary-label {
    color: var(--sen-muted);
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 8px;
}
.sen-summary-value {
    color: var(--sen-navy);
    font-size: 26px;
    font-weight: 800;
    line-height: 1.1;
}
.sen-search-title {
    background: #F8F3E8;
    color: var(--sen-navy);
    border: 1px solid #E8DDC5;
    border-radius: 10px;
    padding: 8px 14px;
    font-size: 15px;
    font-weight: 800;
    line-height: 1.3;
    margin-bottom: 14px;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.72);
}
div[class*="st-key-prospect_search_area"] [data-testid="stVerticalBlockBorderWrapper"],
div[class*="st-key-contract_search_area"] [data-testid="stVerticalBlockBorderWrapper"] {
    background: #FAF8F2;
    border-color: #E8DDC5;
    border-radius: 12px;
}
.sen-result-heading {
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--sen-navy);
    font-size: 17px;
    font-weight: 800;
    margin: 18px 0 12px 0;
    padding: 0 0 10px 0;
    background: transparent;
    border-bottom: 1px solid var(--sen-border);
}
.sen-result-count-text {
    color: var(--sen-navy);
    font-size: 17px;
    font-weight: 800;
}
div[class*="st-key-sen_tab_navigation"] {
    margin-top: 18px;
    margin-bottom: 8px;
}
div[class*="st-key-sen_tab_active_"] button {
    background: var(--sen-navy) !important;
    border: 1px solid var(--sen-navy) !important;
    border-radius: 10px !important;
    color: #FFFFFF !important;
    min-height: 44px;
    box-shadow: 0 6px 14px rgba(31, 45, 74, 0.16);
}
div[class*="st-key-sen_tab_active_"] button p {
    color: #FFFFFF !important;
    font-weight: 800 !important;
}
div[class*="st-key-sen_tab_inactive_"] button {
    background: #FFFFFF !important;
    border: 1px solid #D1D5DB !important;
    border-radius: 10px !important;
    color: #6B7280 !important;
    min-height: 44px;
    box-shadow: none;
}
div[class*="st-key-sen_tab_inactive_"] button:hover {
    border-color: rgba(184, 155, 94, 0.72) !important;
    color: var(--sen-navy) !important;
    background: #FBFAF7 !important;
}
div[class*="st-key-sen_tab_inactive_"] button p {
    color: #6B7280 !important;
    font-weight: 700 !important;
}
div[class*="st-key-sen_tab_inactive_"] button:hover p {
    color: var(--sen-navy) !important;
}
div[class*="st-key-prospect_customer_card_"] [data-testid="stVerticalBlockBorderWrapper"],
div[class*="st-key-contract_customer_card_"] [data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid var(--sen-border);
    border-radius: 12px;
    box-shadow: 0 4px 14px rgba(31, 45, 74, 0.07);
    transition: transform 140ms ease, box-shadow 140ms ease, border-color 140ms ease;
    margin-bottom: 10px;
}
div[class*="st-key-prospect_customer_card_"] [data-testid="stVerticalBlockBorderWrapper"]:hover,
div[class*="st-key-contract_customer_card_"] [data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: rgba(184, 155, 94, 0.52);
    box-shadow: 0 10px 24px rgba(31, 45, 74, 0.13);
    transform: translateY(-2px);
}
div[class*="st-key-prospect_customer_card_"] strong,
div[class*="st-key-contract_customer_card_"] strong {
    color: var(--sen-navy);
    font-size: 18px;
}
@media (max-width: 900px) {
    .sen-summary-grid {
        grid-template-columns: 1fr;
    }
    .crm-detail-status {
        grid-template-columns: 1fr 1fr;
    }
    .crm-contract-chart-header {
        grid-template-columns: 1fr;
    }
    .crm-contract-chart-metrics {
        grid-template-columns: 1fr;
    }
}
.crm-section-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    margin-bottom: 16px;
    overflow: hidden;
}
.crm-section-title {
    background: #1E293B;
    color: #FFFFFF;
    padding: 10px 14px;
    font-size: 16px;
    font-weight: 700;
}
.crm-section-body {
    padding: 10px 14px;
}
.crm-field-row {
    display: grid;
    grid-template-columns: 150px minmax(0, 1fr);
    gap: 16px;
    padding: 7px 0;
    border-bottom: 1px solid #F1F5F9;
}
.crm-field-row:last-child {
    border-bottom: 0;
}
.crm-field-label {
    color: #6B7280;
    font-size: 13px;
}
.crm-field-value {
    color: #1F2937;
    font-size: 14px;
    font-weight: 600;
    overflow-wrap: anywhere;
    white-space: pre-wrap;
}
.crm-detail-header {
    background: #F8FAFC;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 18px;
}
.crm-contract-chart-header {
    display: grid;
    grid-template-columns: minmax(260px, 1.1fr) minmax(360px, 1.6fr);
    gap: 22px;
    background: linear-gradient(135deg, #1F2D4A 0%, #2B3B5E 100%);
    border: 1px solid rgba(184, 155, 94, 0.42);
    border-radius: 12px;
    padding: 22px 24px;
    margin-bottom: 18px;
    box-shadow: 0 12px 28px rgba(31, 45, 74, 0.18);
}
.crm-contract-chart-header .crm-detail-label {
    color: #E8DDC5;
    font-weight: 700;
}
.crm-contract-chart-header .crm-detail-name {
    color: #FFFFFF;
    margin-bottom: 10px;
}
.crm-contract-chart-header .crm-detail-company {
    color: #CBD5E1;
}
.crm-contract-chart-main {
    min-width: 0;
}
.crm-contract-chart-side {
    display: grid;
    gap: 14px;
    align-content: center;
}
.crm-contract-chart-profile {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 10px 18px;
}
.crm-contract-chart-profile .crm-detail-value {
    color: #FFFFFF;
}
.crm-contract-chart-tier {
    color: #FEF3C7;
    font-size: 18px;
    font-weight: 800;
}
.crm-contract-chart-metrics {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 10px;
}
.crm-contract-chart-metrics div {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 8px;
    padding: 10px 12px;
    min-width: 0;
}
.crm-contract-chart-metrics span {
    display: block;
    color: #CBD5E1;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 4px;
}
.crm-contract-chart-metrics strong {
    display: block;
    color: #FFFFFF;
    font-size: 16px;
    line-height: 1.35;
    overflow-wrap: anywhere;
}
.crm-detail-name {
    color: #1F2937;
    font-size: 32px;
    font-weight: 700;
    line-height: 1.25;
    margin-bottom: 4px;
}
.crm-detail-company {
    color: #6B7280;
    font-size: 14px;
    margin-bottom: 14px;
}
.crm-detail-status {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 16px;
}
.crm-detail-label {
    color: #6B7280;
    font-size: 12px;
    margin-bottom: 6px;
}
.crm-detail-value {
    color: #1F2937;
    font-size: 15px;
    font-weight: 600;
}
.crm-detail-badge {
    display: inline-block;
    border-radius: 999px;
    padding: 4px 10px;
    font-size: 13px;
    font-weight: 700;
    line-height: 1.4;
    white-space: nowrap;
}
.crm-badge-gray { background: #F1F5F9; color: #475569; }
.crm-badge-blue { background: #DBEAFE; color: #1D4ED8; }
.crm-badge-orange { background: #FFEDD5; color: #C2410C; }
.crm-badge-green { background: #DCFCE7; color: #15803D; }
.crm-badge-yellow { background: #FEF3C7; color: #92400E; }
</style>
"""


def apply_styles() -> None:
    """アプリ全体のCSSを適用する。"""
    st.markdown(CSS, unsafe_allow_html=True)
