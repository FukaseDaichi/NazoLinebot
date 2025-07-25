# libディレクトリ定義ファイル

`lib`ディレクトリには、LINE Botのゲームやメッセージ、ポストバックアクションを定義するためのJSONファイルが格納されています。

## `config.json`

このファイルは、Botが提供するゲームやモードの設定を定義します。

- **`games`**: ゲームやモードのリストを定義する配列です。
  - **`id`**: ゲームやモードの一意な識別子です。
  - **`path`**: 対応する`messages.json`へのパスです。
  - **`isGame`**: これがゲームであるかどうかを示すブール値です。
  - **`title`**: ゲームのタイトルです。
  - **`image`**: ゲームリストに表示される画像のURLです。
  - **`description`**: ゲームの説明です。

### 例:

```json
{
    "games": [
        {
            "id": "default",
            "path": "./lib/messages.json",
            "isGame": false,
            "title": null,
            "image": null,
            "description": null
        },
        {
            "id": "tutorial",
            "path": "./lib/tutorial/messages.json",
            "isGame": true,
            "title": "チュートリアル",
            "image": "https://developers-resource.landpress.line.me/fx/clip/clip10.jpg",
            "description": "チュートリアル脱出ゲーム。1分～"
        }
    ]
}
```

## `messages.json`

このファイルは、ユーザーのテキストメッセージに対するBotの応答を定義します。キーは正規表現であり、値は応答メッセージまたは実行するサービスクラスへのパスです。

- **キー**: ユーザーメッセージにマッチする正規表現。
- **値**:
  - **静的メッセージ**: `{user_name}`のようなプレースホルダーを含むことができる文字列または文字列の配列。
  - **動的応答**: `src.messages.messages_game_list`のように、応答を処理するPythonクラスへのパス。`||`で区切られた追加のパラメータを持つことができます。

### 例:

```json
{
  "一覧": "src.messages.messages_game_list",
  "こん.*": "{user_name}さんこんにちは",
  "おはよう": [
    "{user_name}さんおはようございます。",
    "いい朝ですね"
  ],
  "ランキング": "src.messages.messages_ranking||tutorial"
}
```

## `postbacks.json`

このファイルは、LINEのポストバックイベントに対するBotのアクションを定義します。キーはポストバックデータのクエリ文字列にマッチする正規表現で、値は応答メッセージまたは実行するサービスクラスへのパスです。

- **キー**: ポストバックデータにマッチする正規表現。
- **値**:
  - **静的メッセージ**: 文字列。
  - **動的応答**: `src.messages.messages_register_user`のように、アクションを処理するPythonクラスへのパス。

### 例:

```json
{
  "action=reject.*": "もう一度教えてください。",
  "action=register.*": "src.messages.messages_register_user",
  "action=changemode.*": "src.messages.messages_change_mode"
}
```

## サブディレクトリ

`first`や`tutorial`のようなサブディレクトリには、特定のゲームモードのための`messages.json`が含まれています。これらのファイルは、そのゲームがアクティブなときにのみ使用されます。
