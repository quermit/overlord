# -*- coding: utf-8 -*-

import datetime


def format_datetime(handler, value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)


def format_duration(handler, delta):
    seconds = delta % 60
    minutes = (delta / 60) % 60
    hours = (delta / 3600) % 60
    days = (delta / 86400)

    amount = []

    if days > 0:
        amount.append("%sd" % days)
    if hours > 0:
        amount.append("%sh" % hours)
    if minutes > 0:
        amount.append("%sm" % minutes)
    if seconds > 0:
        amount.append("%ss" % seconds)
    if not amount:
        amount = ["0s"]

    return " ".join(amount)
