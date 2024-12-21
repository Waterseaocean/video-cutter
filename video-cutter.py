import cv2
import numpy as np  #asを使うと"np"としてNumPyを利用する際に省略名を定義できる

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


def detect_slide_changes(video_path: str, diff_threshold: int = 50):
    """
    動画内のフレーム間の差分を演算し、スライドが変化した場面を保存する。
    
    Args:
        video_path (str): 動画ファイルのパス
        diff_threshold (int): 差分の平均値がこの閾値を超えた場合にスライド変化を検出。
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: 動画を読み込めませんでした。")
        return

    frame_count = 0
    prev_frame = None
    slide_count = 0

    try:  #最後に行う動作を定義するためにtryを使う
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

            if prev_frame is not None:
                frame_diff = cv2.absdiff(prev_frame, gray_frame)  #avsdi画素ごとの差異を計算するための関数
                diff_mean = np.mean(frame_diff)

                if diff_mean > diff_threshold:
                    slide_count += 1
                    slide_filename = f"slide_{slide_count}.jpg"
                    cv2.imwrite(slide_filename, frame)
                    print(f"スライドを保存しました: {slide_filename}")

            prev_frame = gray_frame
            frame_count += 1

            cv2.imshow("Current Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
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
detect_slide_changes(video_path, diff_threshold=50)
