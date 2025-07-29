import tkinter as tk
import threading
import keyboard
import tkinter.messagebox as msgbox
import time
from pygetwindow import getWindowsWithTitle
from auto_hunter import start_auto_hunt
from cheat_controller import run_cheat_commands
import os

def show_countdown_alert():
    msgbox.showinfo("알림", "10초 후 사냥이 종료됩니다.")

def handle_cheat_all():
    windows = getWindowsWithTitle("게임 이름")
    if not windows:
        print("게임 창을 찾을 수 없습니다.")
        return
    for i, win in enumerate(windows):
        try:
            print(f"{i+1}번째 창 실행: {win.title}")
            win.activate()
            time.sleep(1)
            
            run_cheat_commands(item_ids, item_qtys, stat_entries, cheat_group_entry.get().strip())
        except Exception as e:
            print(f"창 활성화 실패 : {e}")

def handle_cheat_current():
    run_cheat_commands(item_ids, item_qtys, stat_entries, cheat_group_entry.get().strip())

def quit_program():
    keyboard.wait("f1")
    print("F1 입력 감지됨. 즉시 종료합니다.")
    os._exit(0)

# 전역 변수들
root = tk.Tk()
item_ids = []
item_qtys = []
stat_entries = {}
cheat_group_entry = None
hunt_time_entry = None
server_entry = None

threading.Thread(target=quit_program, daemon=True).start()

def run_gui():
    global root, item_ids, item_qtys, stat_entries, cheat_group_entry, hunt_time_entry, server_entry

    root.title("밸런스 테스트 자동화 프로그램")
    root.geometry("480x500")

    tk.Label(root, text="밸런스 테스트 자동화 프로그램", font=("맑은 고딕", 14, "bold")).pack(pady=10)

    frame_top = tk.Frame(root)
    frame_top.pack(pady=10)

    frame_item = tk.Frame(frame_top)
    frame_item.grid(row=0, column=0, padx=20)
    tk.Label(frame_item, text="아이템 지급", font=("맑은 고딕", 10, "bold")).grid(row=0, column=0, columnspan=3, pady=5)
    for i in range(6):
        tk.Label(frame_item, text=f"아이템 ID").grid(row=i+1, column=0, padx=5, pady=2)
        id_entry = tk.Entry(frame_item, width=10)
        id_entry.grid(row=i+1, column=1, padx=2)
        qty_entry = tk.Entry(frame_item, width=5)
        qty_entry.grid(row=i+1, column=2, padx=2)
        item_ids.append(id_entry)
        item_qtys.append(qty_entry)

    frame_stat = tk.Frame(frame_top)
    frame_stat.grid(row=0, column=1, padx=20)
    tk.Label(frame_stat, text="추가 스탯 입력창", font=("맑은 고딕", 10, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
    stats = ["공격력", "방어력", "명중", "공격 속도", "아이템 획득 확률", "무게"]
    for i, stat in enumerate(stats):
        tk.Label(frame_stat, text=stat).grid(row=i+1, column=0, padx=(0,10), pady=2)
        entry = tk.Entry(frame_stat, width=10)
        entry.grid(row=i+1, column=1, padx=(0,10))
        stat_entries[stat] = entry

    frame_cheat_group = tk.Frame(root)
    frame_cheat_group.pack(pady=10)
    tk.Label(frame_cheat_group, text="명령어 그룹명").grid(row=0, column=0, padx=5)
    cheat_group_entry = tk.Entry(frame_cheat_group, width=20)
    cheat_group_entry.grid(row=0, column=1)

    frame_buttons = tk.Frame(root)
    frame_buttons.pack(pady=10)
    tk.Button(frame_buttons, text="모든 창에 치트 적용", width=20, height=2, command=handle_cheat_all).grid(row=0, column=0, padx=(0, 30))
    tk.Button(frame_buttons, text="현재 창에 치트 적용", width=20, height=2, command=handle_cheat_current).grid(row=0, column=1)

    frame_bottom = tk.Frame(root)
    frame_bottom.pack(pady=10, anchor="center")
    tk.Label(frame_bottom, text="서버명").grid(row=0, column=0, padx=5)
    server_entry = tk.Entry(frame_bottom, width=10)
    server_entry.grid(row=0, column=1, padx=5)
    tk.Label(frame_bottom, text="사냥 시간 (분)").grid(row=0, column=2, padx=5, pady=2)
    hunt_time_entry = tk.Entry(frame_bottom, width=10)
    hunt_time_entry.grid(row=0, column=3, padx=5)

    tk.Button(root, text="사냥 시작 버튼", width=40, height=2, command=lambda: start_auto_hunt(hunt_time_entry, server_entry)).pack(pady=15)

    root.mainloop()
