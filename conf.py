import os
import sys

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
