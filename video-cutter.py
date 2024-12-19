import cv2

def display_frames(video_path: str):
    # 動画の読み込み
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: 動画を読み込めませんでした。")
        return
    
    frame_count = 0
    # フレームの取得と表示
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:  # フレームが取得できない場合は終了
            break
        
        # フレームをウィンドウに表示
        window_name = f"Frame {frame_count + 1}"
        cv2.imshow(window_name, frame)

        # 'q'キーで終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1

    # リソース解放
    cap.release()
    cv2.destroyAllWindows()

video_path = r"c:\Users\yamada\OneDrive\ドキュメント\test1.mp4"  # 動画のパス
display_frames(video_path)