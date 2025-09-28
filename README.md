# **Nubra Market Analysis & GTM Strategy**  

A complete **Go-to-Market (GTM) strategy** and **market sizing analysis** for Nubra, aimed at onboarding engineers in India into the trading ecosystem. Includes business analysis using **TAM–SAM–SOM**, a 1-year GTM plan, and an **interactive Streamlit app** for scenario testing.  

---

## **Overview**  
**Objective:** Onboard students, professionals, and freelancers into trading via Nubra  

**Approach:** Market sizing → 1-year phased GTM plan  

**Tools:** Python, Streamlit, Pandas, Matplotlib  

---

## **Market Sizing**  
- **TAM (Total Addressable Market):** All engineers in India (~15–16M)
 
  **Formula:**
               `TAM = Students + Professionals`
  
- **SAM (Serviceable Available Market):** Engineers with smartphones, internet, and disposable income (~9–10M)
  
  **Formula:**
               `SAM = TAM × Smartphone Penetration (%)`
  
- **SOM (Serviceable Obtainable Market):** Realistically reachable engineers in Year 1 (~300K–500K)
  
  **Formula:**
               `SOM = SAM × Adoption Rate (%)`  

  **Revenue Formula:**
               `Revenue = SOM × ARPU`  

---

## **Streamlit App Features**  

- Interactive **TAM–SAM–SOM calculator**  
- Adjustable sliders: smartphone penetration, adoption rate, ARPU  
- Charts: **TAM vs SAM vs SOM**, state-wise SOM & revenue, adoption scenarios  
- Filters by state and penetration level  
- CSV export for reporting  

---

## **1-Year GTM Plan**  

**Phase 1: Awareness (Months 1–3)**  

- Campus activations  
- Influencer marketing campaigns  

**Phase 2: Acquisition (Months 4–6)**  

- Referral programs  
- Gamified trading contests  
- Corporate pilot programs  

**Phase 3: Engagement & Monetization (Months 7–12)**  

- Trading certifications  
- Community building for engineers  
- Premium trading tools  

---

## **Success Metrics**  

- **Adoption:** New users, CAC, referral-driven signups  
- **Engagement:** DAU/MAU, trades per user, contest participation  
- **Retention:** 30/60/90-day retention, churn rate  
- **Business Impact:** ARPU, LTV, total revenue  

---



# Run the Streamlit app
streamlit run Nubra_market_size.py
