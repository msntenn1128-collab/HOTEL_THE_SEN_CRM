ALL_OPTION = "すべて"
NO_VALUE = "-"

GOOGLE_SHEETS_CACHE_TTL_SECONDS = 100
SHEET_HEADER_ROW_INDEX = 2
SHEET_DATA_START_ROW_INDEX = 3
MIN_SHEET_ROW_COUNT = 3

SUMMARY_AMOUNT_UNIT_DIVISOR = 10
MAN_YEN_PER_OKU_YEN = 10000

DUE_FILTER_OPTIONS = ["指定なし", "7日以内", "14日以内", "30日以内", "期限超過"]
DUE_FILTER_DAYS = {"7日以内": 7, "14日以内": 14, "30日以内": 30}

ACTIVE_PROSPECT_STAGE_PREFIXES = ("01_アポ取り中", "02_説明済", "03_回答待ち", "04_サイン待")
PROSPECT_AMOUNT_COLUMN_CANDIDATES = [
    "金額見込(千円)",
    "金額見込 (千円)",
    "見込み金額(千円)",
    "見込み金額 (千円)",
    "金額見込",
]

TAB_OPTIONS = ["見込み管理", "契約管理", "明細"]
TAB_SLUGS = {"見込み管理": "prospect", "契約管理": "contract", "明細": "detail"}
TAB_MIGRATIONS = {
    "見込み顧客": "見込み管理",
    "契約済み顧客": "契約管理",
    "明細データ": "明細",
}

COLUMN_ALIASES = {
    "no": ["NO", "No", "ID", "顧客ID", "顧客No", "顧客番号"],
    "owner": ["担当者", "担当", "営業担当", "担当スタッフ"],
    "name": ["氏名", "顧客名", "お客様名", "名前"],
    "company": ["会社名", "法人名", "企業名", "団体名"],
    "company_hp": ["会社HP", "HP", "ホームページ", "URL", "Webサイト", "ウェブサイト"],
    "stage": ["ステージ", "商談ステージ", "進捗", "状況"],
    "tier": ["ティア", "ランク", "顧客ランク", "グレード"],
    "amount": ["金額", "見込金額", "見込み金額", "契約金額", "売上見込", "金額見込"],
    "weighted_amount": ["加重金額", "加重売上", "加重見込金額"],
    "probability": ["見込み確度", "確度", "受注確度"],
    "awareness_route": ["認知経路", "流入経路", "出逢い", "接点", "認知"],
    "referrer": ["紹介者", "紹介元"],
    "first_contact": ["初回接触日", "初回連絡日"],
    "last_contact": ["最終接触日", "最終連絡日"],
    "next_action": ["次アクション", "次回アクション", "次回対応"],
    "next_appointment": ["次回アポ", "次回予定"],
    "due_date": ["次期日", "次回日", "次回予定日", "対応期限", "期限"],
    "conversation": ["話した内容", "会話内容", "商談内容"],
    "success_reason": ["成約理由", "契約理由"],
    "lost_reason": ["成約に至らず理由", "失注理由", "未成約理由"],
    "memo": ["備考", "メモ", "商談メモ"],
    "contract_date": ["契約日", "成約日", "申込日"],
    "contract_amount": ["会員権金額", "契約金額", "受注金額", "成約金額", "金額"],
    "plan": ["プラン", "商品", "客室", "利用プラン"],
    "payment_status": ["入金状況", "入金ステータス", "支払状況"],
    "payment_due_date": ["入金予定日", "支払期日", "請求期日"],
    "payment_date": ["入金日", "支払日"],
    "invoice_no": ["請求書番号", "請求No", "Invoice No"],
    "procedure_status": ["手続き状況", "契約手続き", "進行状況"],
    "sales_record_date": ["売上計上日", "計上日"],
    "sales_month": ["売上計上月", "計上月", "売上月"],
    "revenue_category": ["売上区分", "売上分類"],
}

PROSPECT_DETAIL_SECTIONS = [
    ("基本情報", [("NO", "no"), ("担当者", "owner"), ("氏名", "name"), ("会社名", "company"), ("会社HP", "company_hp")]),
    (
        "進捗・興味",
        [("ステージ", "stage"), ("ティア", "tier"), ("金額", "amount"), ("見込み確度", "probability"), ("加重金額", "weighted_amount")],
    ),
    (
        "出逢い・接点",
        [("認知経路", "awareness_route"), ("紹介者", "referrer"), ("初回接触日", "first_contact"), ("最終接触日", "last_contact")],
    ),
    (
        "フォロー・結果",
        [
            ("次アクション", "next_action"),
            ("次回アポ", "next_appointment"),
            ("次期日", "due_date"),
            ("話した内容", "conversation"),
            ("成約理由", "success_reason"),
            ("成約に至らず理由", "lost_reason"),
            ("備考", "memo"),
        ],
    ),
]

CONTRACT_DETAIL_SECTIONS = [
    ("基本情報", [("NO", "no"), ("担当者", "owner"), ("氏名", "name"), ("会社名", "company"), ("会社HP", "company_hp")]),
    (
        "契約・金額",
        [("ステージ", "stage"), ("ティア", "tier"), ("契約日", "contract_date"), ("契約金額", "contract_amount"), ("プラン", "plan")],
    ),
    (
        "手続き・入金",
        [
            ("手続き状況", "procedure_status"),
            ("請求書番号", "invoice_no"),
            ("入金状況", "payment_status"),
            ("入金予定日", "payment_due_date"),
            ("入金日", "payment_date"),
        ],
    ),
    (
        "売上計上",
        [("売上計上月", "sales_month"), ("売上計上日", "sales_record_date"), ("売上区分", "revenue_category"), ("備考", "memo")],
    ),
]
