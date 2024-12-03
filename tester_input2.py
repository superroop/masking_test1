import streamlit as st
import streamlit.components.v1 as components

# テキストファイルをアップロードして読み込む
uploaded_file = st.file_uploader("テキストファイルをアップロード", type=["txt"])

if uploaded_file is not None:
    # アップロードされたファイルの内容を読み込む
    original_text = uploaded_file.read().decode("shift_jis")

    # 元のテキストを表示
    st.write("元のテキスト:")
    st.write(original_text)

    # 強調された説明文を追加
    st.markdown("""
    <div style="border: 2px solid #007BFF; padding: 10px; margin: 10px 0; background-color: #f9f9f9; border-radius: 5px;">
        <h4 style="color: #007BFF;">マスキング処理について</h4>
        <ul>
            <li>以下のテキスト部分を確認してください。</li>
            <li>必要な箇所を選択し、ボタンをクリックすることで指定された記号に変換できます。</li>
            <li>変換後の内容をダウンロードすることも可能です。</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # JavaScriptを使ってテキストを選択し、変換するコンポーネントを埋め込む
    html_code = f"""
    <style>
        /* ボタンデザインのスタイル */
        button {{
            display: inline-block;
            padding: 10px 20px;
            margin: 10px 0;
            font-size: 16px;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}

        .btn-blue {{ background-color: #007BFF; color: #fff; }}
        .btn-green {{ background-color: #28a745; color: #fff; }}
        .btn-red {{ background-color: #dc3545; color: #fff; }}
        .btn-yellow {{ background-color: #ffc107; color: #000; }}
        .btn-purple {{ background-color: #6f42c1; color: #fff; }}
        .btn-orange {{ background-color: #fd7e14; color: #fff; }}
    </style>

    <div id="text-container" style="white-space: pre-wrap;">
        {original_text}
    </div>
    <button class="btn-blue" onclick="convertToSymbol('■')">選択した部分が、個人に関する非開示情報（5条1号）に該当（「■」に変換）</button><br>
    <button class="btn-green" onclick="convertToSymbol('□')">選択した部分が、法人等に関する非開示情報（5条2号）に該当（「□」に変換）</button><br>
    <button class="btn-red" onclick="convertToSymbol('▲')">選択した部分が、国の安全等に関する非開示情報（5条3号）に該当（「▲」に変換）</button><br>
    <button class="btn-yellow" onclick="convertToSymbol('▽')">選択した部分が、公共の安全等に関する非開示情報（5条4号）に該当（「▽」に変換）</button><br>
    <button class="btn-purple" onclick="convertToSymbol('●')">選択した部分が、審議・検討に関する非開示情報（5条5号）に該当（「●」に変換）</button><br>
    <button class="btn-orange" onclick="convertToSymbol('○')">選択した部分が、事務又は事業に関する非開示情報（5条6号）に該当（「○」に変換）</button><br>
    <button onclick="downloadText()">変換後のテキストをダウンロード</button>

    <script>
    let convertedText = "";  // グローバル変数として変換後のテキストを格納

    function convertToSymbol(symbol) {{
        var container = document.getElementById("text-container");
        var selection = window.getSelection();

        if (selection.rangeCount > 0) {{
            var range = selection.getRangeAt(0); // 選択範囲を取得
            var selectedText = range.toString();

            if (selectedText) {{
                var newText = container.innerText; // 元のテキストを取得
                var startOffset = newText.indexOf(selectedText, range.startOffset);
                var endOffset = startOffset + selectedText.length;

                // テキストを配列として扱い、選択部分を置き換え
                var textArray = Array.from(newText);
                for (var i = startOffset; i < endOffset; i++) {{
                    textArray[i] = symbol;
                }}

                var updatedText = textArray.join("");
                container.innerText = updatedText; // テキストを更新
                convertedText = updatedText;      // グローバル変数に保持
            }}
        }}
    }}

    function downloadText() {{
        // ファイル名を設定
        var fileName = "{uploaded_file.name.replace('.txt', '')}_masked.txt";
        
        // convertedText のトリム（前後の空白や改行を削除）
        var cleanText = convertedText.trim();
        
        var blob = new Blob([cleanText], {{ type: 'text/plain' }});
        var link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = fileName;
        link.click();
    }}
    </script>
    """

    # JavaScriptを含むHTMLをStreamlitに表示
    components.html(html_code, height=2000)