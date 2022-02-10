from typing import Optional

from django.contrib import admin
from django.http import HttpRequest
from django.urls import path

from swap_user.views import CheckOTPView, GetOTPView


class EmailOTPUserSite(admin.AdminSite):
    def get_urls(self):
        """
        Here we are adding a new route /check-otp/ to the parent routes.
        """

        default_urls = super().get_urls()

        custom_urls = [
            path("check-otp/", self.check_otp, name="check-otp"),
        ]

        # Order is matter
        urls = custom_urls + default_urls

        return urls

    def login(self, request: HttpRequest, extra_context: Optional[dict] = None):
        """
        At this view handler we are registering custom `GetOTPView`
        which sends an OTP to user via provided sender.
        """

        request.current_app = self.name
        context = self._get_context(request, extra_context)

        return GetOTPView.as_view(**context)(request)

    def check_otp(self, request: HttpRequest, extra_context: Optional[dict] = None):
        """
        This view checks received OTP with OTP cached at backend side.
        """

        request.current_app = self.name
        context = self._get_context(request, extra_context)

        return CheckOTPView.as_view(**context)(request)

    def _get_context(self, request, extra_context: dict) -> dict:
        """
        Let's create a context for view
        Ref - django.contrib.admin.sites#login
        """

        context = {
            **self.each_context(request),
            **(extra_context or {}),
        }
        defaults = {
            "extra_context": context,
        }

        return defaults
