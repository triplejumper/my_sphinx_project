from sphinx.util import logging
sphinx_logger = logging.getLogger(__name__)

def on_render_need(app, need, needs, *args, **kwargs):
    sphinx_logger.info(f"on_render_need")
    """
    項目（Need）が画面に表示・レンダリングされるタイミングで呼び出される
    - need: 現在描画しようとしている Need の辞書データ
    - needs: 全 Need のデータ辞書
    """
    need_id = need['id']
    
    # 1. 表示直前に子Needの工数を集計して 'hours' を動的更新
    links = need.get('links', [])
    if links:
        total = 0.0
        for child_id in links:
            if child_id in needs:
                try:
                    total += float(needs[child_id].get('hours', 0))
                except (ValueError, TypeError):
                    pass
        # 描画用データとして表示直前にセット
        need['hours'] = f"{total:.1f}"

    # 2. 表示タイミングで本文（content）の末尾に動的注記を挿入する例
    if need.get('status') == 'implemented':
        # need['content'] は項目の本文テキスト
        need['content'] += f"\n\n.. note:: この項目は現在作業中です（最終更新確認: {need_id}）。"


# def sum_child_hours(need, logger, *args, **kwargs):
#     """
#     リンクされている子Needの 'hours' 値を合計する動的関数
#     """
#     from sphinx.builders import Builder
    
#     # Sphinxの環境オブジェクトから全Needのデータを取得
#     # needs_all_needs は {need_id: need_dict} の形式
#     env = need['app'].builder.env
#     all_needs = getattr(env, 'needs_all_needs', {})
    
#     total_hours = 0.0
    
#     # このNeedにリンクしている（child_needs または links で指定された）Need IDを取得
#     # ※ Sphinx-Needsの設定で links などのカスタムリンクを定義している場合は適宜変更
#     links = need.get('links', [])
    
#     for linked_id in links:
#         if linked_id in all_needs:
#             linked_need = all_needs[linked_id]
#             # 子Needの 'hours' オプションを取得（文字列で入っている場合があるため float に変換）
#             hours_val = linked_need.get('hours', 0)
#             try:
#                 total_hours += float(hours_val)
#             except (ValueError, TypeError):
#                 pass

#     return f"{total_hours:.1f}h"


def _get_all_needs_safely(app):
    """sphinx-needs のバージョン差分を吸収して全 Need データを安全に取得するヘルパー関数"""
    env = getattr(app, "env", None) or app.builder.env

    # 1. 最新の sphinx-needs (SphinxNeedsData) から取得を試みる
    try:
        from sphinx_needs.data import SphinxNeedsData

        needs_data_obj = SphinxNeedsData(env)

        # バージョンごとのアクセス方法を順番に試行
        if hasattr(needs_data_obj, "get_or_create_needs"):
            # sphinx_logger.info(f"get_or_create_needs")
            return needs_data_obj.get_or_create_needs()
        elif hasattr(needs_data_obj, "get_needs_view"):
            # sphinx_logger.info(f"get_needs_view")
            return needs_data_obj.get_needs_view()
        elif hasattr(needs_data_obj, "needs"):
            # sphinx_logger.info(f"needs")
            return needs_data_obj.needs
    except (ImportError, Exception) as e:
        sphinx_logger.debug(f"SphinxNeedsData からの取得をスキップ: {e}")

    # 2. 従来(〜v1.x)の env.needs_all_needs から取得
    all_needs = getattr(env, "needs_all_needs", {})
    if all_needs:
        # sphinx_logger.info(f"needs_all_needs")
        return all_needs

    # 3. env.needs_data 等の別ルートをフォールバック検索
    if hasattr(env, "needs_data"):
        needs_data = getattr(env, "needs_data")
        if isinstance(needs_data, dict):
            # sphinx_logger.info(f"needs_data (dict)")
            return needs_data
        elif hasattr(needs_data, "needs"):
            sphinx_logger.info(f"needs_data (object with 'needs' attribute)")
            return needs_data.needs

    return {}


def sum_child_hours(app, need, *args, **kwargs):
    all_needs = _get_all_needs_safely(app)

    # sphinx_logger.info(f"Processing links for need : {need['id']}, links: {need.get('links', [])}")
    # sphinx_logger.info(f"all_needs : {all_needs}")

    total_hours = 0.0
    links = need.get('links', [])
    for linked_id in links:
        if linked_id in all_needs:
            linked_need = all_needs[linked_id]
            # 子Needの 'hours' オプションを取得（文字列で入っている場合があるため float に変換）
            hours_val = linked_need.get('hours', 0)
            try:
                total_hours += float(hours_val)
            except (ValueError, TypeError):
                pass

    return f"{total_hours:.2f}"


def update_needs_on_post_build(app, exception):
    sphinx_logger.info(f"update_needs_on_post_build")
    """全 Need の構築完了後に要素を上書きするフック関数"""

    # all_needs = _get_all_needs_safely(app)
    # sphinx_logger.info(f"all_needs : {all_needs}")
    # all_needs['REQ_001']['hours'] = "3.0"
    # sphinx_logger.info(f"all_needs[''REQ_001''] : {all_needs['REQ_001']['hours'] if 'REQ_001' in all_needs else 'Not Found'}")
    # for need_id, need in needs.items():
    #     # 1. カスタムフィールドの上書き
    #     need["hours"] = "5.0"

    #     # 2. 条件に応じた動的な上書き
    #     if need.get("type") == "req":
    #         need["status"] = "IN_PROGRESS"

    #     # 3. 本文 (content) の上書き・追加
    #     if "jira_id" in need:
    #         need["content"] += f"\n\n.. note:: Jira ID: {need['jira_id']}"
    pass

def env_before_read_docs(app, exception, list):
    sphinx_logger.info(f"env_before_read_docs")
    """全 Need の構築完了後に要素を上書きするフック関数"""
    # all_needs = _get_all_needs_safely(app)
    # sphinx_logger.info(f"all_needs : {all_needs}")
    # for need_id, need in needs.items():
    #     # 1. カスタムフィールドの上書き
    #     need["hours"] = "5.0"

    #     # 2. 条件に応じた動的な上書き
    #     if need.get("type") == "req":
    #         need["status"] = "IN_PROGRESS"

    #     # 3. 本文 (content) の上書き・追加
    #     if "jira_id" in need:
    #         need["content"] += f"\n\n.. note:: Jira ID: {need['jira_id']}"
    pass

def env_updated(app, env):
    sphinx_logger.info(f"env_updated")
    """全 Need の構築完了後に要素を上書きするフック関数"""

    all_needs = _get_all_needs_safely(app)
    sphinx_logger.info(f"all_needs : {all_needs}")
    all_needs['REQ_001']['hours'] = "3.0"
    sphinx_logger.info(f"all_needs[''REQ_001''] : {all_needs['REQ_001']['hours'] if 'REQ_001' in all_needs else 'Not Found'}")
    # for need_id, need in needs.items():
    #     # 1. カスタムフィールドの上書き
    #     need["hours"] = "5.0"

    #     # 2. 条件に応じた動的な上書き
    #     if need.get("type") == "req":
    #         need["status"] = "IN_PROGRESS"

    #     # 3. 本文 (content) の上書き・追加
    #     if "jira_id" in need:
    #         need["content"] += f"\n\n.. note:: Jira ID: {need['jira_id']}"
    pass


def html_page_context(app , pagename , templatename , context , doctree):
    sphinx_logger.info(f"html_page_context")
    """全 Need の構築完了後に要素を上書きするフック関数"""

    all_needs = _get_all_needs_safely(app)
    sphinx_logger.info(f"all_needs : {all_needs}")
    all_needs['REQ_001']['hours'] = "3.0"
    sphinx_logger.info(f"all_needs[''REQ_001''] : {all_needs['REQ_001']['hours'] if 'REQ_001' in all_needs else 'Not Found'}")
    # for need_id, need in needs.items():
    #     # 1. カスタムフィールドの上書き
    #     need["hours"] = "5.0"

    #     # 2. 条件に応じた動的な上書き
    #     if need.get("type") == "req":
    #         need["status"] = "IN_PROGRESS"

    #     # 3. 本文 (content) の上書き・追加
    #     if "jira_id" in need:
    #         need["content"] += f"\n\n.. note:: Jira ID: {need['jira_id']}"
    pass
