"""
Register a Blink-PIN for a user.

This script captures a 4-blink PIN (quick=0, long=1) using the same
blink detection logic as the authentication script, then stores the
hashed PIN under the provided username in users.json.

Requirements:
- Python 3.10-3.12
- OpenCV (opencv-python)
- MediaPipe
- NumPy
"""

from __future__ import annotations

import time
import cv2
import numpy as np

from blink_utils import (
    BLINK_TO_DIGIT,
    EAR_THRESHOLD,
    BLINK_DURATION_THRESHOLD,
    MIN_BLINK_INTERVAL,
    CONSEC_FRAMES,
    MAX_BLINKS,
    LEFT_EYE_LANDMARKS,
    RIGHT_EYE_LANDMARKS,
    calculate_ear,
    get_landmark_coords,
    create_face_mesh,
    set_user_pin,
)


def main() -> None:
    print("[INFO] Blink-PIN Registration")
    print("[INFO] Quick blink = 0, Long blink = 1")
    print("[INFO] Press 'q' to quit, 'r' to reset")

    username = input("Enter a username to register: ").strip()
    if not username:
        print("[ERROR] Username cannot be empty.")
        return

    face_mesh = create_face_mesh()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Cannot access camera")
        face_mesh.close()
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    blink_sequence = []
    frame_counter = 0
    ear_history = []
    is_blinking = False
    blink_start_time = 0.0
    last_blink_time = 0.0
    consec_blinks = 0

    print("[INFO] Camera initialized. Start blinking to set your PIN...")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[ERROR] Failed to read frame")
                break

            frame_counter += 1
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)
            current_time = time.time()

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    left_eye = get_landmark_coords(face_landmarks, LEFT_EYE_LANDMARKS, w, h)
                    right_eye = get_landmark_coords(face_landmarks, RIGHT_EYE_LANDMARKS, w, h)

                    left_ear = calculate_ear(left_eye)
                    right_ear = calculate_ear(right_eye)
                    avg_ear = (left_ear + right_ear) / 2.0

                    ear_history.append(avg_ear)
                    if len(ear_history) > 5:
                        ear_history.pop(0)

                    smooth_ear = float(np.mean(ear_history)) if ear_history else avg_ear

                    # Draw landmarks
                    for point in left_eye + right_eye:
                        cv2.circle(frame, tuple(point), 2, (0, 255, 0), -1)

                    left_contour = np.array(left_eye, np.int32)
                    right_contour = np.array(right_eye, np.int32)
                    cv2.polylines(frame, [left_contour], True, (255, 0, 0), 1)
                    cv2.polylines(frame, [right_contour], True, (255, 0, 0), 1)

                    # Blink detection
                    if smooth_ear < EAR_THRESHOLD:
                        consec_blinks += 1
                        if not is_blinking and consec_blinks >= CONSEC_FRAMES:
                            if (current_time - last_blink_time) > MIN_BLINK_INTERVAL:
                                is_blinking = True
                                blink_start_time = current_time
                                print(f"[BLINK START] EAR: {smooth_ear:.3f}")
                                cv2.putText(
                                    frame,
                                    "BLINK DETECTED!",
                                    (50, 100),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    1,
                                    (0, 0, 255),
                                    2,
                                )
                    else:
                        consec_blinks = 0
                        if is_blinking:
                            blink_duration = current_time - blink_start_time

                            if len(blink_sequence) < MAX_BLINKS:
                                if blink_duration < BLINK_DURATION_THRESHOLD:
                                    blink_type = "quick"
                                    digit = "0"
                                    color = (0, 255, 0)
                                else:
                                    blink_type = "long"
                                    digit = "1"
                                    color = (0, 0, 255)

                                blink_sequence.append(blink_type)
                                last_blink_time = current_time
                                print(
                                    f"[DETECTED] {blink_type.upper()} blink ({blink_duration:.2f}s) -> {digit}"
                                )

                                cv2.putText(
                                    frame,
                                    f"{blink_type.upper()} -> {digit}",
                                    (50, 150),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    1,
                                    color,
                                    2,
                                )

                            is_blinking = False

                    # HUD
                    cv2.putText(
                        frame,
                        f"EAR: {smooth_ear:.3f}",
                        (w - 150, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 255),
                        2,
                    )
                    cv2.putText(
                        frame,
                        f"Threshold: {EAR_THRESHOLD}",
                        (w - 150, 60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 255),
                        2,
                    )

                    if frame_counter % 60 == 0:
                        print(f"[DEBUG] Current EAR: {smooth_ear:.3f} (Threshold: {EAR_THRESHOLD})")
            else:
                cv2.putText(
                    frame,
                    "NO FACE DETECTED",
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                )

            progress_text = f"PIN: {len(blink_sequence)}/{MAX_BLINKS}"
            cv2.putText(
                frame,
                progress_text,
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 0),
                2,
            )

            if blink_sequence:
                sequence = "".join([BLINK_TO_DIGIT[b] for b in blink_sequence])
                cv2.putText(
                    frame,
                    f"Sequence: {sequence}",
                    (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 0),
                    2,
                )

            cv2.putText(
                frame,
                "Quick=0, Long=1 | Q=Quit, R=Reset",
                (10, h - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 255),
                1,
            )

            cv2.imshow("Register Blink-PIN", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                print("[INFO] Quit requested. Registration aborted.")
                break
            elif key == ord("r"):
                print("[INFO] Resetting sequence...")
                blink_sequence = []
                is_blinking = False
                consec_blinks = 0

            if len(blink_sequence) >= MAX_BLINKS:
                print("[INFO] PIN capture complete!")
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        face_mesh.close()

    # Save if complete
    if len(blink_sequence) >= MAX_BLINKS:
        pin_str = "".join([BLINK_TO_DIGIT[b] for b in blink_sequence])
        print(f"\nBlink sequence: {blink_sequence}")
        print(f"PIN: {pin_str}")
        set_user_pin(username, pin_str)
        print("[SUCCESS] PIN registered for user:", username)
    else:
        print("[INFO] Registration incomplete; nothing saved.")


if __name__ == "__main__":
    main()
