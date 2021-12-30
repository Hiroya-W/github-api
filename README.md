# GitHub API

GitHub API V3/V4をPythonから利用するためのライブラリ

## インストール

PyPIには公開していないので、GitHubリポジトリからインストールすることになる。
`pip`を使う場合:

```bash
pip install git+https://github.com/Hiroya-W/github-api
```

`poetry`を使う場合:

```bash
poetry add git+https://github.com/Hiroya-W/github-api#main
```

## 環境変数にPersonal Access Tokenをセットする

GitHub APIを利用する際に、Personal Access Tokenが必要になる。
実行時、環境変数として、`GITHUB_TOKEN`にセットしておく。

例えば、macOSでは、Keychain acessが利用でき、`GitHub-PAT`という名前の`Hiroya-W`ユーザからパスワードを取得できる。
fishでは、環境変数のセットには`set -x`を用いれば良い。

```fish
set -x GITHUB_TOKEN (security find-generic-password -a Hiroya-W -s GitHub-PAT -w)
```
