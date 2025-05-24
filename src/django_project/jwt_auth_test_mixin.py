import jwt
import os
from datetime import datetime, timezone
from rest_framework.test import APIClient

class JWTAuthTestMixin:
  JWT_PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
MIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQDAHxdTxa68qsnh
PFl/Y2twIZbZLzwyyXFaPaZ9wnvt2eEh8YWWFS2iRc6jaI9Rii9RDuCTpSsiAjam
xqL6t2hJjsf8O5FfF/tFZur1BY5qMGs2Xs/YhO7WNVk/jTPOb8uyVe0A1haDXm3T
bosvIVpjVQik4hLgQ+C90VOLEbvc5U6d3xzBACkRMwypR7Shu3uUN7bJHCvsKXkK
sIkzcfgM6U6IH1GZaTkt9Vgrbz6EImkBBu1mp1DcuwulpsO6hgwFKvpujgVT62QO
ydit+VKMOBdWRT3XbR/wBaMWNa/PNcY5FoJ66Gi/AN0bfptVYP/5pG4BH8JomxJm
fPAqtPh1AgMBAAECgf9GiyQFnpCKtitqiL5UCC1q/upk1PNFsrHscLaxdrgKnfYM
gKKMeTpIW1mEpt/5EMRO/yd3Dy7HTgjDNCyj4rRoTgUgmL7ILAYXdbLQRToFw8Ga
NTYcSrNn9C7RJwfexS4GTYa4x+N8WS/6cpyosZZ+4rpJ0Lkdn87l4/bJGbnhYa6C
ni5K0RQU8c+kgCEREZGkfm33YSMyxqUafVUJDXdkG3UYBaek8rQoXGacRwe1Bn80
JBSf6T3AsOuQ/ywK79gISJoRry9CKUtEtyXP+lDrqkLFtJZo+kgw8q9X5PzKVhsZ
7cU9eCkxFyGtBGw73JJGmJ+31hPt599sGnLQocECgYEA5h0DEC2LHDHV+0dd7nqC
5ClCaELSGn4Ouk1GB1BkzEzbTkc4reSHbfBlrKHlHkitZNwXbroKOoe5MEwe+oPA
XxRV82fUgWvuHrspWKj/PJjJ7cV5KwXhygPu9K4eehkxpXrRlokhzapZ0E+S1yQI
Y2vcvmSBq6175HnYUZdmI10CgYEA1bv1ZrFr3tnaotjk8ugLSTnEFs2eNfv1C1LW
QdGpww14oGL/1aLmSvPaZ4exO4IdT8aaS5Fm/AN9TQgN8fUdIiGBmSEt7kZdzwzK
8PcEoR8OWWVQilVzqeNKw2aDPr1N8UDl86eXNzzRvnRd4XdhT+ykjhMxtVOtVeHQ
i7vwr/kCgYEAp078xSx38n4BmPugvh3xQTcGg4vh+0UgLDC28+ZuA2T2Jwn9meGI
3lRleIkVb1lkSOsFVoqJmVjJOuZ9t6NHoVnFzH33sknpDgsC2uW0/jgQyYJEwRU7
v4fwm5JlslzTDgAolw0JuOFc/+p7V1Vpi/AGxZ+J8Groo4w7zccIijkCgYByNbnw
YiZOMwONuXC+DBjbzC5oMP+1wSk0H9O14B9ixzQKIFytABsnOh8e63ddYS3gjzOr
5cquJ/8wxnkNLfmfX2AtP3mXtaozFZbsJFMo9btpMaZUBU2FHpu4xnKjd+zKWe+G
v6siLTG3H996t5wcZUuZT9BkII6jMcOKp6b5oQKBgBbl250gb+4cvIiCLsdgCW8j
oSkRhS+yMDH4PLuGG2aiD8Poiiv6cFe4l02RAW5G6RQUz4cLq/HoABnoyw+s9XbX
il/aHWEUd/Eoe+qLOEN8OD/6ZmYwKCno9RRGedCj1LQoxwnZBYku99fd3EQqjOU9
fJoYOBktao4dC5NqcoZR
-----END PRIVATE KEY-----"""

  JWT_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwB8XU8WuvKrJ4TxZf2Nr
cCGW2S88MslxWj2mfcJ77dnhIfGFlhUtokXOo2iPUYovUQ7gk6UrIgI2psai+rdo
SY7H/DuRXxf7RWbq9QWOajBrNl7P2ITu1jVZP40zzm/LslXtANYWg15t026LLyFa
Y1UIpOIS4EPgvdFTixG73OVOnd8cwQApETMMqUe0obt7lDe2yRwr7Cl5CrCJM3H4
DOlOiB9RmWk5LfVYK28+hCJpAQbtZqdQ3LsLpabDuoYMBSr6bo4FU+tkDsnYrflS
jDgXVkU9120f8AWjFjWvzzXGORaCeuhovwDdG36bVWD/+aRuAR/CaJsSZnzwKrT4
dQIDAQAB
-----END PUBLIC KEY-----"""
  def setUp(self) -> None:
    self.client = APIClient()

  def generate_jwt_token(self, roles=None, exp_minutes=60, **extra_claims):
    if roles is None:
      roles = ["offline_access", "admin", "uma_authorization", "default-roles-codeflix"]
    
    now = int(datetime.now(timezone.utc).timestamp())
    
    payload = {
      "realm_access": {
        "roles": roles
      },
      "iat": now,
      "exp": now + (exp_minutes * 60),
      "iss": "http://localhost:8080/realms/codeflix",
      "sub": "test-user-id",
      "typ": "Bearer",
      "azp": "test-client",
      "aud": "account",  # Audience que seu serviço espera
      **extra_claims
    }
    
    token = jwt.encode(payload, self.JWT_PRIVATE_KEY.encode(), algorithm="RS256")
    return token
  
  def authenticate_user(self, roles=None, **token_claims):
    os.environ['AUTH_PUBLIC_KEY'] = self.JWT_PUBLIC_KEY
    token = self.generate_jwt_token(roles=roles, **token_claims)
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return token
  
  def authenticate_admin(self):
    """Autentica como admin"""
    return self.authenticate_user(roles=["admin", "offline_access", "uma_authorization"])

