<div align="center">

# 🌱 Green-Wash Verifier: Supply Chain Carbon Auditor

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)](https://streamlit.io/)

**An interactive climate-tech web application that audits the carbon footprint of a product’s entire supply chain.**

[Features](#-key-features) • [How It Works](#%EF%B8%8F-how-it-works) • [Tech Stack](#%EF%B8%8F-tech-stack) • [Why This Matters](#-why-this-matters)

</div>

---

## 📖 About the Project

**Green-Wash Verifier** helps identify misleading sustainability claims (“greenwashing”) by quantifying hidden emissions across logistics routes and comparing them with cleaner alternatives.

Instead of only measuring emissions at the factory, this system evaluates the *full journey* of a product — from raw material source to final retailer — using real-world transport emission factors. This turns sustainability into a **measurable, auditable, and explainable metric**, not just a marketing claim.

---

## ✨ Key Features

* 🌍 **Multi-leg Supply Chain Modelling**: Simulate real-world logistics: Source → Factory → Port → Retailer.
* 📊 **Live Carbon Auditing Dashboard**: Instantly updates emissions as users change routes and transport modes.
* 🔍 **Greenwashing Detection**: Compares actual routes against optimal low-carbon routes.
* 📈 **Explainable Visual Analytics**: Bar charts and tables show exactly where emissions occur.
* 💡 **What-If Sustainability Simulator**: Calculates CO₂ savings from cleaner logistics decisions.

---

## ⚙️ How It Works

The system is built using a clean, professional architecture:

| Layer         | File          | Purpose                                             |
| ------------- | ------------- | --------------------------------------------------- |
| **Logic Engine**  | `engine.py`   | Performs carbon calculations using emission factors |
| **Web Interface** | `app.py`      | Interactive dashboard built with Streamlit          |
| **Visualization** | `Plotly`      | Displays emissions by supply-chain leg              |

### 🧮 Core Formula

For each transport leg:
> **Carbon Emissions = Weight × Distance × Emission Factor**

*The total product footprint is the sum of all legs.*

---

## 🛠️ Tech Stack

<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly" />
</p>

* **Python** - Core logic and calculations
* **Streamlit** - Interactive Web UI
* **NetworkX** - Supply chain graph modelling
* **Plotly** - Interactive charts & visualizations
* **Pandas** - Data handling & manipulation

---

## 📁 Project Structure

```bash
green_wash_verifier/
│
├── engine.py   # Carbon calculation engine
├── app.py      # Streamlit web application
└── README.md   # Project documentation
```

*(Note: Additional files for API services and Streamlit configs may exist as the project grows).*

---

## 🎯 Why This Matters

Many companies claim products are “eco-friendly” while ignoring emissions from global shipping and logistics. This project exposes that blind spot by making supply-chain pollution visible, measurable, and comparable.

**Green-Wash Verifier can support:**
* 🏢 **ESG Auditing**
* 🚚 **Sustainable Supply Chain Planning**
* 📜 **Climate Policy Analysis**
* 📊 **Corporate Sustainability Reporting**

---

## 🚀 Future Improvements

- [ ] Automatic greenwashing risk score
- [ ] Route anomaly detection
- [ ] Real-world logistics API integration
- [ ] Exportable carbon audit reports (PDF/CSV)

---

<div align="center">
  <b>Built as a climate-tech data science project focused on transparency, accountability, and real-world impact.</b>
</div>
