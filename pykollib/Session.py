from .request.HomepageRequest import HomepageRequest
from .request.LoginRequest import LoginRequest
from .request.LogoutRequest import LogoutRequest
from .request.StatusRequest import StatusRequest
from .request.CharpaneRequest import CharpaneRequest



import cookielib    # @UnusedImport
import hashlib

try:
    import requests  # @UnusedImport
    from Opener import RequestsOpener as Opener
except ImportError:
    from Opener import StandardOpener as Opener


class Session(object):
    "This class represents a user's session with The Kingdom of Loathing."

    def __init__(self):
        self.opener = Opener()
            
        self.isConnected = False
        self.userId = None
        self.userName = None
        self.userPasswordHash = None
        self.serverURL = None
        self.pwd = None

    def login(self, username, password, serverNumber=0):
        """
        Perform a KoL login given a username and password. A server number may also be specified
        to ensure that the user logs in using that particular server. This can be helpful
        if the user continues to be redirected to a server that is down.
        """
        
        self.userName = username
        self.userPasswordHash = hashlib.md5(password).hexdigest()
        self.password = password;

        # Grab the KoL homepage.
        homepageRequest = HomepageRequest(self, serverNumber=serverNumber)
        homepageResponse = homepageRequest.doRequest()
        self.serverURL = homepageResponse["serverURL"]

        # Perform the login.
        loginRequest = LoginRequest(self, "")
        loginRequest.doRequest()

        # Load the charpane once to make StatusRequest report the rollover time
        charpaneRequest = CharpaneRequest(self)
        charpaneRequest.doRequest()

        # Get pwd, user ID, and the user's name.
        request = StatusRequest(self)
        response = request.doRequest()
        self.pwd = response["pwd"]
        self.userName = response["name"]
        self.userId = int(response["playerid"])
        self.rollover = int(response["rollover"])

    def logout(self):
        "Performs a logut request, closing the session."
        logoutRequest = LogoutRequest(self)
        logoutRequest.doRequest()
