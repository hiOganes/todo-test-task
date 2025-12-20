from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


authentication_tags = ['Authentication']

registers_schema = {
    'tags': authentication_tags,
    'summary': 'This endpoint creates a new user',
    'description': '''Takes a set of user credentials, create new user and 
        returns an access and refresh JSON web token pair to prove the 
        authentication of those credentials.''',
    'responses': {201: TokenObtainPairSerializer},
}

custom_token_obtain_pair_schema = {
    'tags': authentication_tags,
    'summary': 'This endpoint returns access and refresh tokens'
}

custom_token_refresh_schema = {
    'tags': authentication_tags,
    'summary': 'This endpoint is updating access token'
}

custom_token_verify_schema = {
    'tags': authentication_tags,
    'summary': 'This endpoint checks the token'
}