# repository mining

リポジトリマイニングする時に用意したスクリプト集

## 環境変数にPersonal Access Tokenをセットする

GitHub APIを利用する際に、Personal Access Tokenが必要になる。
実行時、環境変数として、`GITHUB_TOKEN`にセットしておく。

例えば、macOSでは、Keychain acessが利用でき、`GitHub-PAT`という名前の`Hiroya-W`ユーザからパスワードを取得できる。
fisででは、環境変数のセットには`set -x`を用いれば良い。

```fish
set -x GITHUB_TOKEN (security find-generic-password -a Hiroya-W -s GitHub-PAT -w)
```
