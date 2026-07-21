def is_trip_planning_request(question):

    keywords = [

        "plan",
        "itinerary",
        "trip",
        "travel plan",
        "schedule",
        "days",
        "day trip",
        "vacation",
        "holiday"

    ]


    question = question.lower()


    for word in keywords:

        if word in question:
            return True


    return False