"""
This file is used to implement the necessary methods that must run
on the SSO pipeline of the package `social-auth-app-django`.
"""


# pylint: disable=unused-argument
def save_profile(backend, user, response, *args, **kwargs):
    """
    The method used to execute the user profile save.

    Args:
        `backend`: The current backend instance.
        `user`: The user instance (or None if it
        wasn't created or retrieved from the database yet).
        `response`: The server user-details response, it depends
        on the protocol in use (and sometimes the provider
        implementation of such protocol), but usually it's just
        a dict with the user profile details from the provider.
        Lots of information related to the user is provided here,
        sometimes the scope will increase the amount of information
        in this response on OAuth providers.
    """

    name = (
        response.get("name")
        or response.get("full_name")
        or response.get("preferred_username")
    )
    if name:
        user.first_name = name.split(" ")[0]
        if len(name.split(" ")) > 1:
            user.last_name = name.split(" ")[-1]

    username = response.get("username")
    if name:
        user.username = username.split(" ")[0]

    user.save()
