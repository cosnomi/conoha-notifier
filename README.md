# conoha-notifier
ConoHaの請求情報をzaimとSlackに通知するAWS lambda function

# 機能
- ConoHaからAPI経由で当月分の請求情報を取得
- 請求情報をzaimに登録。(accountやcategoryも指定可能)
- 請求情報をSlackのWebhookに通知

# Installation
ReleasesにあるzipファイルをAWS lambdaにアップロード。  
適宜、環境変数を設定

# TODO
- 請求予定額が一定額を超えた段階で通知
- slash commandで現時点での請求予定額を表示
- インスタンスごとの請求情報を取得し、Slackに通知する
