import cv2
import numpy as np  #asを使うと"np"としてNumPyを利用する際に省略名を定義できる
from doesImgSeemDifferent import doesImgSeemDifferent
from display_frame import display_frames  # 動画を確認する場合（デバッグ用）


def select_roi(video_path: str):
    """
    動画の最初のフレームからROI (Region of Interest) を選択する。
    
    Args:
        video_path (str): 動画ファイルのパス。
    
    Returns:
        tuple: ROIの座標とサイズ (x, y, w, h) を返す。
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: 動画を読み込めませんでした。")
        return None

    ret, frame = cap.read()
    if not ret:  #ret:格納できたかどうかTrue or False
        print("Error: 動画の最初のフレームを取得できませんでした。")
        cap.release()
        return None

    # ROIを選択 (ユーザーがマウス操作で選択)
    roi = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select ROI")
    cap.release()

    if roi == (0, 0, 0, 0):
        print("Error: ROIが選択されませんでした。")
        return None
    return roi


def detect_slide_changes(video_path: str):
    """
    動画内のフレーム間の変化を`doesImgSeemDifferent`関数を用いて検出し、
    指定範囲 (ROI) 内で画面が変化した場面を保存する。
    
    Args:
        video_path (str): 動画ファイルのパス。
    """
    # ROIを選択
    roi = select_roi(video_path)
    if roi is None:
        print("Error: ROIが無効です。処理を中止します。")
        return
    x, y, w, h = roi

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: 動画を読み込めませんでした。")
        return

    frame_count = 0
    prev_frame = None
    slide_count = 0

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # ROI領域を切り取り
            cropped_frame = frame[y:y+h, x:x+w]

            if prev_frame is not None:
                # フレーム間の変化をdoesImgSeemDifferent関数で判定
                if doesImgSeemDifferent(prev_frame, cropped_frame):
                    slide_count += 1
                    slide_filename = f"slide_{slide_count}.jpg"  # f-string
                    cv2.imwrite(slide_filename, frame)  # 全体フレームを保存
                    print(f"スライドを保存しました: {slide_filename}")

            prev_frame = cropped_frame  # 前フレームを更新
            frame_count += 1

            # 現在のフレームを表示（デバッグ用）
            cv2.imshow("Current Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

    print(f"保存されたスライド数: {slide_count}")


# 動画パスの指定
video_path = r"c:\Users\yamada\OneDrive\ドキュメント\test1.mp4"

# スライド変化を検知して保存
detect_slide_changes(video_path)

# display_frames(video_path)