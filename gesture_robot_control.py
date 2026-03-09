import mediapipe as mp
import cv2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time
import math
import socket

# -----------------------------
# UDP CONFIG
# -----------------------------
UDP_IP = "172.20.189.223"
UDP_PORT = 15000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# -----------------------------
# SPEED CONFIG
# -----------------------------
linear_speed = 0.2
angular_speed = 0.2

MIN_VAL = 0.1
MAX_VAL = 1.0

last_detection_time = time.time()
last_send_time = 0

# -----------------------------
# UI CONFIG
# -----------------------------
SLIDER_Y = 0.85
SLIDER_WIDTH = 0.3
HITBOX_H = 0.1

LIN_X_START = 0.1
LIN_X_END = LIN_X_START + SLIDER_WIDTH

ANG_X_START = 0.6
ANG_X_END = ANG_X_START + SLIDER_WIDTH

# -----------------------------
# MEDIAPIPE MODEL
# -----------------------------
base_options = python.BaseOptions(model_asset_path="hand_landmarker.task")

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    running_mode=vision.RunningMode.VIDEO
)

detector = vision.HandLandmarker.create_from_options(options)

# -----------------------------
# DIRECTION DETECTION
# -----------------------------
def get_direction(lm):

    wrist = lm[0]
    index_tip = lm[8]
    index_pip = lm[6]
    thumb_tip = lm[4]
    thumb_ip = lm[3]

    dx = index_tip.x - wrist.x
    dy = index_tip.y - wrist.y
    dx_thumb = thumb_tip.x - wrist.x

    dist = math.sqrt(dx*dx + dy*dy)

    if dist < 0.07:
        return "stop"

    dead = 0.15

    if dx > dead and index_tip.x > index_pip.x:
        return "right"

    if dx < -dead and index_tip.x < index_pip.x:
        return "left"

    if dy < -dead and index_tip.y < index_pip.y:
        return "forward"

    if dy > dead and index_tip.y > index_pip.y:
        return "backward"

    if dx_thumb > dead and thumb_tip.x > thumb_ip.x:
        return "rotate_right"

    if dx_thumb < -dead and thumb_tip.x < thumb_ip.x:
        return "rotate_left"

    return "stop"

# -----------------------------
# DRAW UI
# -----------------------------
def draw_ui(frame, direction, lin, ang, active_lin, active_ang):

    h, w, _ = frame.shape

    cv2.rectangle(frame, (5,5), (420,110), (40,40,40), -1)

    cv2.putText(frame,f"DIR: {direction.upper()}",
                (15,35),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

    cv2.putText(frame,f"LIN SPEED: {lin:.2f}",
                (15,65),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,0),2)

    cv2.putText(frame,f"ANG SPEED: {ang:.2f}",
                (15,95),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,255),2)

    def draw_bar(x_start,x_end,val,label,active):

        color = (0,255,0) if active else (120,120,120)

        s_px = int(x_start*w)
        e_px = int(x_end*w)
        y_px = int(SLIDER_Y*h)

        cv2.line(frame,(s_px,y_px),(e_px,y_px),color,3)

        ratio = (val-MIN_VAL)/(MAX_VAL-MIN_VAL)
        hx = int(s_px + ratio*(e_px-s_px))

        cv2.circle(frame,(hx,y_px),12,(0,255,255),-1)

        cv2.putText(frame,label,(s_px,y_px-20),
                    cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)

    draw_bar(LIN_X_START,LIN_X_END,lin,"LINEAR",active_lin)
    draw_bar(ANG_X_START,ANG_X_END,ang,"ANGULAR",active_ang)

# -----------------------------
# CAMERA
# -----------------------------
cap = cv2.VideoCapture(0)

timestamp = 0

while cap.isOpened():

    ret,frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame,1)

    h,w,_ = frame.shape

    rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    timestamp += 1

    res = detector.detect_for_video(mp_image,timestamp)

    direction = "stop"
    active_lin = False
    active_ang = False

    if res.hand_landmarks:

        last_detection_time = time.time()

        hand = res.hand_landmarks[0]

        direction = get_direction(hand)

        middle_tip = hand[12]

        in_y = abs(middle_tip.y - SLIDER_Y) < (HITBOX_H/2)

        # linear slider
        if in_y and LIN_X_START <= middle_tip.x <= LIN_X_END:

            active_lin = True

            t = (middle_tip.x - LIN_X_START)/(LIN_X_END-LIN_X_START)

            linear_speed = MIN_VAL + t*(MAX_VAL-MIN_VAL)

        # angular slider
        if in_y and ANG_X_START <= middle_tip.x <= ANG_X_END:

            active_ang = True

            t = (middle_tip.x - ANG_X_START)/(ANG_X_END-ANG_X_START)

            angular_speed = MIN_VAL + t*(MAX_VAL-MIN_VAL)

        cx = int(middle_tip.x*w)
        cy = int(middle_tip.y*h)

        cv2.circle(frame,(cx,cy),10,(0,255,0),2)

    # safety stop
    if time.time() - last_detection_time > 0.25:
        direction = "stop"

    # -----------------------------
    # VELOCITY
    # -----------------------------
    vx = 0
    vy = 0
    wz = 0

    if direction == "forward":
        vx = linear_speed

    elif direction == "backward":
        vx = -linear_speed

    elif direction == "left":
        vy = linear_speed

    elif direction == "right":
        vy = -linear_speed

    elif direction == "rotate_left":
        wz = angular_speed

    elif direction == "rotate_right":
        wz = -angular_speed

    # -----------------------------
    # UDP SEND (20Hz limit)
    # -----------------------------
    if time.time() - last_send_time > 0.05:

        msg = f"{vx:.2f} {vy:.2f} {wz:.2f}"

        sock.sendto(msg.encode(),(UDP_IP,UDP_PORT))

        last_send_time = time.time()

    # -----------------------------
    # UI
    # -----------------------------
    draw_ui(frame,direction,linear_speed,angular_speed,
            active_lin,active_ang)

    cv2.imshow("Gesture Robot Teleop",frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
sock.close()