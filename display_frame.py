import cv2

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