from faker import Faker



def get_fake_profiles(count=10):
    fake = Faker()
    user_data = []
    for _ in range(count):
        profile = fake.profile()
        data = {
            "username": profile.get("username"),
            "email" : profile.get("mail"),
            "is_active": True
        }

        if 'name' in profile:
            data["first_name"] = profile.get("name").split(" ")[0]
            data["last_name"] = profile.get("name").split(" ")[1]

        user_data.append(data)
    return user_data
