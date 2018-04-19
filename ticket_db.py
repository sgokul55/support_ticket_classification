from pymongo import MongoClient
import time
# if no argument then it defaults to localhost interface on port 27017
client = MongoClient()
db = client.ticket

# receives the data
def add_ticket(data):
	db.TicketCollection.insert({"incident_id": data['incident_id'],
		"status": data['status'],
		"category": data['category'],
		"system_id": data['system_id'], 
		"client":  data['client'], 
		"group_id": data['group_id'],
		 "incident_description": data['incident_description'],
		 "additional_description" : data['additional_description'],
		 "is_classified" : data['is_classified']
		 })
def update_ticket(incident_id, classification):
	try:
		db.TicketCollection.update({"incident_id":incident_id },{'$set':{'is_classified':True}})
		db.TicketCollection.update({"incident_id":incident_id },{'$set':{'classification':classification['classification']}})
		db.TicketCollection.update({"incident_id":incident_id },{'$set':{'proposed_solution':classification['proposed_solution']}})
		db.TicketCollection.update({"incident_id":incident_id },{'$set':{'sub_category':classification['sub_category']}})
	except Exception as e:
		print(e)
	finally:
		pass
	
def get_home_page_details():
	data = {
	"dev_ops": {
		"total": 10

	},
	"routing": {
		"total": 10
	},
	"others": {
		"total": 10
	},

	"bar_chart": [{
		"FilterDef": "Jan 2017",
		"total_incidents": "30",
		"classified_incidents": "15",
		"non_classified_incidents": "15"
	},{
		"FilterDef": "Feb 2017",
		"total_incidents": "50",
		"classified_incidents": "40",
		"non_classified_incidents": "10"
	},{
		"FilterDef": "Mar 2017",
		"total_incidents": "45",
		"classified_incidents": "25",
		"non_classified_incidents": "20"
	},{
		"FilterDef": "Apr 2017",
		"total_incidents": "35",
		"classified_incidents": "20",
		"non_classified_incidents": "15"
	},{
		"FilterDef": "May 2017",
		"total_incidents": "50",
		"classified_incidents": "45",
		"non_classified_incidents": "5"
	}, {
		"FilterDef": "Jun 2017",
		"total_incidents": "60",
		"classified_incidents": "52",
		"non_classified_incidents": "8"
	}, {
		"FilterDef": "Jul 2017",
		"total_incidents": "17",
		"classified_incidents": "15",
		"non_classified_incidents": "2"
	}]
}
	data['dev_ops']['total'] = db.TicketCollection.find({"classification":"DT"}).count()
	data['routing']['total'] = db.TicketCollection.find({"classification":"RT"}).count()
	data['others']['total'] = db.TicketCollection.find({"category":"others"}).count()
	return data

def get_open_classified_tickets(classification):
	all_open_tickets = []
	cursor = db.TicketCollection.find({'is_classified': True, 'classification': classification},{"_id":0})
	for doc in cursor:
		all_open_tickets.append(doc)
	return all_open_tickets

def get_other_tickets(classification):
	all_open_tickets = []
	cursor = db.TicketCollection.find({'category':classification},{"_id":0})
	for doc in cursor:
		all_open_tickets.append(doc)
	return all_open_tickets

def get_ticket_info_by_incident(incident_id):
	all_open_tickets = []
	cursor = db.TicketCollection.find({'incident_id':incident_id},{"_id":0})
	for doc in cursor:
		all_open_tickets.append(doc)
	return all_open_tickets

def get_open_not_classified_tickets():
	all_open_tickets = []
	cursor = db.TicketCollection.find({'status': 'NEW','is_classified':False},{"_id":0})
	for doc in cursor:
		all_open_tickets.append(doc)
	return all_open_tickets

def get_proposed_solution(classification, solution):
	proposed_solution = ''
	cursor = db.SolutionCollection.find({'classification': classification,'tag':solution})
	for doc in cursor:
		proposed_solution = doc['SOLUTION']
	return proposed_solution

if __name__ == '__main__':

	print(get_open_classified_tickets('others'))
	# cursor = db.TicketCollection.find({'client': '710'})
	# for doc in cursor:
	# 	print(doc['source_of_incident'])