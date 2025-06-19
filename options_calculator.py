import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy.stats import norm
import math

# Configuration de la page
st.set_page_config(
    page_title="Calculateur d'Options Black-Scholes",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre principal avec style
st.markdown("""
    <h1 style='text-align: center; color: #1f77b4; font-size: 3em; margin-bottom: 0;'>
        📈 Calculateur d'Options Black-Scholes
    </h1>
    <p style='text-align: center; color: #666; font-size: 1.2em; margin-top: 0;'>
        Évaluation professionnelle et analyse des Greeks
    </p>
    """, unsafe_allow_html=True)

# CSS personnalisé pour un meilleur design
st.markdown("""
    <style>
    .metric-container {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .greek-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)


class BlackScholesCalculator:
    """Calculateur Black-Scholes avec Greeks"""
    
    @staticmethod
    def black_scholes_price(S, K, T, r, sigma, option_type='call'):
        """Calcule le prix Black-Scholes"""
        if T <= 0 or sigma <= 0:
            return 0
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        if option_type == 'call':
            price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        else:  # put
            price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        
        return max(0, price)
    
    @staticmethod
    def calculate_greeks(S, K, T, r, sigma, option_type='call'):
        """Calcule tous les Greeks"""
        if T <= 0:
            return {'delta': 0, 'gamma': 0, 'theta': 0, 'vega': 0, 'rho': 0}
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        # Delta
        if option_type == 'call':
            delta = norm.cdf(d1)
        else:
            delta = norm.cdf(d1) - 1
        
        # Gamma (identique pour call et put)
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        
        # Theta
        if option_type == 'call':
            theta = (-(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) 
                    - r * K * np.exp(-r * T) * norm.cdf(d2))
        else:
            theta = (-(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) 
                    + r * K * np.exp(-r * T) * norm.cdf(-d2))
        
        # Vega (identique pour call et put)
        vega = S * norm.pdf(d1) * np.sqrt(T)
        
        # Rho
        if option_type == 'call':
            rho = K * T * np.exp(-r * T) * norm.cdf(d2)
        else:
            rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)
        
        return {
            'delta': delta,
            'gamma': gamma,
            'theta': theta / 365,  # Par jour
            'vega': vega / 100,    # Pour 1% de volatilité
            'rho': rho / 100       # Pour 1% de taux
        }


def main():
    # Sidebar pour les paramètres
    st.sidebar.header("⚙️ Paramètres de l'option")
    
    # Paramètres d'entrée
    S = st.sidebar.number_input("Prix du sous-jacent (S)", value=100.0, min_value=0.1, step=0.1)
    K = st.sidebar.number_input("Prix d'exercice (K)", value=105.0, min_value=0.1, step=0.1)
    T = st.sidebar.number_input("Temps à expiration (années)", value=0.25, min_value=0.001, max_value=5.0, step=0.01)
    r = st.sidebar.number_input("Taux sans risque (%)", value=5.0, min_value=0.0, max_value=20.0, step=0.1) / 100
    sigma = st.sidebar.number_input("Volatilité (%)", value=20.0, min_value=0.1, max_value=100.0, step=0.1) / 100
    option_type = st.sidebar.selectbox("Type d'option", ['call', 'put'])
    
    # Calculs
    calculator = BlackScholesCalculator()
    price = calculator.black_scholes_price(S, K, T, r, sigma, option_type)
    greeks = calculator.calculate_greeks(S, K, T, r, sigma, option_type)
    
    # Valeur intrinsèque
    if option_type == 'call':
        intrinsic_value = max(0, S - K)
    else:
        intrinsic_value = max(0, K - S)
    
    time_value = price - intrinsic_value
    
    # Interface principale avec onglets
    tab1, tab2, tab3, tab4 = st.tabs(["🧮 Calculateur", "📊 Greeks", "📈 Sensibilité", "🎯 Stratégies"])
    
    with tab1:
        # Résultats principaux
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class="metric-container">
                    <h3>Prix de l'option</h3>
                    <h2>€{price:.4f}</h2>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-container">
                    <h3>Valeur intrinsèque</h3>
                    <h2>€{intrinsic_value:.4f}</h2>
                </div>
                """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-container">
                    <h3>Valeur temps</h3>
                    <h2>€{time_value:.4f}</h2>
                </div>
                """, unsafe_allow_html=True)
        
        # Graphique prix vs spot
        st.subheader("📈 Évolution du prix selon le sous-jacent")
        
        spot_range = np.linspace(S * 0.7, S * 1.3, 50)
        prices = [calculator.black_scholes_price(spot, K, T, r, sigma, option_type) for spot in spot_range]
        intrinsic_values = [max(0, spot - K) if option_type == 'call' else max(0, K - spot) for spot in spot_range]
        
        fig_price = go.Figure()
        fig_price.add_trace(go.Scatter(x=spot_range, y=prices, mode='lines', name='Prix de l\'option', line=dict(color='blue', width=3)))
        fig_price.add_trace(go.Scatter(x=spot_range, y=intrinsic_values, mode='lines', name='Valeur intrinsèque', line=dict(color='red', dash='dash')))
        fig_price.add_vline(x=S, line_dash="dot", line_color="green", annotation_text="Prix actuel")
        fig_price.update_layout(title="Prix de l'option vs Prix du sous-jacent", xaxis_title="Prix du sous-jacent", yaxis_title="Prix", height=400)
        st.plotly_chart(fig_price, use_container_width=True)
        
        # Impact de la volatilité
        st.subheader("🌪️ Impact de la volatilité")
        
        vol_range = np.linspace(0.1, 0.5, 30)
        vol_prices = [calculator.black_scholes_price(S, K, T, r, vol, option_type) for vol in vol_range]
        
        fig_vol = go.Figure()
        fig_vol.add_trace(go.Scatter(x=vol_range*100, y=vol_prices, mode='lines', name='Prix', line=dict(color='purple', width=3)))
        fig_vol.add_vline(x=sigma*100, line_dash="dot", line_color="green", annotation_text="Volatilité actuelle")
        fig_vol.update_layout(title="Prix de l'option vs Volatilité", xaxis_title="Volatilité (%)", yaxis_title="Prix", height=400)
        st.plotly_chart(fig_vol, use_container_width=True)
    
    with tab2:
        st.header("📊 Analyse des Greeks")
        
        # Affichage des Greeks
        col1, col2 = st.columns(2)
        
        greeks_data = [
            {"Greek": "Delta", "Valeur": f"{greeks['delta']:.4f}", "Description": "Sensibilité au prix du sous-jacent", "Couleur": "#1f77b4"},
            {"Greek": "Gamma", "Valeur": f"{greeks['gamma']:.4f}", "Description": "Sensibilité du delta", "Couleur": "#ff7f0e"},
            {"Greek": "Theta", "Valeur": f"{greeks['theta']:.4f}", "Description": "Décroissance temporelle (par jour)", "Couleur": "#d62728"},
            {"Greek": "Vega", "Valeur": f"{greeks['vega']:.4f}", "Description": "Sensibilité à la volatilité", "Couleur": "#9467bd"},
            {"Greek": "Rho", "Valeur": f"{greeks['rho']:.4f}", "Description": "Sensibilité au taux sans risque", "Couleur": "#8c564b"}
        ]
        
        for i, greek in enumerate(greeks_data):
            if i % 2 == 0:
                with col1:
                    st.markdown(f"""
                        <div class="greek-card">
                            <h3 style="color: {greek['Couleur']}; margin: 0;">{greek['Greek']}: {greek['Valeur']}</h3>
                            <p style="margin: 0.5rem 0 0 0; color: #666;">{greek['Description']}</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                with col2:
                    st.markdown(f"""
                        <div class="greek-card">
                            <h3 style="color: {greek['Couleur']}; margin: 0;">{greek['Greek']}: {greek['Valeur']}</h3>
                            <p style="margin: 0.5rem 0 0 0; color: #666;">{greek['Description']}</p>
                        </div>
                        """, unsafe_allow_html=True)
        
        # Graphique Delta et Gamma
        st.subheader("Delta et Gamma vs Prix du sous-jacent")
        
        deltas = []
        gammas = []
        for spot in spot_range:
            greek_temp = calculator.calculate_greeks(spot, K, T, r, sigma, option_type)
            deltas.append(greek_temp['delta'])
            gammas.append(greek_temp['gamma'])
        
        fig_greeks = make_subplots(specs=[[{"secondary_y": True}]])
        fig_greeks.add_trace(go.Scatter(x=spot_range, y=deltas, mode='lines', name='Delta', line=dict(color='blue')), secondary_y=False)
        fig_greeks.add_trace(go.Scatter(x=spot_range, y=gammas, mode='lines', name='Gamma', line=dict(color='orange')), secondary_y=True)
        fig_greeks.add_vline(x=S, line_dash="dot", line_color="green", annotation_text="Prix actuel")
        fig_greeks.update_xaxes(title_text="Prix du sous-jacent")
        fig_greeks.update_yaxes(title_text="Delta", secondary_y=False)
        fig_greeks.update_yaxes(title_text="Gamma", secondary_y=True)
        fig_greeks.update_layout(title="Évolution Delta et Gamma", height=400)
        st.plotly_chart(fig_greeks, use_container_width=True)
        
        # Interprétation des Greeks
        st.subheader("🔍 Interprétation")
        st.info(f"""
        **Delta ({greeks['delta']:.4f}):** Pour une hausse de 1€ du sous-jacent, l'option varie de {greeks['delta']:.4f}€
        
        **Gamma ({greeks['gamma']:.4f}):** Le delta change de {greeks['gamma']:.4f} pour chaque 1€ de mouvement
        
        **Theta ({greeks['theta']:.4f}):** L'option perd {abs(greeks['theta']):.4f}€ par jour qui passe
        
        **Vega ({greeks['vega']:.4f}):** +1% de volatilité = +{greeks['vega']:.4f}€ sur l'option
        
        **Rho ({greeks['rho']:.4f}):** +1% de taux = +{greeks['rho']:.4f}€ sur l'option
        """)
    
    with tab3:
        st.header("📈 Analyse de sensibilité")
        
        # Métriques de base
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            moneyness = (S / K - 1) * 100
            st.metric("Moneyness", f"{moneyness:.1f}%", 
                     "ITM" if (moneyness > 0 and option_type == 'call') or (moneyness < 0 and option_type == 'put') else "OTM")
        
        with col2:
            days_to_expiry = T * 365
            st.metric("Jours restants", f"{days_to_expiry:.0f}")
        
        with col3:
            st.metric("Vol. implicite", f"{sigma*100:.1f}%")
        
        with col4:
            st.metric("Valeur temps", f"€{time_value:.4f}")
        
        # Analyse de scénarios
        st.subheader("🎭 Analyse de scénarios")
        
        scenarios = [
            {"Nom": "Baisse 10%", "Prix": S * 0.9, "Couleur": "#d62728"},
            {"Nom": "Baisse 5%", "Prix": S * 0.95, "Couleur": "#ff7f0e"},
            {"Nom": "Actuel", "Prix": S, "Couleur": "#2ca02c"},
            {"Nom": "Hausse 5%", "Prix": S * 1.05, "Couleur": "#1f77b4"},
            {"Nom": "Hausse 10%", "Prix": S * 1.1, "Couleur": "#9467bd"}
        ]
        
        scenario_results = []
        for scenario in scenarios:
            new_price = calculator.black_scholes_price(scenario["Prix"], K, T, r, sigma, option_type)
            pnl = new_price - price
            pnl_pct = (pnl / price * 100) if price > 0 else 0
            scenario_results.append({
                "Scénario": scenario["Nom"],
                "Prix sous-jacent": f"€{scenario['Prix']:.2f}",
                "Prix option": f"€{new_price:.4f}",
                "P&L": f"€{pnl:.4f}",
                "P&L %": f"{pnl_pct:.1f}%"
            })
        
        df_scenarios = pd.DataFrame(scenario_results)
        st.dataframe(df_scenarios, use_container_width=True)
        
        # Heatmap de sensibilité
        st.subheader("🌡️ Heatmap de sensibilité (Prix vs Volatilité)")
        
        price_range = np.linspace(S * 0.8, S * 1.2, 10)
        vol_range_heat = np.linspace(sigma * 0.5, sigma * 1.5, 10)
        
        heatmap_data = []
        for p in price_range:
            row = []
            for v in vol_range_heat:
                option_price = calculator.black_scholes_price(p, K, T, r, v, option_type)
                row.append(option_price)
            heatmap_data.append(row)
        
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=[f"{v*100:.1f}%" for v in vol_range_heat],
            y=[f"€{p:.0f}" for p in price_range],
            colorscale='RdYlBu_r',
            colorbar=dict(title="Prix option")
        ))
        fig_heatmap.update_layout(
            title="Sensibilité Prix de l'option (Y: Prix sous-jacent, X: Volatilité)",
            xaxis_title="Volatilité",
            yaxis_title="Prix sous-jacent",
            height=400
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with tab4:
        st.header("🎯 Stratégies d'options")
        
        # Stratégies de base
        strategies = [
            {
                "nom": "Long Call",
                "description": "Achat d'un call - Position bullish",
                "cout": price,
                "max_gain": "Illimité",
                "max_perte": price,
                "seuil": K + price,
                "conseil": "Utilisez si vous anticipez une hausse significative"
            },
            {
                "nom": "Long Put", 
                "description": "Achat d'un put - Position bearish",
                "cout": calculator.black_scholes_price(S, K, T, r, sigma, 'put'),
                "max_gain": K - calculator.black_scholes_price(S, K, T, r, sigma, 'put'),
                "max_perte": calculator.black_scholes_price(S, K, T, r, sigma, 'put'),
                "seuil": K - calculator.black_scholes_price(S, K, T, r, sigma, 'put'),
                "conseil": "Utilisez si vous anticipez une baisse significative"
            },
            {
                "nom": "Covered Call",
                "description": "Détention action + Vente call",
                "cout": -price,  # On reçoit la prime
                "max_gain": (K - S) + price if K > S else price,
                "max_perte": "Limitée à la baisse de l'action",
                "seuil": S - price,
                "conseil": "Stratégie de génération de revenus sur actions détenues"
            },
            {
                "nom": "Protective Put",
                "description": "Détention action + Achat put",
                "cout": calculator.black_scholes_price(S, K, T, r, sigma, 'put'),
                "max_gain": "Illimité (moins la prime)",
                "max_perte": S - K + calculator.black_scholes_price(S, K, T, r, sigma, 'put'),
                "seuil": S + calculator.black_scholes_price(S, K, T, r, sigma, 'put'),
                "conseil": "Assurance contre la baisse de votre portefeuille"
            }
        ]
        
        for i, strategy in enumerate(strategies):
            with st.expander(f"📋 {strategy['nom']}", expanded=(i==0)):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Description:** {strategy['description']}")
                    st.write(f"**Coût initial:** €{abs(strategy['cout']):.4f} {'(reçu)' if strategy['cout'] < 0 else '(payé)'}")
                    st.write(f"**Gain maximum:** {strategy['max_gain'] if isinstance(strategy['max_gain'], str) else f'€{strategy['max_gain']:.4f}'}")
                
                with col2:
                    st.write(f"**Perte maximum:** {strategy['max_perte'] if isinstance(strategy['max_perte'], str) else f'€{strategy['max_perte']:.4f}'}")
                    st.write(f"**Seuil de rentabilité:** €{strategy['seuil']:.2f}")
                    st.info(f"💡 {strategy['conseil']}")
        
        # Comparaison rapide
        st.subheader("⚖️ Comparaison rapide")
        
        comparison_data = {
            "Stratégie": [s["nom"] for s in strategies],
            "Coût": [f"€{abs(s['cout']):.4f}" for s in strategies],
            "Risque": ["Limité", "Limité", "Élevé", "Limité"],
            "Potentiel": ["Illimité", "Limité", "Limité", "Élevé"],
            "Complexité": ["Faible", "Faible", "Moyenne", "Moyenne"]
        }
        
        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison, use_container_width=True)


if __name__ == "__main__":
    main()