[**ドキュメント**](https://github.com/Byaidu/PDFMathTranslate) > **API 詳細** _(現在のページ)_

<h2 id="toc">目次</h2>
本プロジェクトは Redis を利用する 2 種類の API を提供しています。

- [Python からの関数呼び出し](#api-python)
- [HTTP プロトコル](#api-http)

---

<h2 id="api-python">Python</h2>

`pdf2zh` は Python モジュールとしてインストールされるため、任意のスクリプトから呼び出せるメソッドを提供しています。

たとえば、Google 翻訳を使って英語の PDF を中国語に変換する場合は次のように記述します。

```python
from pdf2zh import translate, translate_stream

params = {
    "lang_in": "en",
    "lang_out": "zh",
    "service": "google",
    "thread": 4,
}
```

ファイルを渡して翻訳する:

```python
(file_mono, file_dual) = translate(files=["example.pdf"], **params)[0]
```

ストリームを渡して翻訳する:

```python
with open("example.pdf", "rb") as f:
    (stream_mono, stream_dual) = translate_stream(stream=f.read(), **params)
```

[⬆️ トップへ戻る](#toc)

---

<h2 id="api-http">HTTP</h2>

より柔軟に連携したい場合は、HTTP プロトコルを通じて通信できます。以下の手順を実行してください。

1. バックエンドをインストールして起動する

   ```bash
   pip install pdf2zh[backend]
   pdf2zh --flask
   pdf2zh --celery worker
   ```

2. HTTP 経由で操作する

   - 翻訳タスクを登録

     ```bash
     curl http://localhost:11008/v1/translate -F "file=@example.pdf" -F "data={\"lang_in\":\"en\",\"lang_out\":\"zh\",\"service\":\"google\",\"thread\":4}"
     {"id":"d9894125-2f4e-45ea-9d93-1a9068d2045a"}
     ```

   - 進捗を確認

     ```bash
     curl http://localhost:11008/v1/translate/d9894125-2f4e-45ea-9d93-1a9068d2045a
     {"info":{"n":13,"total":506},"state":"PROGRESS"}
     ```

   - 完了後の状態を取得

     ```bash
     curl http://localhost:11008/v1/translate/d9894125-2f4e-45ea-9d93-1a9068d2045a
     {"state":"SUCCESS"}
     ```

   - 単言語版 PDF を保存

     ```bash
     curl http://localhost:11008/v1/translate/d9894125-2f4e-45ea-9d93-1a9068d2045a/mono --output example-mono.pdf
     ```

   - 二言語版 PDF を保存

     ```bash
     curl http://localhost:11008/v1/translate/d9894125-2f4e-45ea-9d93-1a9068d2045a/dual --output example-dual.pdf
     ```

   - 実行中のタスクを中断して削除

     ```bash
     curl http://localhost:11008/v1/translate/d9894125-2f4e-45ea-9d93-1a9068d2045a -X DELETE
     ```

[⬆️ トップへ戻る](#toc)

---
