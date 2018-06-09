import  requests
import jose
from jose.jwt import get_unverified_claims

s = requests.session()


class Iyo(object):
    def verify(self, jwt):
        try:
            claims = get_unverified_claims(jwt)
        except jose.exceptions.JWTError:
            return

        username = claims.get("globalid", None) or claims.get("username", None)

        if username is None:
            return

        url = "https://itsyou.online/api/users/{}/info".format(username)

        response = s.get(
            url,
            headers={
                'Authorization': 'bearer {}'.format(jwt)
            }
        )

        info = response.json()
        emails = [record['emailaddress'] for record in info['emailaddresses']]

        if not emails:
            return

        return {
            'username': username,
            'email': emails[0]
        }

iyo = Iyo()