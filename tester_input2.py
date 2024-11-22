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
            <li>必要な箇所を選択し、ボタンをクリックすることで「■」に変換できます。</li>
            <li>変換後の内容をダウンロードすることも可能です。</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # JavaScriptを使ってテキストを選択し、変換するコンポーネントを埋め込む
    html_code = f"""
    <div id="text-container" style="white-space: pre-wrap;">
        {original_text}
    </div>
    <button onclick="convertToBox()">選択した部分を「■」に変換</button>
    <button onclick="downloadText()">変換後のテキストをダウンロード</button>

    <script>
    let convertedText = "";  // グローバル変数として変換後のテキストを格納

    function convertToBox() {{
        var container = document.getElementById("text-container");
        var selectedText = window.getSelection().toString();

        if (selectedText) {{
            var newText = container.innerText.trim();  // innerTextを使い、trim()で前後の空白を除去

            // 変換部分だけを「■」に置き換え
            var convertedSelectedText = selectedText.replace(/./g, "■");
            newText = newText.replace(selectedText, convertedSelectedText);

            container.innerText = newText;  // innerTextで変換後のテキストを更新

            // 変換後のテキストを保持
            convertedText = newText;  // innerTextをそのまま保持して、改行やインデントを除去
        }}
    }}

    function downloadText() {{
        // ダウンロード時のファイル名に元のファイル名を使い、_maskedを追加
        var fileName = "{uploaded_file.name.replace('.txt', '')}_masked.txt";

        // 変換後のテキストをダウンロード
        var blob = new Blob([convertedText], {{ type: 'text/plain' }});
        var link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = fileName;  // ファイル名を変更してダウンロード
        link.click();
    }}
    </script>
    """

    # JavaScriptを含むHTMLをStreamlitに表示
    components.html(html_code, height=300)
