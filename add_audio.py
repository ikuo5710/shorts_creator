import os
import argparse
import replicate
import requests
import time
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# Replicate上のMMAudioモデルの識別子
MODEL_ID = (
    "zsxkib/mmaudio:62871fb59889b2d7c13777f08deb3b36bdff88f7e1d53a50ad7694548a41b484"
)


def add_audio_to_video(video_path: str, prompt: str, output_path: str):
    """
    ローカルの動画ファイルに、テキストプロンプトに基づいて音声を生成し追加する。

    Args:
        video_path (str): 入力動画ファイルのパス。
        prompt (str): 生成する音声の説明（プロンプト）。
        output_path (str): 音声付き動画を保存するファイルパス。
    """
    if not os.path.exists(video_path):
        print(f"エラー: 指定された動画ファイルが見つかりません: {video_path}")
        return

    print(f"動画に音声を追加します...")
    print(f"  - 入力動画: {video_path}")
    print(f"  - 音声プロンプト: {prompt}")

    try:
        # ローカルの動画ファイルをバイナリモードで開く
        with open(video_path, "rb") as video_file:
            # Replicate APIを呼び出し、動画ファイルとプロンプトを渡す
            # ライブラリが自動的にファイルをアップロードしてくれます
            output_url = replicate.run(
                MODEL_ID,
                input={
                    "video": video_file,
                    "prompt": prompt,
                },
            )

        # Replicateはファイルライクオブジェクトを返すので、直接内容を読み取って書き込む
        print("音声付き動画をファイルに書き込んでいます...")
        with open(output_path, "wb") as f:
            # outputがストリームオブジェクトの場合、read()で内容を読み取って書き込む
            content = output_url.read()
            f.write(content)

        print(f"動画が正常に保存されました: {output_path}")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        if "REPLICATE_API_TOKEN" not in os.environ:
            print("エラー: 環境変数 REPLICATE_API_TOKEN が設定されていません。")
            print(
                "ReplicateウェブサイトでAPIトークンを取得し、.envファイルに設定してください。"
            )


def main():
    """
    コマンドライン引数を処理し、音声追加処理を開始する。
    """
    parser = argparse.ArgumentParser(
        description="ローカルの動画ファイルにAIで生成した音声を追加します。"
    )
    parser.add_argument("video_path", type=str, help="入力動画ファイルのパス。")
    parser.add_argument(
        "prompt",
        type=str,
        help="生成する音声の説明（例: 'A dramatic cinematic score'）。",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=f"video_with_audio_{int(time.time())}.mp4",
        help="出力ファイル名。デフォルトは 'video_with_audio_[タイムスタンプ].mp4' です。",
    )

    args = parser.parse_args()

    add_audio_to_video(args.video_path, args.prompt, args.output)


if __name__ == "__main__":
    main()
