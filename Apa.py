import streamlit as st
#LIBRERIA TABLA
import pandas as pd

interest=0
#FUNCIONES
def imprimirtabla(period_type,interest, timei, totalamount, opcion_a_calcular, rate, principal):
        tabla=[]
        RATE=rate/100
        if period_type=="Años":
            timei=timei*12

        if opcion_a_calcular=="Interés Simple":
            
            for i in range(1,timei+1):
                tabla.append({'Mes':i,'Interes a pagar':round(interest/timei,2),'Capital a Pagar':round((totalamount/timei)-(interest/timei),2),' Total a Pagar':round((totalamount/timei),2)})
        else:
            for i in range(1,timei+1):
                tabla.append({'Mes':i,'Interes a pagar':round(interest/timei,2),'Capital a Pagar': round(principal/timei, 2),' Total a Pagar': round(principal*((RATE/12)*((1+(RATE/12))**timei))/(((1+(RATE/12))**timei)-1),2)})
            #falta poner formulas

        return tabla

def conversion_de_tiempo(period_type):
    if period_type=="Meses":
        TIEMPO= time/12
    else:
        TIEMPO= time

    return TIEMPO    

def calculate_credito(principal,rate,TIEMPO,opcion_a_calcular,timei,period_type):
    """Calcula el credito solcitado"""
    if period_type=="Años":
            timei=timei*12
    
    if opcion_a_calcular=="Interés Simple":
        interest=round(principal * ((rate / 100) * TIEMPO), 2)
        total_amount = principal + interest
    else:
        cuotames=principal*((rate/100/12)*((1+(rate/100/12))**timei))/(((1+(rate/100/12))**timei)-1)
        total_amount=cuotames*TIEMPO*12
        interest=total_amount-principal
     
    
    return interest, total_amount

def calculate_inversion(principal,rate,TIEMPO,opcion_a_calcular):
    """Calcula el interés compuesto."""  

    if opcion_a_calcular=="Interés Compuesto":
        interest= round(principal * (1 + (rate / 100)) ** TIEMPO-principal,2)
    else:
        interest=round(principal * (rate / 100) * TIEMPO,2)

    total_amount=principal+interest

    return interest, total_amount

def valor_presente(rate,TIEMPO,fvalue,opcion_a_calcular):
    """Calcula valor presente de una inversion."""
    if opcion_a_calcular=="Interés Simple":
        valor_actual=round(fvalue/(1+(rate/100)*TIEMPO), 2)
    else:
        valor_actual=round(fvalue/((1 + (rate / 100)) ** TIEMPO), 2)

    return valor_actual        

def ahorro(meta, ahorrado):
    DIFERENCIA=meta-ahorrado
    DIFERENCIA_PORCENTUAL=(DIFERENCIA/meta)*100
    return DIFERENCIA_PORCENTUAL, DIFERENCIA

#Interfaz grafica


st.title("PROYECTO PERSONAL DANIEL ERIQUE")
st.write("Calcula créditos e inversiones con interés simple y compuesto.")
st.image("https://preview.redd.it/mickey-and-goofy-possessers-of-the-drip-v0-yb5pxq88epg91.jpg?auto=webp&s=a38e47ee7dab84d96ac380a6cb5d19a313236aaf", width=150,)

#MANUAL DE USUARIO
if 'ver_manual' not in st.session_state:
    st.session_state.ver_manual = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button(" Instrucciones"):
        st.session_state.ver_manual = True

if st.session_state.ver_manual:
    with st.container(border=True):
        st.subheader(" Guía de Uso - Calculadora Financiera")
        
        if st.button("Cerrar Guía "):
            st.session_state.ver_manual = False
            st.rerun()

        st.markdown("""
        ### 1. Configuración Inicial
        En el panel central, selecciona qué deseas hacer:
        * **Solicitar Crédito:** Calcula pagos mensuales y genera una tabla de amortización, que muestra el valor de cada cuota mensual.
        * **Inversión a plazo fijo:** Proyecta el crecimiento de tu capital de forma anual.
        * **Valor presente:** Calcula cuánto invertir hoy para recibir un monto futuro.
        * **Estado del ahorro:** Compara tu ahorro actual contra una meta.

        ### 2. Tipos de Interés
        * **Interés Simple:** El interés se calcula solo sobre el capital original.
        * **Interés Compuesto:** El interés se calcula en base al capital original y el interese se calculan de manera mensual y incrementa o decrece exponencialmente.

        ### 3. Ingreso de Datos (Panel Lateral)
        * **Monto Principal:** La cantidad de dinero inicial a invertir o pedir prestado.
        * **Tasa de Interés:** Ingrese el porcentaje anual (ej. 5.0).
        * **Período:** El tiempo o plazo de la operación. Asegúrese de marcar si este número son 'Meses' o 'Años' en el selector central.

        ### 4. Interpretación de Resultados
        * **Créditos:** Verás una tabla con el desglose mensual de intereses y capital.
        * **Inversion:** Veras la cantidad de intereses ganados anualmente y el total del capital acumulado
        * **Valor presente:** Veras el valor presente a invertir para alcanzar un valor futuro deseado en el plazo y tasa ingresados.            
        * **Ahorro:** Si el resultado aparece en **rojo**, aún no has alcanzado tu meta y se te indicará el porcentaje faltante.

        """)
        st.divider()


# INPUTS
st.header("Tipo de Cálculo")
calculation_type = st.radio("Selecciona el tipo de cálculo:", ("Solicitar Crédito", "Inversión a plazo fijo", "Valor presente", "Estado del ahorro"))
opcion_a_calcular = st.radio("Selecciona el tipo de interés:", ("Interés Simple", "Interés Compuesto"))
period_type=st.radio("Selecciona el tipo de periodo:", ("Meses", "Años" ))

if calculation_type=="Solicitar Crédito" or calculation_type=="Inversión a plazo fijo":
    st.sidebar.header("Parámetros de Entrada")
    principal = st.sidebar.number_input("Monto Principal ($)", min_value=0.0, value=1000.0, step=100.0)
    rate = st.sidebar.number_input("Tasa de Interés Anual (%)", min_value=0.0, value=5.0, step=0.1)
    time =st.sidebar.number_input("Período (Años, Meses)", min_value=1.0, value=1.0, step=1.0)
    timei=int(time)
elif calculation_type=="Valor presente":
    st.sidebar.header("Parámetros de Entrada")
    rate = st.sidebar.number_input("Tasa de Interés Anual (%)", min_value=0.0, value=5.0, step=0.1)
    time = st.sidebar.number_input("Período (Años, Meses)", min_value=0.0, value=1.0, step=1.0)
    fvalue=st.sidebar.number_input("Valor futuro ($)", min_value=0.0, value=1000.0, step=100.0)
    timei=int(time)
else:
    st.sidebar.header("Parámetros de Entrada")
    meta=st.sidebar.number_input("Meta de ahorro($)", min_value=0.0, value=1000.0, step=100.0)
    ahorrado=st.sidebar.number_input("Dinero ahorrado($)", min_value=0.0, value=0.0, step=100.0)


#LLAMA FUNCIONES
if st.button("Calcular"):
    
    if calculation_type=="Valor presente":
        time=conversion_de_tiempo(period_type)
        valor_actual= valor_presente(rate, time,fvalue,opcion_a_calcular)
    
    elif calculation_type== "Solicitar Crédito":
        time=conversion_de_tiempo(period_type)
        interest, total_amount = calculate_credito(principal,rate,time,opcion_a_calcular, timei,period_type)
        tablap=imprimirtabla(period_type,interest,timei,total_amount,opcion_a_calcular,rate,principal)
    
    elif calculation_type=="Inversión a plazo fijo":
        time=conversion_de_tiempo(period_type)  
        interest, total_amount = calculate_inversion(principal,rate,time,opcion_a_calcular)
    else:
        DIFERENCIA_PORCENTUAL, DIFERENCIA=ahorro(meta, ahorrado)
    
    # PRESENTA RESUKTADOS


    st.subheader("Resultados:")

    if calculation_type == "Solicitar Crédito":
        st.success(f"Para un {calculation_type.lower()} de ${principal:,.2f} a una tasa del {rate}% durante {time} años con {opcion_a_calcular.lower()}:")
        st.write(f"Interés a pagar: ${interest:,.2f}")
        st.write(f"Monto Total a Pagar: ${total_amount:,.2f}")
        df = pd.DataFrame(tablap)
        st.write(df)
    elif calculation_type=="Inversión a plazo fijo":  # Inversión
        st.success(f"Para una {calculation_type.lower()} de ${principal:,.2f} a una tasa del {rate}% durante {time} años con {opcion_a_calcular.lower()}:")
        st.write(f"Intereses Ganados: ${interest:,.2f}")
        st.write(f"Valor Futuro de la Inversión: ${total_amount:,.2f}")
    elif calculation_type=="Valor presente":
        st.success(f"Para un valor futuro de ${fvalue:,.2f} a una tasa del {rate}% dentro de {time} años con {opcion_a_calcular.lower()}:")
        st.write(f"Valor presente de la inversion debe ser de {valor_actual:,.2f}")
    else:
        if DIFERENCIA<=0:
            st.success("Ya alcanzo su meta de ahorro")
        else:
            st.error("Todavia no alcanzo su meta de ahorro")
            st.write(f"Usted esta a un {DIFERENCIA_PORCENTUAL:,.2f}(%) lejos de su meta de ahorro")
   
        
