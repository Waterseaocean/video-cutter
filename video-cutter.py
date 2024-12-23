import cv2
import numpy as np  #asを使うと"np"としてNumPyを利用する際に省略名を定義できる
from doesImgSeemDifferent import doesImgSeemDifferent

def display_frames(video_path: str):
    """
    動画をフレームごとに表示するデバッグ用関数。
    
    Args:
        video_path (str): 動画ファイルのパス。
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: 動画を読み込めませんでした。")
        return

    frame_count = 0
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            window_name = f"Frame {frame_count + 1}"
            cv2.imshow(window_name, frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            frame_count += 1
    finally:
        cap.release()
        cv2.destroyAllWindows()


def detect_slide_changes(video_path: str):
    """
    動画内のフレーム間の変化を`doesImgSeemDifferent`関数を用いて検出し、スライドが変化した場面を保存する。
    
    Args:
        video_path (str): 動画ファイルのパス
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: 動画を読み込めませんでした。")
        return

    frame_count = 0
    prev_frame = None
    slide_count = 0

    try:  #finallyを使うためにtryを使う
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if prev_frame is not None:
                # フレーム間の変化をdoesImgSeemDifferent関数で判定
                if doesImgSeemDifferent(prev_frame, frame):
                    slide_count += 1
                    slide_filename = f"slide_{slide_count}.jpg"  #f:f"文字列 {変数} その他の文字列", f-stringというもの
                    cv2.imwrite(slide_filename, frame)
                    print(f"スライドを保存しました: {slide_filename}")

            prev_frame = frame  # 前フレームを更新
            frame_count += 1

            # 現在のフレームを表示（デバッグ用）
            cv2.imshow("Current Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):  #waitkey:画像を表示するウィンドウからの、キーボード入力を待ち受ける関数,'q'キーで終了
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

    print(f"保存されたスライド数: {slide_count}")


# 動画パスの指定
video_path = r"c:\Users\yamada\OneDrive\ドキュメント\test1.mp4"

# 動画を確認する場合（デバッグ用）
# display_frames(video_path)

# スライド変化を検知して保存
detect_slide_changes(video_path)