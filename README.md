# NazoLinebot

## 環境構築
-'uv venv'
- `uv pip install -r requirements.txt`

## FlexMessageの作成方法
[シミュレーターで確認する](https://developers.line.biz/flex-simulator/?status=success)

## Annaconda

1. 仮想環境の新規作成
   1. `conda create -n nazolinebot python=3.11`
2. 仮想環境の切り替え
   1. `conda activate nazolinebot`


## Redis

1. インストール
   1. `choco install redis-64`
2. 起動
   1. `Start-Service -Name "Redis"`
3. 停止
   1. `Stop-Service -Name "Redis"`

## freezeコマンド
`uv pip freeze > requirements.txt`