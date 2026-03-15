## Green-Wash Verifier: Supply Chain Carbon Auditor

Green-Wash Verifier is an interactive climate-tech web application that audits the carbon footprint of a product’s entire supply chain. It helps identify misleading sustainability claims (“greenwashing”) by quantifying hidden emissions across logistics routes and comparing them with cleaner alternatives.

Instead of only measuring emissions at the factory, this system evaluates the *full journey* of a product — from raw material source to final retailer — using real-world transport emission factors.

---

## What This Project Does

This tool allows users to:

* Model a product’s supply chain in multiple transport legs
* Calculate CO₂ emissions using standard freight emission factors
* Visualise which part of the route causes the most pollution
* Simulate greener transport options and measure potential savings

This turns sustainability into a **measurable, auditable, and explainable metric**, not just a marketing claim.

---

## How It Works

The system is built using a clean, professional architecture:

| Layer         | File        | Purpose                                             |
| ------------- | ----------- | --------------------------------------------------- |
| Logic Engine  | `engine.py` | Performs carbon calculations using emission factors |
| Web Interface | `app.py`    | Interactive dashboard built with Streamlit          |
| Visualization | Plotly      | Displays emissions by supply-chain leg              |

### Core Formula

For each transport leg:

```
Carbon Emissions = Weight × Distance × Emission Factor
```

The total product footprint is the sum of all legs.

---

## Key Features

* **Multi-leg Supply Chain Modelling**
  Simulate real-world logistics: Source → Factory → Port → Retailer

* **Live Carbon Auditing Dashboard**
  Instantly updates emissions as users change routes and transport modes

* **Greenwashing Detection via Comparison**
  Compares actual routes against optimal low-carbon routes

* **Explainable Visual Analytics**
  Bar charts and tables show exactly where emissions occur

* **What-If Sustainability Simulator**
  Calculates CO₂ savings from cleaner logistics decisions

---

## Tech Stack

* Python
* Streamlit (Web UI)
* NetworkX (Supply chain graph modelling)
* Plotly (Interactive charts)
* Pandas (Data handling)

---

## Project Structure

```
green_wash_verifier/
│
├── engine.py   # Carbon calculation engine
├── app.py      # Streamlit web application
└── README.md   # Project documentation
```

---

## Why This Matters

Many companies claim products are “eco-friendly” while ignoring emissions from global shipping and logistics. This project exposes that blind spot by making supply-chain pollution visible, measurable, and comparable.

Green-Wash Verifier can support:

* ESG auditing
* Sustainable supply chain planning
* Climate policy analysis
* Corporate sustainability reporting

---

## Future Improvements

* Automatic greenwashing risk score
* Route anomaly detection
* Real-world logistics API integration
* Exportable carbon audit reports

---

## Author

Built as a climate-tech data science project focused on transparency, accountability, and real-world impact.

---


