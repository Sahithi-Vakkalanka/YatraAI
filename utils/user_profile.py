import json


user_profiles = {}



DEFAULT_PROFILE = {

    "budget": None,

    "duration": None,

    "travel_style": None,

    "interests": [],

    "food_preference": None,

    "traveler_type": None,

    "preferred_season": None

}



def get_user_profile(session_id):


    if session_id not in user_profiles:

        user_profiles[session_id] = (
            DEFAULT_PROFILE.copy()
        )


    return user_profiles[session_id]





def update_user_profile(
        session_id,
        new_data
):


    profile = get_user_profile(
        session_id
    )


    for key,value in new_data.items():


        if value is None:
            continue



        if key == "interests":


            for item in value:


                if item not in profile["interests"]:

                    profile["interests"].append(
                        item
                    )



        else:

            profile[key] = value



    user_profiles[session_id] = profile


    return profile





def format_user_profile(session_id):


    profile=get_user_profile(
        session_id
    )


    return json.dumps(
        profile,
        indent=2
    )