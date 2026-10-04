サンプルドキュメント
================================

要件定義 (Requirements)
--------------------------------

.. req:: ユーザー認証機能
   :id: REQ_001
   :status: open
   :priority: High
   :assignee: 山田
   :hours: 5
   :total_hours: [[ sum_child_hours() ]]

   ユーザーはメールアドレスとパスワードでシステムにログインできること。

.. req:: パスワード再設定機能
   :id: REQ_002
   :status: open
   :priority: Medium
   :assignee: 鈴木
   :links: REQ_001
   :hours: 4.25

   登録済みメールアドレス宛に再設定リンクを送信できること。

.. req:: ユーザー認証機能2
   :id: REQ_003
   :priority: High
   :assignee: 山田

   ユーザーはメールアドレスとパスワードでシステムにログインできること。

.. req:: ユーザー認証機能3
   :id: REQ_004
   :status: open
   :priority: High
   :assignee: 山田

   ユーザーはメールアドレスとパスワードでシステムにログインできること。

.. req:: ユーザー認証機能4
   :id: REQ_005
   :status: open
   :priority: High
   :assignee: 山田

   ユーザーはメールアドレスとパスワードでシステムにログインできること。

.. req:: ユーザー認証機能5
   :id: REQ_006
   :status: open
   :priority: High
   :assignee: 山田

   ユーザーはメールアドレスとパスワードでシステムにログインできること。

.. req:: ユーザー認証機能6
   :id: REQ_007
   :status: open
   :priority: High
   :assignee: 山田

   ユーザーはメールアドレスとパスワードでシステムにログインできること。

.. req:: ユーザー認証機能7
   :id: REQ_008
   :status: open
   :priority: High
   :assignee: 山田

   ユーザーはメールアドレスとパスワードでシステムにログインできること。

.. req:: ユーザー認証機能8
   :id: REQ_009
   :status: open
   :priority: High
   :assignee: 山田

   ユーザーはメールアドレスとパスワードでシステムにログインできること。

.. req:: ユーザー認証機能9
   :id: REQ_010
   :status: open
   :priority: High
   :assignee: 山田

   ユーザーはメールアドレスとパスワードでシステムにログインできること。

.. req:: ユーザー認証機能10
   :id: REQ_011
   :status: open
   :priority: High
   :assignee: 山田

   ユーザーはメールアドレスとパスワードでシステムにログインできること。

.. req:: ユーザー認証機能11
   :id: REQ_012
   :status: implemented
   :priority: High
   :assignee: 山田

   ユーザーはメールアドレスとパスワードでシステムにログインできること。


仕様定義 (Specifications)
--------------------------------

.. spec:: 認証API仕様
   :id: SPEC_001
   :status: implemented
   :links: REQ_001,REQ_002
   :total_hours: [[ sum_child_hours() ]]

   POST /api/v1/login リクエストを受け取り、JWTトークンを返す。


テストケース (Test Cases)
--------------------------------

.. test:: 正常系ログインテスト
   :id: TEST_001
   :status: closed
   :links: SPEC_001

   正しいメールアドレスとパスワードで 200 OK が返ることを確認する。


トレーサビリティ一覧 (Needtable)
--------------------------------

.. needtable::
   :types: req, spec, test
   :columns: id, title, status, priority, assignee, links
   :style: datatable


フローグラフ (Needflow)
--------------------------------

.. needflow::
