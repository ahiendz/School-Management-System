import matplotlib.pyplot as plt
import os

def save_parent_chart_image(avg_scores: dict, output_path: str = "Assets/Charts/parent_chart.png"):
    subjects = list(avg_scores.keys())
    scores_sem1 = [avg_scores[sub]["semester_1"] for sub in subjects]
    scores_sem2 = [avg_scores[sub]["semester_2"] for sub in subjects]

    x = range(len(subjects))
    width = 0.35

    width_px = 600
    height_px = 204
    dpi = 100

    # Tính kích thước theo inch: inch = pixel / dpi
    fig_width = width_px / dpi
    fig_height = height_px / dpi

    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=dpi)
    ax.bar([i - width/2 for i in x], scores_sem1, width, label='Học kỳ 1', color='#4a90e2')
    ax.bar([i + width/2 for i in x], scores_sem2, width, label='Học kỳ 2', color='#7ed6df')

    ax.set_ylabel('Điểm trung bình', fontsize=8)
    ax.set_title('So sánh điểm các môn', fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels(subjects, fontsize=8)
    ax.tick_params(axis='y', labelsize=8)
    ax.legend(fontsize=8)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    fig.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path)
    plt.close(fig)
