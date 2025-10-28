from typing import TypedDict, Union, Optional, List, Dict
from langgraph.graph import StateGraph, END
import pdb, random, agent_lib

class AgentState(TypedDict):
    message : str
    payload : Dict
    issues : List[str]
    res : Dict	
	
def issue_evaluater(state: AgentState) -> AgentState:
	"""Node to evaluate all the issues and populate the issue tracker"""
	print(state)
	# pdb.set_trace()
	print(state["payload"]["custID"], state["payload"]["first_name"])
	state['res'] = {
		"delivery_delay_email" : False,
		"delivery_esc" : False,
		"refund_delay_email" : False,
		"refund_esc" : False,
			  }
	
	state["issues"] = []
	if (state["payload"]["Delivery_status"] == 'pending') and (state["payload"]["Delivery_AI_cust_email"]!= True) and (state["payload"]["Delivery_delta"] <0):
		state["issues"].append('delivery')
		

	if (state["payload"]["Refund_status"] == 'pending') and (state["payload"]["Refund_AI_cust_email"]!= True) and (state["payload"]["Refund_delta"] <0):
		state["issues"].append('refund')
	
	print("issues found are : ",state['issues'])
	return state


		
def _refund_handle(state: AgentState) -> AgentState:
	"""Simple node that sends email to the customer informing on delay on refun"""
	print("refund handled - Sent email to", state["payload"]["email"])
	
	email_body = agent_lib.write_email('refund')
	state["issues"].remove('refund')
	state['res'].update({
		"refund_delay_email" : email_body,
		"refund_esc" : True,
			  })
	return state


def _delivery_handle(state: AgentState) -> AgentState:
	"""Simple node that sends email to the customer informing on delay on orders"""
	print("delivery handled - Sent email to", state["payload"]["email"])
	email_body = agent_lib.write_email('delivery')
	shipping_status = agent_lib.latest_shipping_status()
	state["issues"].remove('delivery')
	state['res'].update({
		"delivery_delay_email" : email_body,
		"delivery_esc" : True
			  })
	return state

def router(state: AgentState) -> str:
	if 'refund' in state["issues"]:
		return "refund_handle"
	elif 'delivery' in state["issues"]:
		return "delivery_handle"
	else: 
		return 'continue'

def get_agent():
    graph = StateGraph(AgentState)
    graph.add_node("issue_evaluater", issue_evaluater)
    graph.add_node("router", lambda state: state)
    graph.add_node("_refund_handle", _refund_handle)
    graph.add_node("_delivery_handle", _delivery_handle)

    graph.add_edge('issue_evaluater', 'router')
    graph.add_conditional_edges("router", router,
                                    {
                                        "refund_handle" : "_refund_handle",
                                        "delivery_handle" : "_delivery_handle",
                                        "continue" : END
                                    }
                                )
    graph.add_edge('_refund_handle', 'router')
    graph.add_edge('_delivery_handle', 'router')


    graph.set_entry_point("issue_evaluater")
	
    app = graph.compile()
	
    return app

