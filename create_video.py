import os
import argparse
import replicate
import requests
import time
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# APIのモデル識別子
MODEL_ID = "bytedance/seedance-1-lite"


def create_video_from_prompt(prompt: str, output_path: str):
    """
    テキストプロンプトから動画を生成し、指定されたパスに保存する。

    Args:
        prompt (str): 動画生成のためのテキストプロンプト。
        output_path (str): 生成された動画を保存するファイルパス。
    """
    print(f"動画生成を開始します... プロンプト: {prompt}")

    try:
        # Replicate APIを呼び出して動画生成を開始
        output = replicate.run(
            MODEL_ID,
            input={"prompt": prompt, "aspect_ratio": "9:16"},
        )

        # APIの応答（ストリーム）を直接ファイルに書き込みます。
        print("動画データをファイルに書き込んでいます...")
        with open(output_path, "wb") as f:
            # outputがストリームオブジェクトの場合、read()で内容を読み取って書き込む
            content = output.read()
            f.write(content)

        print(f"動画が正常に保存されました: {output_path}")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        if "REPLICATE_API_TOKEN" not in os.environ:
            print("エラー: 環境変数 REPLICATE_API_TOKEN が設定されていません。")
            print(
                "ReplicateウェブサイトでAPIトークンを取得し、環境変数を設定してください。"
            )


def main():
    """
    コマンドライン引数を処理し、動画生成を開始する。
    """
    parser = argparse.ArgumentParser(
        description="テキストプロンプトから縦型動画を生成します。"
    )
    parser.add_argument("prompt", type=str, help="動画を説明するテキストプロンプト。")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=f"output_{int(time.time())}.mp4",
        help="出力ファイル名。デフォルトは 'output_[タイムスタンプ].mp4' です。",
    )

    args = parser.parse_args()

    create_video_from_prompt(args.prompt, args.output)


if __name__ == "__main__":
    main()
