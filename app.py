import streamlit as st
import random
import math
import numpy as np
import matplotlib.pyplot as plt

# --- 🎨 유틸리티 함수 ---
def random_palette(k=5):
    # return k random pastel-like colors
    return [(random.random(), random.random(), random.random()) for _ in range(k)]

def blob(center=(0.2, 0.2), r=0.8, points=500, wobble=0.3):
    # generate a wobbly closed shape
    angles = np.linspace(0, 2 * math.pi, points)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

# --- 🖼️ Matplotlib 그리기 함수 ---
def draw_abstract_poster():
    # Streamlit에서 그림을 표시하기 위해 figure 객체를 생성합니다.
    fig, ax = plt.subplots(figsize=(7, 10))
    ax.axis('off')

    # background
    ax.set_facecolor((0.98, 0.98, 0.97))

    # Set a random seed based on a timestamp or Streamlit rerun to get different art each time
    random.seed() 
    np.random.seed(random.randint(0, 100000)) # Ensure NumPy randomness changes too

    palette = random_palette(6)
    n_layers = 8
    
    for i in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(0.15, 0.45)
        x, y = blob(center=(cx, cy), r=rr, wobble=random.uniform(0.05, 0.25))
        color = random.choice(palette)
        alpha = random.uniform(0.25, 0.6)
        ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0, 0, 0, 0))

    # simple typographic label
    ax.text(0.05, 0.95, "Generative Poster", fontsize=18, weight='bold', transform=ax.transAxes)
    ax.text(0.05, 0.91, "Week 2 • Arts & Advanced Big Data", fontsize=11, transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    return fig

# --- 💻 Streamlit 앱 메인 함수 ---
def main():
    st.set_page_config(layout="centered")
    st.title("Generative Abstract Poster")
    st.write("Click 'Regenerate' to create a new, unique piece of art based on randomness.")

    # 버튼을 누르면 스크립트가 재실행되어 새로운 랜덤 시드로 그림이 그려집니다.
    if st.button("🔄 Regenerate Poster"):
        st.write("") # 버튼 클릭 시 상태 업데이트 유도를 위한 코드

    # 포스터 그리기 함수 호출 및 Streamlit에 표시
    fig = draw_abstract_poster()
    st.pyplot(fig)
    plt.close(fig) # 메모리 해제

if __name__ == "__main__":
    main()
