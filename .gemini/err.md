[2025-07-28 05:21:03 +0000] [103] [CRITICAL] WORKER TIMEOUT (pid:617)
[2025-07-28 05:21:03 +0000] [617] [ERROR] Error handling request /callback
Traceback (most recent call last):
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/gunicorn/workers/sync.py", line 134, in handle
    self.handle_request(listener, req, client, addr)
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/gunicorn/workers/sync.py", line 177, in handle_request
    respiter = self.wsgi(environ, resp.start_response)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/flask/app.py", line 1536, in __call__
    return self.wsgi_app(environ, start_response)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/flask/app.py", line 1511, in wsgi_app
    response = self.full_dispatch_request()
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/flask/app.py", line 917, in full_dispatch_request
    rv = self.dispatch_request()
         ^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/flask/app.py", line 902, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/app.py", line 177, in callback
    handler.handle(body, signature)
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/linebot/v3/webhook.py", line 227, in handle
    self.__invoke_func(func, event, payload)
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/linebot/v3/webhook.py", line 237, in __invoke_func
    func(event, payload.destination)
  File "/opt/render/project/src/app.py", line 116, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/app.py", line 216, in handle_message
    reply_message(event, messages)
  File "/opt/render/project/src/app.py", line 260, in reply_message
    line_bot_api.reply_message(
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/pydantic/v1/decorator.py", line 40, in wrapper_function
    return vd.call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/pydantic/v1/decorator.py", line 134, in call
    return self.execute(m)
           ^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/pydantic/v1/decorator.py", line 206, in execute
    return self.raw_function(**d, **var_kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/linebot/v3/messaging/api/messaging_api.py", line 6944, in reply_message
    return self.reply_message_with_http_info(reply_message_request, **kwargs)  # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
None
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/pydantic/v1/decorator.py", line 40, in wrapper_function
{'mode': 'first', 'name': '白いフラン'}
127.0.0.1 - - [28/Jul/2025:05:21:04 +0000] "POST /callback HTTP/1.1" 500 0 "-" "-"
    return vd.call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/pydantic/v1/decorator.py", line 134, in call
    return self.execute(m)
           ^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/pydantic/v1/decorator.py", line 206, in execute
    return self.raw_function(**d, **var_kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/linebot/v3/messaging/api/messaging_api.py", line 7049, in reply_message_with_http_info
    return self.api_client.call_api(
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/linebot/v3/messaging/api_client.py", line 407, in call_api
    return self.__call_api(resource_path, method,
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/linebot/v3/messaging/api_client.py", line 212, in __call_api
    response_data = self.request(
                    ^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/linebot/v3/messaging/api_client.py", line 451, in request
    return self.rest_client.post_request(url,
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/linebot/v3/messaging/rest.py", line 270, in post_request
    return self.request("POST", url,
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/linebot/v3/messaging/rest.py", line 156, in request
    r = self.pool_manager.request(
        ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/urllib3/_request_methods.py", line 143, in request
    return self.request_encode_body(
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/urllib3/_request_methods.py", line 278, in request_encode_body
    return self.urlopen(method, url, **extra_kw)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/urllib3/poolmanager.py", line 443, in urlopen
    response = conn.urlopen(method, u.request_uri, **kw)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/urllib3/connectionpool.py", line 789, in urlopen
    response = self._make_request(
               ^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/urllib3/connectionpool.py", line 536, in _make_request
    response = conn.getresponse()
               ^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/urllib3/connection.py", line 507, in getresponse
    httplib_response = super().getresponse()
                       ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/python/Python-3.11.10/lib/python3.11/http/client.py", line 1395, in getresponse
    response.begin()
  File "/opt/render/project/python/Python-3.11.10/lib/python3.11/http/client.py", line 325, in begin
    version, status, reason = self._read_status()
                              ^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/python/Python-3.11.10/lib/python3.11/http/client.py", line 286, in _read_status
    line = str(self.fp.readline(_MAXLINE + 1), "iso-8859-1")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/python/Python-3.11.10/lib/python3.11/socket.py", line 718, in readinto
    return self._sock.recv_into(b)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/python/Python-3.11.10/lib/python3.11/ssl.py", line 1314, in recv_into
    return self.read(nbytes, buffer)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/python/Python-3.11.10/lib/python3.11/ssl.py", line 1166, in read
    return self._sslobj.read(len, buffer)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/gunicorn/workers/base.py", line 204, in handle_abort
    sys.exit(1)
SystemExit: 1
[2025-07-28 05:21:05 +0000] [103] [ERROR] Worker (pid:617) was sent SIGKILL! Perhaps out of memory?

---

# Renderデプロイ環境でのWORKER TIMEOUTエラー解決策

## 1. エラー概要

- **現象:** Render.comの無料プランでデプロイしたGunicorn + Flaskアプリケーションが、一定時間アクセスがない状態からの初回リクエスト時に`WORKER TIMEOUT`エラーで失敗する。
- **原因:** Renderの無料プランでは、非アクティブな状態が続くとインスタンスがスリープする。次のリクエストが来た際にインスタンスが復帰（Wake-up）するが、その起動処理（モデルの読み込み、外部サービスへの接続など）に時間がかかり、Gunicornのデフォルトワーカータイムアウト（30秒）を超えてしまうため。

## 2. 解決策の方針

即時性と根本解決の観点から、以下の段階的な対策を提案します。

### Level 1: 緊急回避策（即時対応）

- **Gunicornのタイムアウト値を延長する:**
  - **目的:** インスタンスの復帰時間を許容し、タイムアウトエラーを回避する。
  - **方法:** Renderの起動コマンドに`--timeout`オプションを追加し、タイムアウトを60秒以上に設定する。
  - **コマンド例:** `gunicorn --bind 0.0.0.0:8000 app:app --timeout 120`

### Level 2: アプリケーションの改善（推奨）

- **非同期ワーカーを導入する:**
  - **目的:** ネットワークI/O（LINE APIへのリクエスト等）で処理がブロックされるのを防ぎ、ワーカーの効率を向上させる。
  - **方法:**
    1. `requirements.txt`に`gevent`を追加する。
    2. Gunicornの起動コマンドでワーカースラスを`gevent`に変更する (`-k gevent`)。
  - **コマンド例:** `gunicorn --bind 0.0.0.0:8000 app:app -k gevent --timeout 120`

- **Firebaseクライアントの初期化を効率化する:**
  - **目的:** リクエストごとに発生する可能性のある初期化処理のオーバーヘッドを削減する。
  - **方法:** Firebase Admin SDKの初期化 (`firebase_admin.initialize_app()`) が、アプリケーションの起動時に一度だけ実行されるようにコードを構成する。グローバルスコープで一度だけ呼び出すのが一般的。

### Level 3: 根本解決

- **Renderの有料プランを検討する:**
  - **目的:** インスタンスのスリープを完全に防ぎ、安定したサービス提供を実現する。
  - **方法:** Renderの有料プラン（Starterプラン以上）にアップグレードする。これにより、インスタンスは常にアクティブ状態に保たれる。

- **Voskモデルの読み込みを遅延させる（もし起動時に読み込んでいる場合）:**
  - **目的:** アプリケーションの起動時間を短縮する。
  - **方法:** 音声認識モデルの読み込みを、アプリケーション起動時ではなく、実際に音声メッセージが処理されるタイミングで一度だけ行うようにリファクタリングする。

## 3. 具体的な修正手順案

1.  **[修正]** `render.yaml`またはRenderダッシュボードの起動コマンドを修正し、`--timeout`オプションを追加する。
    ```yaml
    services:
      - type: web
        name: my-line-bot
        env: python
        buildCommand: "pip install -r requirements.txt"
        startCommand: "gunicorn --bind 0.0.0.0:8000 app:app --timeout 120"
    ```
2.  **[確認・修正]** `app.py`などを確認し、`firebase_admin.initialize_app()`がリクエスト処理関数の中ではなく、グローバルスコープで一度だけ呼び出されていることを確認する。
3.  **[修正]** （推奨）`requirements.txt`に`gevent`を追加し、起動コマンドで`-k gevent`を指定する。
4.  **[検討]** 上記対策でも問題が解決しない、あるいはより安定した運用を目指す場合は、Renderの有料プランへの移行を検討する。
