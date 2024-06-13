from templated_mail.mail import BaseEmailMessage
from os import path
from dineqr.settings import ABS_PATH

class ForgotPasswordOtpMail(BaseEmailMessage):
    template_name = path.join(ABS_PATH, "templates/emails/forgot_password_otp_mail.html")
    def get_context_data(self):
        context = super().get_context_data()
        return context
    
    

class ForgotPasswordSuccessfulMail(BaseEmailMessage):
    template_name = path.join(ABS_PATH, "templates/emails/forgot_password_successful_email.html")
    def get_context_data(self):
        context = super().get_context_data()
        return context
    

class SendStaffInviteMail(BaseEmailMessage):
    template_name = path.join(ABS_PATH, "templates/emails/staff_invite_email.html")
    def get_context_data(self):
        context = super().get_context_data()
        return context