# 🎬 Movie Emotion Analysis

An **interactive visualization platform** that analyzes and compares movie emotions from **scripts, reviews, trailers**, and **user perceptions**.

---

## 🚀 Features

* 🎭 **Multimodal Emotion Analysis**

  * Scripts & Subtitles → Sentiment arcs (HuggingFace transformers)
  * Audience Reviews → Emotion classification (BERT-based)
  * Movie Trailers → Video-language model (NVILA-Lite-15B-Video, fine-tuned on EmoStim)
* 🌍 **Interactive Visualization**

  * Global map of movie ratings by country
  * Regional sortable film tables
  * Film detail pages with side-by-side comparisons
* 📊 **Evaluation**

  * RMSE for script models, MAE for video models
  * Benchmarked against baseline/random predictions

---

## 📂 Project Structure

```
.
├── data/                # Sample data (subtitles, reviews, videos)
├── notebooks/           # Jupyter notebooks for analysis
├── src/                 # Core scripts (preprocessing, models, visualization)
├── results/             # Output figures & metrics
└── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/username/movie-emotion-analysis.git
cd movie-emotion-analysis
pip install -r requirements.txt
```

---

## 🖥️ Demo

* 🌍 Explore global rating map
* 📑 View emotion arcs from scripts/reviews
* 🎥 Compare video-based predictions with user-selected emotions

---

## 📌 Future Improvements

* Multilingual support
* Real-time user feedback integration
* Broader media analytics (TV, streaming, games)


The site is live at https://xinjiez9.github.io/CSE6242/
