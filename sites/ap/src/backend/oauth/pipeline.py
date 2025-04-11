def save_profile(backend, user, response, *args, **kwargs):
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
