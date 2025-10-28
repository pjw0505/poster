import streamlit as st
import random, math
import numpy as np
import matplotlib.pyplot as plt

# --- 🎨 유틸리티 함수 (기존과 동일) ---
def random_palette(k=8, seed=None):
    if seed is not None:
        random.seed(seed)
    # Streamlit에서 랜덤성을 유지하기 위해 random.seed()를 사용합니다.
    # 단, Streamlit이 전체 스크립트를 재실행하므로, palette는 함수 내에서 생성하지 않고
    # 세션 상태(st.session_state)를 이용해 외부에서 관리해야 합니다.
    return [(random.random(), random.random(), random.random()) for _ in range(k)]

def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    angles = np.linspace(0, 2 * math.pi, points)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

# --- 🖼️ Matplotlib 그리기 함수 ---
def draw_poster(n_layers, wobble_val, blobs_data, palette):
    # Figure 준비 (plt.subplots()를 사용해야 Streamlit에서 올바르게 표시됩니다)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.axis('off')
    ax.set_facecolor((0.98, 0.98, 0.97))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # 1. 랜덤 블롭 생성 및 그리기
    for i in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(0.15, 0.45)
        x, y = blob(center=(cx, cy), r=rr, wobble=wobble_val)
        color = random.choice(palette)
        ax.fill(x, y, color=color, alpha=0.5, edgecolor=(0, 0, 0, 0))

    # 2. '클릭' 블롭 데이터 그리기 (마우스 클릭 기능 대체)
    for cx, cy, c in blobs_data:
        # Streamlit에서는 마우스 클릭 기능을 직접 구현하기 어려우므로,
        # 이 부분은 '저장된' 블롭을 표시하는 용도로 사용합니다.
        x, y = blob(center=(cx, cy), r=0.2, wobble=0.1)
        ax.fill(x, y, color=c, alpha=0.7)

    # 3. 라벨
    ax.text(0.05, 0.95, "Interactive Poster", fontsize=16, weight='bold', transform=ax.transAxes)
    ax.text(0.05, 0.91, f"Layers: {n_layers}, Wobble: {wobble_val:.2f}", fontsize=11, transform=ax.transAxes)

    # Streamlit에 Figure 표시
    st.pyplot(fig)
    plt.close(fig) # 메모리 절약

# --- 💻 Streamlit 앱 메인 함수 ---
def main():
    st.set_page_config(layout="centered")
    st.title("Generative Poster on Streamlit")

    # 1. 세션 상태 초기화 (Streamlit에서 상태를 유지하는 방법)
    if 'palette' not in st.session_state:
        st.session_state.palette = random_palette(8)
    if 'blobs' not in st.session_state:
        st.session_state.blobs = []

    # 2. 슬라이더 설정 (Streamlit 위젯)
    st.sidebar.header("Poster Parameters")
    n_layers = st.sidebar.slider('Layers (n_layers)', 1, 12, value=8, step=1)
    wobble_val = st.sidebar.slider('Wobble (wobble_val)', 0.05, 0.4, value=0.3, step=0.01)

    # 3. '마우스 클릭' 기능 대체 (랜덤 블롭 추가 버튼)
    def add_random_blob():
        cx, cy = random.uniform(0.1, 0.9), random.uniform(0.1, 0.9)
        c = random.choice(st.session_state.palette)
        st.session_state.blobs.append((cx, cy, c))

    col1, col2 = st.sidebar.columns(2)
    col1.button("✨ Add Random Blob", on_click=add_random_blob)
    col2.button("🔄 Reset Blobs", on_click=lambda: st.session_state.update(blobs=[]))
    st.sidebar.info("파라미터를 변경하거나 블롭을 추가하면 포스터가 재생성됩니다.")

    # 4. 포스터 그리기
    # 매개변수가 변경될 때마다 이 함수가 재실행되어 포스터가 그려집니다.
    draw_poster(n_layers, wobble_val, st.session_state.blobs, st.session_state.palette)

    # 5. 팔레트 리셋 버튼
    if st.button("🎨 Generate New Palette"):
        st.session_state.palette = random_palette(8)
        st.experimental_rerun()


if __name__ == "__main__":
    main()
