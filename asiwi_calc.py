
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Калькулятор партнёрской прибыли", layout="centered")
st.title("🔄 Универсальный расчёт по одной сумме")

st.markdown("Если у вас нет спецификации — просто введите известную сумму и выберите, от кого она: от подрядчика или от клиента.")

known_party = st.selectbox("Эта сумма получена от...", ["Подрядчика", "Клиента"])
sum_with_nds = st.number_input("Введите сумму:", min_value=0.0, step=1000.0, format="%.2f")
includes_nds = st.checkbox("Сумма включает НДС", value=True)
desired_profit = st.number_input("Желаемая чистая прибыль (можно оставить 0):", min_value=0.0, step=1000.0)

if st.button("🔁 Рассчитать встречную сумму"):
    nds_rate = 0.2

    if known_party == "Подрядчика":
        # Считаем сколько нужно выставить клиенту
        if includes_nds:
            nds_sub = sum_with_nds * nds_rate / (1 + nds_rate)
            net_sub = sum_with_nds - nds_sub
        else:
            net_sub = sum_with_nds
            nds_sub = net_sub * nds_rate
            sum_with_nds = net_sub + nds_sub

        nds_loss = nds_sub * 0.75
        direct_costs = net_sub + nds_loss
        tax_base = desired_profit / 0.95
        total_client_net = direct_costs + tax_base
        total_client_sum = total_client_net * (1 + nds_rate)

        st.markdown(f"📦 **Сумма от подрядчика:** `{sum_with_nds:,.2f} ₽`".replace(",", " ").replace(".", ","))
        st.markdown(f"💰 **НДС подрядчика:** `{nds_sub:,.2f} ₽`".replace(",", " ").replace(".", ","))
        st.markdown(f"🔄 **Нужно выставить клиенту:** `{total_client_sum:,.2f} ₽`".replace(",", " ").replace(".", ","))
        st.markdown(f"🧮 **Чистая прибыль будет:** `{desired_profit:,.2f} ₽`".replace(",", " ").replace(".", ","))

    else:
        # Считаем сколько можно заплатить подрядчику
        if includes_nds:
            nds_client = sum_with_nds * nds_rate / (1 + nds_rate)
            net_client = sum_with_nds - nds_client
        else:
            net_client = sum_with_nds
            nds_client = net_client * nds_rate
            sum_with_nds = net_client + nds_client

        tax_base = net_client / (1 + (0.75 * nds_rate)) - (desired_profit / 0.95)
        net_sub = tax_base
        nds_sub = net_sub * nds_rate
        total_sub_sum = net_sub + nds_sub

        st.markdown(f"📦 **Сумма от клиента:** `{sum_with_nds:,.2f} ₽`".replace(",", " ").replace(".", ","))
        st.markdown(f"💰 **НДС клиента:** `{nds_client:,.2f} ₽`".replace(",", " ").replace(".", ","))
        st.markdown(f"📤 **Можно заплатить подрядчику:** `{total_sub_sum:,.2f} ₽`".replace(",", " ").replace(".", ","))
        st.markdown(f"🧮 **Чистая прибыль будет:** `{desired_profit:,.2f} ₽`".replace(",", " ").replace(".", ","))
