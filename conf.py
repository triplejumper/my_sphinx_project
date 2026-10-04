import os
import sys
from pathlib import Path

project = 'Sphinx-Needs Sample'
copyright = '2026, Sample User'
author = 'Sample User'

# 拡張機能の追加
extensions = [
    'sphinx_needs',
]

# テーマの設定
html_theme = 'sphinx_rtd_theme'

# DataTables (インタラクティブ表) の有効化
needs_table_classes = ['datatable']

# カスタムフィールド（任意項目）の定義
needs_fields = {
    'total_hours': {
        'title': '合計工数',
        'description': '作業にかかる合計時間の見積もり',
        'type': 'string',      # スキーマの型指定 ('string', 'number', 'integer' など)
        'nullable': True,      # 未設定 (空値) を許可するかどうか
    },
    'hours': {
        'title': '工数',
        'description': '単体タスクの工数',
        'type': 'string',      # または 'number' (数値として扱う場合)
        'nullable': True,
    },
    'assignee': {
        'title': 'Assignee',
        'type': 'string',
        'default': '',
        'nullable': True,
    },
    'priority': {
        'title': 'Priority',
        'type': 'string',
        'default': '',
        'nullable': True,
    },
}

# 静的ファイルのパス指定
html_static_path = ['_static']

# カスタム CSS の読み込み
html_css_files = [
    'custom.css',
]


# sys.path.append(str(Path(__file__).parent))
import functions

def setup(app):
    # sphinx-needsがロードされた後に登録を促すため、APIを使用
    from sphinx_needs.api.configuration import add_dynamic_function

    add_dynamic_function(app, functions.sum_child_hours)
    # app.connect('need-render-content', functions.on_render_need)
    # add_post_processing(app, functions.update_needs_on_post_build)
    app.connect("build-finished", functions.update_needs_on_post_build)
    app.connect("env-before-read-docs", functions.env_before_read_docs)
    # app.connect("env-updated", functions.env_updated)
    app.connect("html-page-context", functions.html_page_context)

# needs_render_content = functions.on_render_need
