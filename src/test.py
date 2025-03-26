import tkinter as tk
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

data = [
    {"app": "Chrome", "start": "2025-03-26 08:30:00", "end": "2025-03-26 10:15:00"},
    {"app": "VS Code", "start": "2025-03-26 10:30:00", "end": "2025-03-26 12:00:00"},
    {"app": "Slack", "start": "2025-03-26 13:15:00", "end": "2025-03-26 14:45:00"},
    {"app": "Excel", "start": "2025-03-26 15:00:00", "end": "2025-03-26 16:30:00"},
    {"app": "Chrome", "start": "2025-03-26 17:00:00", "end": "2025-03-26 18:30:00"},
]

for d in data:
    d["start"] = datetime.strptime(d["start"], "%Y-%m-%d %H:%M:%S")
    d["end"] = datetime.strptime(d["end"], "%Y-%m-%d %H:%M:%S")

# アプリケーションごとの色を定義
colors = {
    "Chrome": "blue",
    "VS Code": "green",
    "Slack": "red",
    "Excel": "purple"
}

# グラフの設定
fig, ax = plt.subplots(figsize=(10, 2))
ax.set_xlim(0, 24)
ax.set_ylim(0, 1)
ax.set_yticks([])

# 時間を時間単位に変換する関数
def to_hours(dt):
    return dt.hour + dt.minute / 60

# データをプロット
for d in data:
    start = to_hours(d["start"])
    end = to_hours(d["end"])
    ax.fill_betweenx([0.4, 0.6], start, end, color=colors[d["app"]])

# 凡例を追加
patches = [mpatches.Patch(color=color, label=app) for app, color in colors.items()]
legend = ax.legend(handles=patches, loc='upper right')

# 凡例をクリックしたときのイベントハンドラ
def on_legend_click(event):
    # クリック位置の取得
    x, y = event.x, event.y
    # 凡例のバウンディングボックスを取得
    legend_box = legend.get_window_extent()
    # クリックが凡例内かどうかを確認
    if legend_box.contains(x, y):
        # クリックされた凡例アイテムを取得
        for legend_item in legend.get_lines():
            if legend_item.contains(event)[0]:
                # 色を変更
                new_color = "yellow" if legend_item.get_color() != "yellow" else "gray"
                legend_item.set_color(new_color)
                # グラフを再描画
                fig.canvas.draw()
                break

# イベントを登録
fig.canvas.mpl_connect('button_press_event', on_legend_click)

# X軸のラベルを設定
ax.set_xticks(range(0, 25, 1))
ax.set_xticklabels([f"{i:02d}" for i in range(0, 25, 1)])

# グラフを表示
plt.show()