import streamlit as st
import random, math
import numpy as np
import matplotlib.pyplot as plt

# --- 🎨 유틸리티 함수 (기존과 동일) ---
def random_palette(k=6, seed=None):
    if seed is not None:
        random.seed(seed)
    # 튜플로 구성된 k개의 랜덤 RGB 색상 팔레트 생성
    return [(random.random(), random.random(), random.random()) for _ in range(k)]

def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    # '움직이는' 모양을 생성하는 함수
    angles = np.linspace(0, 2 * math.pi, points)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

# --- 🖼️ Matplotlib 그리기 함수 ---
def draw_3d_poster(n_blobs, seed_val):
    # Figure 준비
    fig, ax = plt.subplots(figsize=(7, 10))
    ax.axis('off')
    ax.set_facecolor((0.95, 0.95, 0.96))

    # 랜덤성과 팔레트 재현성을 위해 시드를 사용합니다.
    random.seed(seed_val)
    np.random.seed(seed_val)
    palette = random_palette(8, seed=seed_val)

    # 깊이감 표현 (n_blobs 만큼 반복)
    for i in range(n_blobs):
        # 위치 및 크기 랜덤 설정
        cx, cy = random.random(), random.random()
        rr = random.uniform(0.2, 0.5)
        x, y = blob(center=(cx, cy), r=rr, wobble=0.15)

        # 그림자 효과 (약간의 오프셋으로 깊이감 표현)
        ax.fill(x + 0.02, y - 0.02, color='black', alpha=0.25, zorder=i)

        # 메인 블롭 (투명도 차이로 깊이, zorder로 레이어 설정)
        color = palette[i % len(palette)]
        # 깊어질수록 투명도를 높여(i*0.1) 배경과 섞이게 함
        alpha_val = 0.7 - (i * 0.1)
        ax.fill(x, y, color=color, alpha=alpha_val, zorder=i + 1)

    # 라벨
    ax.text(0.05, 0.95, "Poster", fontsize=18, weight='bold', transform=ax.transAxes)
    ax.text(0.05, 0.91, f"Seed: {seed_val}, Blobs: {n_blobs}", fontsize=11, transform=ax.transAxes)

    return fig

# --- 💻 Streamlit 앱 메인 함수 ---
def main():
    st.set_page_config(layout="centered")
    st.title("Generative Poster")

    st.sidebar.header("Poster Controls")
    
    # 1. 시드 슬라이더 (랜덤성 재현 및 변경)
    seed_val = st.sidebar.slider('Seed Value (Randomness)', 1, 1000, value=42, step=1)
    
    # 2. 블롭 개수 슬라이더
    n_blobs = st.sidebar.slider('Number of Layers (Depth)', 1, 12, value=6, step=1)
    
    # 3. 새로고침 버튼 (옵션)
    if st.sidebar.button("🔄 Regenerate Poster"):
        st.experimental_rerun()

    # 포스터 그리기 및 Streamlit에 표시
    fig = draw_3d_poster(n_blobs, seed_val)
    st.pyplot(fig)
    plt.close(fig) # 메모리 해제

    st.markdown("---")
    st.write("Concepts: Layering (`zorder`), Shadows (offset fill), Depth (transparency).")

if __name__ == "__main__":
    main()
