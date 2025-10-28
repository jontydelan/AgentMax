## create data
import pandas as pd
import random
from datetime import datetime, timedelta
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

class llm_models():
    def __init__(self):
        load_dotenv()
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.AGENT_API_KEY = os.getenv("AGENT_API_KEY")

    def get_groq(self,model_name="llama-3.1-8b-instant",**kwargs):
        llm = ChatGroq(model=model_name,**kwargs)
        return llm

def generate_delay_dataset(n):
    first_names = ["Vihaan", "Aarav", "Ishaan", "Riya", "Anaya", "Meera", "Kabir", "Tara", "Aditya", "Sneha"]
    last_names = ["Sharma", "Patel", "Reddy", "Mehta", "Kapoor", "Iyer", "Khan", "Desai", "Verma", "Joshi"]
    carriers = ['BlueX', 'ShipQuick', 'RapidExpress', 'LocalCouriers']
    delivery_statuses = [None,'pending', 'Delivered']
    refund_statuses = [None,'pending', 'Complete']

    delivery_start = datetime.strptime("23-10-2025", "%d-%m-%Y")
    delivery_end = datetime.strptime("02-11-2025", "%d-%m-%Y")
    refund_start = delivery_start
    refund_end = delivery_end

    data = []
    for i in range(n):
        first = random.choice(first_names)
        last = random.choice(last_names)
        email = f"{first.lower()}.{last.lower()}{i}@example.com"
        cust_id = f"C{100000 + i}"
        tracking_id = f"O{300000 + i}"
        carrier = random.choice(carriers)
        delivery_eta = (delivery_start + timedelta(days=random.randint(0, (delivery_end - delivery_start).days))).strftime("%d-%b-%Y")
        delivery_status = random.choice(delivery_statuses)
        refund_eta = (refund_start + timedelta(days=random.randint(0, (refund_end - refund_start).days))).strftime("%d-%b-%Y")
        refund_status = (None if delivery_status=='pending' else random.choice(refund_statuses))

        row = {
            'custID': cust_id,
            'first_name': first,
            'last_name': last,
            'email': email,
            'Tracking ID': tracking_id,
            'Carrier': carrier,
            'Delivery_ETA': delivery_eta,
            'Delivery_status': delivery_status,
            'Refund_ETA': refund_eta,
            'Refund_status': refund_status,
            # Dummy AI columns
            'Delivery_AI_cust_email': None,
            'Delivery_AI_escalation': None,
            'Delivery_AI_Logistic_email': None,
            'Refund_AI_cust_email': None,
            'Refund_AI_escalation': None,
            'Refund_AI_Logistic_email': None
        }
        data.append(row)

    return pd.DataFrame(data)

def get_delivery_refund_data(n, reuse=True):
    try:
        assert reuse, 'Recreating the data as reuse is False'
        df = pd.read_csv(f'./Data/get_delivery_refund_data{n}.csv')

    except:
        print('recreaing..')
        df = generate_delay_dataset(n)
        # Convert Delivery_ETA to datetime format
        df["Delivery_ETA"] = pd.to_datetime(df["Delivery_ETA"], format="%d-%b-%Y")
        df["Refund_ETA"] = pd.to_datetime(df["Refund_ETA"], format="%d-%b-%Y")

        df["Delivery_delta"] = (df["Delivery_ETA"]- datetime.today()).dt.days
        df["Refund_delta"] = (df["Refund_ETA"] - datetime.today()).dt.days
        
        df.to_csv(f'./Data/get_delivery_refund_data{n}.csv')

    return {'total_records':df.__len__(),
            'delivery_delay':df[(df.Delivery_delta<0) & (df.Delivery_status=='pending')].__len__(),
            'delivery_delay':df[(df.Refund_delta<0) & (df.Refund_status =='pending')].__len__(),
            'data':df}

def generate_transaction_data(n):
    random_state = random.randint(0,100)
    names = ["Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah", "Ian", "Julia"]
    us_surnames = ["Smith", "Johnson", "Williams", "Brown", "Jones",    "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]
    delivery_statuses = ["Delivered", "Delayed"]
    refund_statuses = ["None", "Refund Pending", "Refund Completed"]

    data = []

    for i in range(n):
        name = random.choice(names)+"."+ random.choice(us_surnames)
        order_id = f"ORD{1000 + i}"
        email = f"{name.lower()}@gmail.com"
        delivery_status = random.choice(delivery_statuses)
        delivery_delay_days = random.randint(0, 10)
        delivery_date = (datetime.today() - timedelta(days=delivery_delay_days)).strftime("%Y-%m-%d")

        if delivery_status == "Delayed":
            refund_status = "None"
        else:
            refund_status = random.choice(refund_statuses)

        refund_init_date = None
        refund_ai_agent_reachout = False

        if refund_status != "None":
            refund_delay_days = random.randint(1, 10)
            refund_init_date = (datetime.today() - timedelta(days=refund_delay_days)).strftime("%Y-%m-%d")
            refund_ai_agent_reachout = random.choice([True, False])

        delivery_ai_agent_reachout = delivery_status == "Delayed" and random.choice([True, False])

        data.append({
            "order_id": order_id,
            "customer_name": name,
            "email": email,
            "delivery_status": delivery_status,
            "delivery_date": delivery_date,
            "refund_status": refund_status,
            "refund_init_date": refund_init_date,
            "refund_ai_agent_reachout": refund_ai_agent_reachout,
            "delivery_ai_agent_reachout": delivery_ai_agent_reachout
        })

    return pd.DataFrame(data)