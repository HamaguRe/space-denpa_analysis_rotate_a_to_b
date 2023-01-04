# グラフ作成

import csv
import matplotlib.pyplot as plt
import numpy as np

angles = []  # ベクトル間の角度
orig_q = [[], [], [], []]
q_old = [[], [], [], []]
q_new = [[], [], [], []]
b_true = [[], [], []]
b_old = [[], [], []]
b_new = [[], [], []]
b_error_old = [[], [], []]
b_error_new = [[], [], []]

# CSVからデータを読み出して配列に追加
with open('./result.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        nums = [float(v) for v in row]
        angles.append(nums[0])
        for i in range(4):
            orig_q[i].append(nums[i + 1])
            q_old[i].append(nums[i + 5])
            q_new[i].append(nums[i + 9])
        
        for i in range(3):
            b_true[i].append(nums[i + 13])
            b_old[i].append(nums[i + 16])
            b_new[i].append(nums[i + 19])
            b_error_old[i].append(nums[i + 22])
            b_error_new[i].append(nums[i + 25])


# --- 描画 --- #
# 四元数同士の比較
fig1 = plt.figure(figsize = (10, 9))  # 横, 縦
ax1 = fig1.add_subplot(411)
ax1.set_title('Quaternion Comparison', fontsize=20)
ax1.step(angles, orig_q[0], label="orig")
ax1.step(angles, q_old[0], label="conventional")
ax1.step(angles, q_new[0], label="new")
ax1.set_xlim(angles[0], angles[-1])
ax1.tick_params(labelsize=13)  # 軸目盛の大きさ
ax1.legend(fontsize=15, loc="upper right")
ax1.set_ylabel('q0', fontsize=15)

ax2 = fig1.add_subplot(412)
ax2.step(angles, orig_q[1], label="orig")
ax2.step(angles, q_old[1], label="conventional")
ax2.step(angles, q_new[1], label="new")
ax2.set_xlim(angles[0], angles[-1])
ax2.tick_params(labelsize=13)
ax2.set_ylabel('q1', fontsize=15)

ax3 = fig1.add_subplot(413)
ax3.step(angles, orig_q[2], label="orig")
ax3.step(angles, q_old[2], label="conventional")
ax3.step(angles, q_new[2], label="new")
ax3.set_xlim(angles[0], angles[-1])
ax3.tick_params(labelsize=13)
ax3.set_ylabel('q2', fontsize=15)

ax4 = fig1.add_subplot(414)
ax4.step(angles, orig_q[3], label="orig")
ax4.step(angles, q_old[3], label="conventional")
ax4.step(angles, q_new[3], label="new")
ax4.set_xlim(angles[0], angles[-1])
ax4.set_xlabel("Angle [rad]", fontsize=15)
ax4.tick_params(labelsize=13)
ax4.set_ylabel('q3', fontsize=15)

# ベクトル同士の比較
fig2 = plt.figure(figsize = (10, 9))  # 横, 縦
ax1 = fig2.add_subplot(311)
ax1.set_title('Vector `b` Comparison', fontsize=20)
ax1.step(angles, b_true[0], label="b_true", linestyle = "--")
ax1.step(angles, b_old[0], label="b_old")
ax1.step(angles, b_new[0], label="b_new")
ax1.set_xlim(angles[0], angles[-1])
ax1.tick_params(labelsize=13)  # 軸目盛の大きさ
ax1.legend(fontsize=15, loc="upper right")
ax1.set_ylabel('b[0]', fontsize=15)

ax2 = fig2.add_subplot(312)
ax2.step(angles, b_true[1], label="b_true", linestyle = "--")
ax2.step(angles, b_old[1], label="b_old")
ax2.step(angles, b_new[1], label="b_new")
ax2.set_xlim(angles[0], angles[-1])
ax2.tick_params(labelsize=13)
ax2.set_ylabel('b[1]', fontsize=15)

ax3 = fig2.add_subplot(313)
ax3.step(angles, b_true[2], label="b_true", linestyle = "--")
ax3.step(angles, b_old[2], label="b_old")
ax3.step(angles, b_new[2], label="b_new")
ax3.set_xlim(angles[0], angles[-1])
ax3.tick_params(labelsize=13)
ax3.set_xlabel("Angle [rad]", fontsize=15)
ax3.set_ylabel('b[2]', fontsize=15)

# 従来のアルゴリズムで計算した場合の誤差
fig3 = plt.figure(figsize = (10, 9))  # 横, 縦
ax1 = fig3.add_subplot(311)
ax1.set_title('Vector Error (Old algorithm)', fontsize=20)
ax1.step(angles, b_error_old[0])
ax1.set_xlim(angles[0], angles[-1])
ax1.tick_params(labelsize=13)  # 軸目盛の大きさ
ax1.set_ylabel('error[0]', fontsize=15)

ax2 = fig3.add_subplot(312)
ax2.step(angles, b_error_old[1])
ax2.set_xlim(angles[0], angles[-1])
ax2.tick_params(labelsize=13)
ax2.set_ylabel('error[1]', fontsize=15)

ax3 = fig3.add_subplot(313)
ax3.step(angles, b_error_old[2])
ax3.set_xlim(angles[0], angles[-1])
ax3.tick_params(labelsize=13)
ax3.set_ylabel('error[2]', fontsize=15)
ax3.set_xlabel("Angle [rad]", fontsize=15)

# 特異点を持たないアルゴリズムで計算した場合の誤差
fig4 = plt.figure(figsize = (10, 9))  # 横, 縦
ax1 = fig4.add_subplot(311)
ax1.set_title('Vector Error (New algorithm)', fontsize=20)
ax1.step(angles, b_error_new[0])
ax1.set_xlim(angles[0], angles[-1])
ax1.tick_params(labelsize=13)  # 軸目盛の大きさ
ax1.set_ylabel('error[0]', fontsize=15)

ax2 = fig4.add_subplot(312)
ax2.step(angles, b_error_new[1])
ax2.set_xlim(angles[0], angles[-1])
ax2.tick_params(labelsize=13)
ax2.set_ylabel('error[1]', fontsize=15)

ax3 = fig4.add_subplot(313)
ax3.step(angles, b_error_new[2])
ax3.set_xlim(angles[0], angles[-1])
ax3.tick_params(labelsize=13)
ax3.set_ylabel('error[2]', fontsize=15)
ax3.set_xlabel("Angle [rad]", fontsize=15)

plt.show()