import streamlit as st
import requests
import io
import pandas as pd
from json import loads

def payment_calculator(r,P,N):
    
    # r is the annual interest rate
    # P is the principal
    # N is the loan's term

    r = r/100
    
    r_m = r/12
    
    c = (r_m * P)/(1-(1+r_m)**(-N))
    
    return c


def interest_calculator(c,r,P,N):
    
    # c is the monthly payment from payment calculator
    # r is the annual interest rate
    # P is the principal
    # N month for interest calculation. Note this is different from the N in payment calculator 

    r = r/100
    
    r_m = r/12
    
    i = (P*r_m-c)*((1+r_m)**N-1)/r_m + c*N
    
    return i

#%%
#==============================================================================
# Tab 1 Commission
#==============================================================================

def tab1():
  price = st.number_input("Enter Purchase Price")

  total_commission = round(7000 + (price-100000)*0.02, 2)

  total_commission_percentage = round((total_commission/price)*100, 3)

  buy_commission = round(3220+0.0115*(price-100000), 2)

  buy_commission_percentage = round((buy_commission / price)*100, 3)

  listing_commission = round(3780 + 0.0135*(price-100000),2)
  
  listing_commission_percentage = round((listing_commission / price)*100, 3)

  st.write("佣金总数： {}，占成交价的{}%".format(total_commission, total_commission_percentage))

  st.write("买方佣金总数： {}，占成交价的{}%".format(buy_commission, buy_commission_percentage))
  
  st.write("卖方佣金总数： {}，占成交价的{}%".format(listing_commission, listing_commission_percentage))


  
  

#%%
#==============================================================================
# Tab 2 Mortgage
#==============================================================================

def tab2():

  
  P = st.number_input("Enter Loan Amount")
  r = st.number_input("Enter Effective Annual Interest Rate in %")
  N = st.number_input("Enter Amortization Period in Month")

  c = round(payment_calculator(r,P,N),2)

  st.title("To Calculate Cumulative Interests")

  T = st.number_input("Enter Interest Period in Month")

  i = round(interest_calculator(c, r, P, T),2)

  st.markdown("Monthly Payment is {}".format(c))

  st.markdown("Cumulative Interests for {} Months Are {}".format(T, i))



#%%
#==============================================================================
# Tab 3 Bond
#==============================================================================

def tab3():
    
    url = "https://www.bankofcanada.ca/valet/observations/group/bond_yields_all/csv"

    text = requests.get(url).text[1170:]

    df = pd.read_csv(io.StringIO(text), sep=",")

    # plotly setup 3 Month Year Treasury
    fig_3m = px.line(df, x=df['DATE'], y=['DTB3', 'DGS10'])
    fig_3m.update_xaxes(showgrid=False, gridwidth=1, gridcolor='rgba(0,0,255,0.1)')
    fig_3m.update_yaxes(showgrid=False, gridwidth=1, gridcolor='rgba(0,0,255,0.1)')
    
    fig_3m = bgLevels(df=df, fig = fig_3m, variable = 'USRECDM', level = 0.5, mode = 'above',
                   fillcolor = 'rgba(100,100,100,0.2)', layer = 'below')
      

  
 

    



#==============================================================================
# Main body
#==============================================================================

def run():
    
    
    
    # Add a radio box
    select_tab = st.sidebar.radio("Select tab", ['佣金', '贷款'])

    # Show the selected tab
    if select_tab == '佣金':
        tab1()
    elif select_tab == '贷款':
        tab2()
   
        
if __name__ == "__main__":
    run()   
