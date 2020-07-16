from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/'):
    actual_decorator = user_passes_test(
        lambda u: u.is_administrator,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def seller_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and (u.is_administrator or u.is_seller),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def retailer_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/'):
    actual_decorator = user_passes_test(
        lambda u: u.is_retailer,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def wholesaler_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/'):
    actual_decorator = user_passes_test(
        lambda u: u.is_wholesaler,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
