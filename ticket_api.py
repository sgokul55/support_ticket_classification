from flask import Flask,request,jsonify
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS, cross_origin

import ticket_db
import scheduler
import prepare_model

app = Flask(__name__)
api = Api(app)
CORS(app)
# train the classifier-1 
# this is responsible for categorizing the ticket - DevOps / Routing ticket
prepare_model.train_classifier_1()
prepare_model.train_classifier_dt()
prepare_model.train_classifier_rt()
prepare_model.train_classifier_sub_category()
# initialize scheduler
# this is responsible for reading DB evey 10 secs and feed those to classifiers
#scheduler.init_scheduler()


# Microservices payload 
parser = reqparse.RequestParser()
parser.add_argument('page')
parser.add_argument('incident_id')

class Ticket(Resource):
    def get(self):
        page_type = parser.parse_args()
        result = []
        page = page_type['page']
        if page == 'home_page':
            result = ticket_db.get_home_page_details()
        elif page == 'dt_page':
            result = ticket_db.get_open_classified_tickets('DT')
        elif page == 'rt_page':
            result = ticket_db.get_open_classified_tickets('RT')
        elif page == 'others':
            result = ticket_db.get_other_tickets('others')
        elif page == 'incident_details':
            incident_id = page_type['incident_id']
            result = ticket_db.get_ticket_info_by_incident(incident_id)
        return result
    def post(self):
        tickets = request.json
        are_added = True
        for ticket in tickets:
            try:
                if ticket['category'] != 'others':
                    data = ticket
                    data['is_classified'] = False
                    ticket_db.add_ticket(data)
                else:
                    data = ticket
                    data['is_classified'] = True
                    ticket_db.add_ticket(data)
            except Exception as e:
                are_added = False
                print(e)
            finally:
                pass
        return {"status" : are_added}
api.add_resource(Ticket, '/')

if __name__ == '__main__':
    app.run(host='10.52.231.101', port=5000,debug=True)