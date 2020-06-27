from peer_review.models import Approval
from peer_review.HelperClasses import StatusCodes,PrintObjs
from configurations.HelperClasses import LoggingHelper
import traceback
import datetime
class ApprovalHelper():
	@staticmethod
	def approve_review(review,user,request,approver_comment=None):
		latest_approval_row=ApprovalHelper.get_latest_approval_row(review,request.user)
		# raised_by = latest row state (since approved , preserve old state)
		# raised_to = latest row state (since approved, preserve old state)
		# created_by = user (to preserve history integrity)
		ApprovalHelper.__create_new_approval_row(review_obj=review,
								raised_by=latest_approval_row.raised_by,
								raised_to=latest_approval_row.raised_to,
								approval_outcome=StatusCodes.get_approved_status(),
								delegated=False,
								approver_comment=approver_comment,
								created_by=user,
								request=request)
	@staticmethod
	def get_latest_approval_row(review,request_user,raise_exception=True):
		latest_approval_row=review.approval_review_assoc.filter(latest=True).all()
		logger=LoggingHelper(request_user.username,__name__)
		PrintObjs.print_review_obj(review,request_user)
		if latest_approval_row.count()>1:
			logger.write('Multiple rows exists for approval',LoggingHelper.DEBUG)
			logger.write('Rows:',LoggingHelper.DEBUG)
			# all_latest_rows=review.approval_review_assoc.assoc.filter(latest=True).all()
			for row in latest_approval_row:
				PrintObjs.print_approval_obj(row,request.user) 
			if raise_exception:
				raise Exception('Multiple latest rows exists for approval')
		if latest_approval_row.count()<0:
			logger.write('No rows exists for approval',LoggingHelper.DEBUG)
			if raise_exception:
				raise Exception('No latest rows exists for approval')
		if latest_approval_row.count()==1:
			return latest_approval_row.first()
		else:
			if raise_exception:
				raise Exception('Error while fetching latest approval row.'+str(latest_approval_row.count()))

	@staticmethod
	def mark_rest_rows_as_not_latest(review,exclude,user):
		all_approval_rows=ApprovalHelper.get_all_approval_rows(review).exclude(pk=exclude.pk)
		all_approval_rows.update(latest=False)
		for apr in all_approval_rows:
			apr.save()

	@staticmethod
	def reject_review(review,user,request,approver_comment=None):
		latest_approval_row=ApprovalHelper.get_latest_approval_row(review,request.user)
		# raised_by = latest row state (since approved , preserve old state)
		# raised_to = latest row state (since approved, preserve old state)
		# created_by = user (to preserve history integrity)
		ApprovalHelper.__create_new_approval_row(review_obj=review,
								raised_by=latest_approval_row.raised_by,
								raised_to=latest_approval_row.raised_to,
								approval_outcome=StatusCodes.get_rejected_status(),
								delegated=False,
								approver_comment=approver_comment,
								created_by=user,
								request=request)

	@staticmethod
	def invalidate_review(review,user,request):
		latest_approval_row=ApprovalHelper.get_latest_approval_row(review,request.user)
		# raised_by = latest row state (since approved , preserve old state)
		# raised_to = latest row state (since approved, preserve old state)
		# created_by = user (to preserve history integrity)
		ApprovalHelper.__create_new_approval_row(review_obj=review,
								raised_by=latest_approval_row.raised_by,
								raised_to=latest_approval_row.raised_to,
								approval_outcome=StatusCodes.get_invalid_status(),
								delegated=False,
								approver_comment=None,
								created_by=user,
								request=request)
	@staticmethod
	def mark_review_pending(review,user,raised_to,request,comment=None):
		# latest_approval_row=ApprovalHelper.get_latest_approval_row(review)
		# raised_by = user (since pending mark action taken by user)
		# raised_to = raised to (since this method is only called if 
					# review is updated, we need to get raised_to 
					# from form entered by user)
		# created_by = user (to preserve history integrity)
		ApprovalHelper.__create_new_approval_row(review_obj=review,
								raised_by=user,
								raised_to=raised_to,
								approval_outcome=StatusCodes.get_pending_status(),
								delegated=False,
								approver_comment=comment,
								created_by=user,
								request=request)

	@staticmethod
	def __get_all_approval_rows(review):
		return review.approval_review_assoc.all()

	@staticmethod
	def delegate_approval(review,user,raised_to,request):
		latest_approval_row=ApprovalHelper.get_latest_approval_row(review,request.user)
		# raised_by = user (since delegation action taken by user)
		# raised_to = raised to ( passed as raised_to from delegation form)
		# created_by = user (to preserve history integrity)
		ApprovalHelper.__create_new_approval_row(review_obj=review,
								raised_by=user,
								raised_to=raised_to,
								approval_outcome=StatusCodes.get_pending_status(),
								delegated=True,
								approver_comment=None,
								created_by=user,
								request=request)

	@staticmethod
	def __mark_all_approval_rows_as_not_latest(all_approval_rows,user):
		all_approval_rows.update(latest=False)
		for apr in all_approval_rows:
			apr.save()

	@staticmethod
	def __create_new_approval_row(review_obj,raised_by,raised_to,approval_outcome,delegated,approver_comment,created_by,request):
		logger=LoggingHelper(request.user,__name__)
		logger.write('***Creating approval row****',LoggingHelper.DEBUG)
		PrintObjs.print_review_obj(review_obj,request.user)
		logger.write(raised_by.username,LoggingHelper.DEBUG)
		logger.write(raised_to.username,LoggingHelper.DEBUG)
		logger.write(str(approval_outcome),LoggingHelper.DEBUG)
		logger.write(str(delegated),LoggingHelper.DEBUG)
		logger.write(str(approver_comment),LoggingHelper.DEBUG)
		logger.write(created_by.username,LoggingHelper.DEBUG)
		logger.write('***Creating approval row****',LoggingHelper.DEBUG)
		ApprovalHelper.__mark_all_approval_rows_as_not_latest(ApprovalHelper.__get_all_approval_rows(review_obj),created_by)
		
		review_obj.approval_outcome=approval_outcome
		
		review_obj.save()
		approval_obj=Approval(review=review_obj,
									raised_by=raised_by,
									raised_to=raised_to,
									approval_outcome=approval_outcome,
									delegated=delegated,
									latest=True,
									approver_comment=approver_comment)
		PrintObjs.print_approval_obj(approval_obj,request.user)
		approval_obj.save()

