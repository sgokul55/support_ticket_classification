import time
import threading
import ticket_db
import prepare_model

def init_scheduler():
    t = threading.Timer(30, function=monitor_open_tickets)
    t.daemon = True
    t.start()

def monitor_open_tickets(): 
    print('Scheduled Task to read New tickets')
    open_tickets = ticket_db.get_open_not_classified_tickets()
    print(open_tickets)
    for cur_ticket in open_tickets:
        input_data = {}
        input_data['incident_description'] = [cur_ticket['incident_description'] ]
        input_data['additional_description'] = [cur_ticket['additional_description']]

        cur_classification = prepare_model.get_prediction(input_data)
        # updates the ticket with DT / RT
        ticket_db.update_ticket(cur_ticket['incident_id'],cur_classification)
    t = threading.Timer(30, function=monitor_open_tickets)
    t.daemon = True
    t.start() 

if __name__ == '__main__':
    #init_scheduler()
    #time.sleep(15)
    monitor_open_tickets()