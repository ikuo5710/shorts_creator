import argparse
import time
import os
import re
from core.create_video import create_video_from_prompt
from core.add_audio import add_audio_to_video
from core.get_asmr_idea import get_asmr_idea

def sanitize_filename(filename):
    """
    ファイル名として不適切な文字をアンダースコアに置換する。
    """
    return re.sub(r'[\/*?:"<>|]', "_", filename)

def main():
    """
    ASMR動画のアイデアから、動画生成、音声追加までのパイプラインを実行する。
    """
    parser = argparse.ArgumentParser(
        description="ASMR動画のアイデアから、音声付きの動画を生成します。"
    )
    parser.add_argument(
        "prompt",
        type=str,
        help="ASMR動画のアイデア（例: 「雨の日の図書館」）。"
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        default=".",
        help="最終的な出力ファイルを保存するディレクトリ。デフォルトはカレントディレクトリです。"
    )

    args = parser.parse_args()

    # 1. ASMRのアイデアを取得
    print("--- ステップ1: ASMRアイデアの生成 ---")
    asmr_idea = get_asmr_idea(args.prompt)

    if not asmr_idea:
        print("エラー: ASMRアイデアの生成に失敗しました。処理を中断します。")
        return

    # 2. JSONから情報を抽出
    title = asmr_idea.get("title")
    video_prompt = asmr_idea.get("video_prompt")
    audio_prompt = asmr_idea.get("audio_prompt")

    if not all([title, video_prompt, audio_prompt]):
        print("エラー: APIからのレスポンスに必要な情報（title, video_prompt, audio_prompt）が含まれていません。")
        return
    
    print(f"  - タイトル: {title}")
    print(f"  - 動画プロンプト: {video_prompt}")
    print(f"  - 音声プロンプト: {audio_prompt}")

    # 3. ファイルパスを準備
    sanitized_title = sanitize_filename(title)
    final_output_path = os.path.join(args.output_dir, f"{sanitized_title}.mp4")
    video_only_path = f"temp_video_{int(time.time())}.mp4"

    # 4. 動画を生成する
    print("\n--- ステップ2: 動画生成 ---")
    create_video_from_prompt(video_prompt, video_only_path)

    if not os.path.exists(video_only_path):
        print(f"エラー: 動画ファイル '{video_only_path}' の生成に失敗しました。処理を中断します。")
        return

    # 5. 生成された動画に音声を追加する
    print("\n--- ステップ3: 音声追加 ---")
    add_audio_to_video(video_only_path, audio_prompt, final_output_path)

    # 6. 中間ファイルを削除
    print(f"\n--- クリーンアップ ---")
    try:
        os.remove(video_only_path)
        print(f"中間ファイル '{video_only_path}' を削除しました。")
    except OSError as e:
        print(f"エラー: 中間ファイル '{video_only_path}' の削除に失敗しました: {e}")

    print(f"\n処理が完了しました。最終的な動画は '{final_output_path}' に保存されています。")


if __name__ == "__main__":
    main()
