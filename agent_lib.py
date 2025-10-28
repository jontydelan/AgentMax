import random

def write_email(_type):
		if _type == "delivery":
			return """Subject: Update on Delayed Delivery: Order O300000

			Dear Ishaan,

			I am writing to you regarding the status of your recent order, O300000, which was shipped via ShipQuick. Unfortunately, we have encountered a delay in the delivery of your package. I want to start by apologizing for the inconvenience this has caused and assure you that we are taking immediate action to resolve the issue.

			Our team has escalated this matter to the logistics department, and we are working closely with ShipQuick to expedite the delivery process. We understand the importance of timely delivery and are committed to ensuring that your package reaches you as soon as possible.

			I would like to provide you with a revised estimated delivery date, which will be communicated to you once it becomes available. In the meantime, if you have any questions or concerns, please do not hesitate to contact us. We are here to support you and appreciate your patience during this time.

			Order details:

			- Order ID: O300000
			- Carrier: ShipQuick
			- Tracking Number: [insert tracking number, if available]

			We value your business and appreciate your understanding in this matter. We will keep you updated on any developments and will notify you as soon as your package is on its way.

			Thank you for your patience and cooperation. If you have any questions or require further assistance, please do not hesitate to contact us.

			Best regards,
			AgenMax e-comm Team"""
		
		elif _type == "refund":
			return """Subject: Update on refund

			Dear Ishaan,

			I am writing to you regarding the status of your recent order, O300000, which was shipped via ShipQuick. Unfortunately, we have encountered a delay in the delivery of your package. I want to start by apologizing for the inconvenience this has caused and assure you that we are taking immediate action to resolve the issue.

			Our team has escalated this matter to the logistics department, and we are working closely with ShipQuick to expedite the delivery process. We understand the importance of timely delivery and are committed to ensuring that your package reaches you as soon as possible.

			I would like to provide you with a revised estimated delivery date, which will be communicated to you once it becomes available. In the meantime, if you have any questions or concerns, please do not hesitate to contact us. We are here to support you and appreciate your patience during this time.

			Order details:

			- Order ID: O300000
			- Carrier: ShipQuick
			- Tracking Number: [insert tracking number, if available]

			We value your business and appreciate your understanding in this matter. We will keep you updated on any developments and will notify you as soon as your package is on its way.

			Thank you for your patience and cooperation. If you have any questions or require further assistance, please do not hesitate to contact us.

			Best regards,
			AgenMax e-comm Team"""

def latest_shipping_status():
	status =  random.choice(["In transit", "Reached nearest delivery Hub", "Out for delivery"])
	return status

def get_issue_info(data):
	data['refund_issue'] = (
		(data['Refund_status'] == 'pending') &
		(data['Refund_AI_cust_email'] != True) &
		(data['Refund_delta'] < 0)
	)
	data['delivery_issue'] = (
		(data['Delivery_status'] == 'pending') &
		(data['Delivery_AI_cust_email'] != True) &
		(data['Delivery_delta'] < 0)
	)

	return {
		'refund_issue': data['refund_issue'].sum(),
		'delivery_issue': data['delivery_issue'].sum()}