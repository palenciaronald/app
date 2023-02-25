import streamlit as st
import pandas as pd
from scipy import stats
import numpy as np
from PIL import Image



st.title('Consultar puntaje de crédito')

st.markdown('- Reporte técnico: https://marloneau.quarto.pub/creacion-scorecard-para-calculo-de-puntaje-crediticio/#ajuste-del-modelo-y-realizaci%C3%B3n-de-scorecard')
st.markdown('- Video acerca de la aplicación: https://youtu.be/pm0IFjFrN0s')

st.markdown('## ¿Qué es el Scorecard?')
st.markdown('Uno de los principales actividades de los bancos es el prestamo de dinero.Saber a quién prestar es un problema porque deben saber si el dinero si se les va a regresar.Por esta razón se desarolló un puntaje de crédito, el cual es un número que representa la probabilidad que el prestatario regrese el dinero al banco a tiempo.')

image = Image.open('credit.png')
st.image(image)

st.markdown('La anterior imagen es un ejemplo de el Scorecard, el cual son unos intervalos que indican que tan bueno es prestar dinero según el puntaje que adquiera.')

st.markdown('## ¿Por qué es importante?')

st.markdown('Este número también le proporciona unade ideacomo estaría su bienestar financiero. Es decir como su situación financiera y decisiones monetarias le proporcionan seguridad y libertad en sus decisiones.')

st.markdown('### Consulte su puntaje de crédito')
st.markdown('Con el siguiente formulario puede consultar su puntaje de crédito. Además podrá comparar su puntaje con el resto de la población ')

image3 = Image.open('desarrollo2.png')
with st.sidebar:
    
    st.image(image3,width=80)
    st.markdown("#### Desarrollado por:")
    st.markdown("- Ronald Gabriel Palencia.")
    st.markdown("   ronaldpalencia1604@gmail.com")
    st.markdown("- Daniel Santiago Cadavid Montoya.")
    st.markdown("   dcadavid@unal.edu.co")
    st.markdown("- Jose Daniel Bustamante Arango.")
    st.markdown("   jobustamantea@unal.edu.co")
    st.markdown("- Marlon Calle Areiza.")
    st.markdown("   mcalle@unal.edu.co")
    st.markdown("- Daniel Daza Macías.")
    st.markdown("   dadazam@unal.edu.co")


with st.form("my_form"):
    option_purpose = st.selectbox(
    '¿Cuál es el propósito del crédito?',
    ('Consolidación de una deuda','Tarjeta de crédito','Compra importante (carro, mejoras en la casa)','Educación, Energía renovable, Mudanza o Negocio pequeño', 
    'Vacaciones, Boda, Salud, Casa, u Otro'))

    option_verification_status = st.selectbox(
    '¿Fueron los ingresos verificados por el Lending Club?',
    ('No','Si','Se verificó la fuente de ingresos'))

    option_home_ownership = st.selectbox(
    'Su casa:',
    ('Es Propia','Está con hipoteca', 'Es arrendada u otra opción'))


    option_tot_cur_bal = st.text_input('Balance actual total de todas las cuentas (valor en dólares)')
    
    option_dti = st.text_input('Dti del prestatario (si no conoce este valor escriba NA)')

    option_inq_last_6mths = st.text_input('Número de consultas en los últimos 6 meses')

    option_out_prncp = st.text_input('Capital restante pendiente por el monto total financiado (valor en dólares)') 

    option_int_rate = st.text_input('Tasa de interés (de 0 a 100)')

    option_term = st.selectbox(
    '¿Cuál es el término del crédito (en meses)?',
    (36, 60))

    option_annual_inc = st.text_input('¿Cuáles son sus ingresos anuales? (valor en dólares)')

    option_revol_util = st.text_input('¿Cuál es la tasa de utilización del crédito? (valores de 0 a 1)')

    option_grade = st.selectbox(
    '¿Grado de préstamo asignado en la carta de crédito?',
    ('A','B','C','D','E','F','G','No sabe'))

    submitted = st.form_submit_button("Enviar")

    df = pd.read_csv('scorecard.csv')
    puntaje = pd.read_csv('y_scores.csv')
    lista = puntaje['0'].tolist()
    
    
  
   
    scores_dict = dict(zip( df['Feature name'], df['Score - Final']))

    opciones = {
        ###Variable purpose
        'Consolidación de una deuda':'home_ownership:OWN',
        'Tarjeta de crédito':'purpose:credit_card',
        'Compra importante (carro, mejoras en la casa)':'purpose:major_purch__car__home_impr',
        'Educación, Energía renovable, Mudanza o Negocio pequeño':'purpose:educ__ren_en__sm_b__mov',
        'Vacaciones, Boda, Salud, Casa, u Otro':'purpose:vacation__house__wedding__med__oth',

        ###Variable verification_status
        'No':'verification_status:Not Verified',
        'Si':'verification_status:Verified',
        'Se verificó la fuente de ingresos':'verification_status:Source Verified',

        ###Variable home_ownership
        'Es Propia':'home_ownership:OWN',
        'Está con hipoteca':'home_ownership:MORTGAGE',
        'Es arrendada u otra opción':'home_ownership:OTHER_NONE_RENT',

        ###Variable option_grade
        'A':'grade:A',
        'B':'grade:B',
        'C':'grade:C',
        'D':'grade:D',
        'E':'grade:E',
        'F':'grade:F',
        'G':'grade:G',
        'No sabe':'grade:G',        #Si no sabe se le asigna grade:G para que no sume ni reste

        ###Variable term
        36:'term:36',
        60:'term:60'
    }

    if submitted:
        if option_tot_cur_bal == '' or option_dti == '' or option_inq_last_6mths == '' or option_out_prncp == '' or option_int_rate == '' or option_annual_inc == '' or option_revol_util == '':
            st.markdown('### Datos faltantes. Llena todo el formulario')

        else:    
            #print('hola')
            #print(len([option_tot_cur_bal,option_dti,option_inq_last_6mths,option_out_prncp,option_int_rate,option_annual_inc,option_revol_util]))
            base = scores_dict['Intercept']

            base += scores_dict[opciones[option_purpose]]
            base += scores_dict[opciones[option_verification_status]]
            base += scores_dict[opciones[option_home_ownership]]
            base += scores_dict[opciones[option_term]]
            base += scores_dict[opciones[option_grade]]

            ###Suma option_tot_cur_bal
            if int(option_tot_cur_bal) <= 100000:
                base += scores_dict['tot_cur_bal:0-100000']
            elif int(option_tot_cur_bal) <= 200000:
                base += scores_dict['tot_cur_bal:100000-200000']
            elif int(option_tot_cur_bal) <= 300000:
                base += scores_dict['tot_cur_bal:200000-300000']
            elif int(option_tot_cur_bal) <= 400000:
                base += scores_dict['tot_cur_bal:300000-400000']
            else:
                base += scores_dict['tot_cur_bal:400000-500000']
            
            ###Suma option_dti
            if option_dti == 'NA':      #por si no conoce su dti
                base+=0
            elif float(option_dti) <= 1.6:
                base += scores_dict['dti:<=1.6']
            elif float(option_dti) <= 5.599:
                base += scores_dict['dti:1.6-5.599']
            elif float(option_dti) <= 10.397:
                base += scores_dict['dti:5.599-10.397']
            elif float(option_dti) <= 15.196:
                base += scores_dict['dti:10.397-15.196']
            elif float(option_dti) <= 19.195:
                base += scores_dict['dti:15.196-19.195']
            elif float(option_dti) <= 24.794:
                base += scores_dict['dti:19.195-24.794']
            elif float(option_dti) <= 35.191:
                base += scores_dict['dti:24.794-35.191']
            else:
                base += scores_dict['dti:>35.191']
            
            ###Suma option_inq_last_6mths
            if int(option_inq_last_6mths) == 0:
                base += scores_dict['inq_last_6mths:0']
            elif int(option_inq_last_6mths) <= 2:
                base += scores_dict['inq_last_6mths:1-2']
            elif int(option_inq_last_6mths) <= 4:
                base += scores_dict['inq_last_6mths:3-4']
            elif int(option_inq_last_6mths) >= 5:
                base += scores_dict['inq_last_6mths:>4']
            else:
                base += scores_dict['inq_last_6mths:missing']
            
            ###Suma option_out_prncp
            if float(option_out_prncp.strip(',')) <= 1286:
                base += scores_dict['out_prncp:<1,286']
            elif float(option_out_prncp.strip(',')) <= 6432:
                base += scores_dict['out_prncp:1,286-6,432']
            elif float(option_out_prncp.strip(',')) <= 9005:
                base += scores_dict['out_prncp:6,432-9,005']
            elif float(option_out_prncp.strip(',')) <= 10291:
                base += scores_dict['out_prncp:9,005-10,291']
            elif float(option_out_prncp.strip(',')) <= 15437:
                base += scores_dict['out_prncp:10,291-15,437']
            else:
                base += scores_dict['out_prncp:>15,437']

            ###Suma option_int_rate
            if float(option_int_rate) < 7.071:
                base += scores_dict['int_rate:<7.071']
            elif float(option_int_rate) < 10.374:
                base += scores_dict['int_rate:7.071-10.374']
            elif float(option_int_rate) < 13.676:
                base += scores_dict['int_rate:10.374-13.676']
            elif float(option_int_rate) < 15.74:
                base += scores_dict['int_rate:13.676-15.74']
            elif float(option_int_rate) < 20.281:
                base += scores_dict['int_rate:15.74-20.281']
            else:
                base += scores_dict['int_rate:>20.281']

            ###Suma option_annual_inc:
            if float(option_annual_inc.strip(',')) <= 28555:
                base += scores_dict['annual_inc:<28,555']
            elif float(option_annual_inc.strip(',')) <= 37440:
                base += scores_dict['annual_inc:28,555-37,440']
            elif float(option_annual_inc.strip(',')) <= 61137:
                base += scores_dict['annual_inc:37,440-61,137']
            elif float(option_annual_inc.strip(',')) <= 81872:
                base += scores_dict['annual_inc:61,137-81,872']
            elif float(option_annual_inc.strip(',')) <= 102606:
                base += scores_dict['annual_inc:81,872-102,606']
            elif float(option_annual_inc.strip(',')) <= 120379:
                base += scores_dict['annual_inc:102,606-120,379']
            elif float(option_annual_inc.strip(',')) <= 150000:
                base += scores_dict['annual_inc:120,379-150,000']
            else:
                base += scores_dict['annual_inc:>150K']
            
            ###Suma option_revol_util
            if float(option_revol_util) < 0.1:
                base += scores_dict['revol_util:<0.1']
            elif float(option_revol_util) < 0.2:
                base += scores_dict['revol_util:0.1-0.2']
            elif float(option_revol_util) < 0.3:
                base += scores_dict['revol_util:0.2-0.3']
            elif float(option_revol_util) < 0.4:
                base += scores_dict['revol_util:0.3-0.4']
            elif float(option_revol_util) < 0.5:
                base += scores_dict['revol_util:0.4-0.5']
            elif float(option_revol_util) < 0.6:
                base += scores_dict['revol_util:0.5-0.6']
            elif float(option_revol_util) < 0.7:
                base += scores_dict['revol_util:0.6-0.7']
            elif float(option_revol_util) < 0.8:
                base += scores_dict['revol_util:0.7-0.8']
            elif float(option_revol_util) < 0.9:
                base += scores_dict['revol_util:0.8-0.9']
            elif float(option_revol_util) < 1:
                base += scores_dict['revol_util:0.9-1.0']
            else:
                base += scores_dict['revol_util:>1.0']

            st.markdown("### Su puntaje de crédito es: "+ str(base) )
            
            percentile = 0
            for i in range(0,101):
                puntaje_credito = stats.scoreatpercentile(puntaje['0'].tolist(), i)
                percentile += 1
                if int(base) <= puntaje_credito:
                    break
            percentil_debajo = 1 - percentile        
            
            if(300<=int(base) and int(base)<= 499):
                st.markdown("#### Su puntaje de crédito es bajo \U0001f534")
                st.markdown("- Con este puntaje no puedes sacar un crédito en el banco.")
                st.markdown("- Usted se en cuentra en el percentil "+ str(percentile) + ". Esto con respecto a la población quiere decir que usted tiene un puntaje mayor al  "+ str(percentile) + '% ' + 'de las otras personas y menor al ' + str(100-percentile) + '% .' )
                st.markdown("#### Algunas recomendaciones para subir el puntaje:")
                st.markdown("- Pague sus cuentas a tiempo.")
                st.markdown("- Mantenga sus saldos bajos: no pidas créditos que estén tan cerca a tu límite máximo de crédito.")
                st.markdown("- Tenga una variedad de préstamos: los prestamistas le gustan ver que puedes manejar varios prestamos a la vez.")
                st.markdown("- Piensa antes de solicitar un crédito.")
                

            if(500<=int(base) and int(base)<= 568):
                st.markdown("#### Su puntaje de crédito es justo \U0001f7e1")
                st.markdown("- Esto quiere decir que no es muy probable que el banco te dé el crédito. Te lo puede dar en casos muy específicos.")
                st.markdown("- Usted se en cuentra en el percentil "+ str(percentile) + ". Esto con respecto a la población quiere decir que usted tiene un puntaje mayor al  "+ str(percentile) + '% ' + 'de las otras personas y menor al ' + str(100-percentile) + '% .' )
                st.markdown("#### Algunas recomendaciones para subir el puntaje:")
                st.markdown("- Pague sus cuentas a tiempo.")
                st.markdown("- Mantenga sus saldos bajos: no pidas créditos que estén tan cerca a tu límite máximo de crédito.")
                st.markdown("- Tenga una variedad de préstamos: los prestamistas le gustan ver que puedes manejar varios prestamos a la vez.")
                st.markdown("- Piensa antes de solicitar un crédito.")


            if(568<int(base) and int(base)<= 633):
                st.markdown("#### Su puntaje de crédito es buena \U0001f7e2")
                st.markdown("- Estas en una situación buena. En casos muy puntuales el banco no te va a dar el crédito.")
                st.markdown("- Usted se en cuentra en el percentil "+ str(percentile) + ". Esto con respecto a la población quiere decir que usted tiene un puntaje mayor al  "+ str(percentile) + '% ' + 'de las otras personas y menor al ' + str(100-percentile) + '% .' )
                st.markdown("#### Algunas recomendaciones para tu puntaje:")
                st.markdown("- Sigue manteniendo los buenos hábitos financieros que llevas.")
                st.markdown("- Puede que se te pase la fecha de pagos de algunos créditos. Cumple a fecha con todos los créditos que tengas.")
                st.markdown("- Piensa antes de solicitar un crédito.")
            
            if(633<int(base) and int(base)<= 850):
                st.markdown("#### Su puntaje de crédito es excelente  \u2714\uFE0F")
                st.markdown("- Usted se en cuentra en el percentil "+ str(percentile) + ". Esto con respecto a la población quiere decir que usted tiene un puntaje mayor al  "+ str(percentile) + '% ' + 'de las otras personas y menor al ' + str(100-percentile) + '%.')
                st.markdown('- Felicitaciones por tus hábitos financieros, los bancos estarán encantados de prestarte plata.')
