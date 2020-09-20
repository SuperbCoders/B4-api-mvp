from django.contrib.auth import get_user_model
from firebase_auth.authentication import FirebaseAuthentication as DefaultFirebaseAuthentication


User = get_user_model()


class FirebaseAuthentication(DefaultFirebaseAuthentication):
    """
    Token based authentication using firebase.

    Clients should authenticate by passing a Firebase ID token in the
    Authorizaiton header using Bearer scheme.
    """

    auth_header_prefix = 'JWT'

    def create_user_from_firebase(self, uid, firebase_user):
        fields = {self.uid_field: uid}

        user, created = User.objects.get_or_create(**fields, defaults={"email": firebase_user.email or ''})
        return user
