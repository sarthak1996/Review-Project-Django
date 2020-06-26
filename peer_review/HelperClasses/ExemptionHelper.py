from peer_review.models import Exemption
from datetime import datetime
from peer_review.HelperClasses import PrintObjs

def create_exemption_row(review,exemption_for,exemption_explanation,user,request):
	exemption_obj=Exemption(review=review,
							exemption_for=exemption_for,
							exemption_explanation=exemption_explanation,
							created_by=user,
							last_update_by=user,
							creation_date=datetime.now()
							)
	exemption_obj.save()
	PrintObjs.print_exemption_obj(exemption_obj,request.user)
