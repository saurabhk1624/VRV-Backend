import uuid6
from django.db import models

from common.models import ActionNum, BaseApproveModel, BaseModel, Dropdown
from no_auth.models import User


class UploadFile(BaseModel):
    image = models.FileField(upload_to="grievances")


class Ticket(BaseModel):
    grievance = models.ForeignKey(
        Dropdown,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="issue_grievance",
    )
    hostel = models.ForeignKey(
        Dropdown, on_delete=models.DO_NOTHING, null=True, related_name="issue_hostel"
    )
    image = models.ForeignKey(
        UploadFile, on_delete=models.DO_NOTHING, null=True, related_name="issue_image"
    )
    issue = models.TextField()
    closed_on = models.DateTimeField(null=True, blank=False)
    closed_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, related_name="issue_closer"
    )


class TicketApproval(BaseApproveModel):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.DO_NOTHING, null=True, related_name="flow_ticket"
    )
    remark = models.TextField(null=True)
    action = models.IntegerField(choices=ActionNum.choices(), default=ActionNum.PENDING)
