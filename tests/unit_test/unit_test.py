# unit_test.py
# created 19/01/2021 at 16:24 by Antoine 'AatroXiss' BEAUDESSON
# last modified 20/01/2021 at 14:25 by Antoine 'AatroXiss' BEAUDESSON

""" unit_test.py

To do:
    - implement all unit tests
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.0.6"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports
from datetime import datetime

# third party imports

# local application imports
import server

# other imports

# constants
NUMBER_OF_CLUBS = 3
NUMBER_OF_COMPETITIONS = 2
WRONG_EMAIL = "wrong@gmail.com"
EMPTY_EMAIL = ""


class TestDatabases():

    def test_load_clubs(self):
        """
        Test that the clubs.json file is loaded correctly
        we know that the file is loaded correctly because
        listOfClubs has the same number of clubs as the
        clubs.json file"""

        listOfClubs = server.loadClubs()
        assert len(listOfClubs) == NUMBER_OF_CLUBS

    def test_load_competitions(self):
        """
        Test that the competitions.json file is loaded correctly
        we know that the file is loaded correctly because
        listOfCompetitions has the same number of competitions as the
        competitions.json file"""

        listOfCompetitions = server.loadCompetitions()
        assert len(listOfCompetitions) == NUMBER_OF_COMPETITIONS


class TestIndex():

    # Happy paths => hp / Sad paths => sp

    def test_get_index_status_code_200(self, client):
        """
        Test that the page is loaded correctly.
        we know that because the page has the status code 200.
        We also know that the page has the right template because
        the title of the page is GUDLFT Registration"""

        response = client.get('/')
        assert response.status_code == 200
        assert ("GUDLFT Registration") in response.data.decode()

    def test_post_index_status_code_405(self, client):
        """
        Test that the index page returns a 405 status code on a post request
        """
        response = client.post('/')
        assert response.status_code == 405


class TestShowSummary():

    def test_post_hp_registered_user_login(self, client):
        """
        Test where a user logs in with a registered email.
        We know the user has successfully logged in because
        the status code is 200 and the page has the right template
        We know that the template is correct because the welcome message
        is displayed with the user's email"""

        email = server.loadClubs()[0]['email']
        response = client.post('/showSummary', data={'email': email})
        assert response.status_code == 200
        assert ("Welcome, " + email) in response.data.decode()

    def test_post_sp_unregistered_user_login(self, client):
        """
        Test where a user logs in with an unregistered email.
        We know the user has successfully not logged in because
        the status code is 200 and the page has the right template
        We know that the template is correct because the error message
        is displayed
        """
        email = WRONG_EMAIL
        response = client.post('/showSummary', data={'email': email})
        assert response.status_code == 200
        assert ("Error: email is not registered") in response.data.decode()

    def test_post_sp_no_email_user_login(self, client):
        """
        Test where a user logs in with no email.
        We know the user has successfully not logged in because
        the status code is 200 and the page has the right template
        We know that the template is correct because the error message
        is displayed
        """
        email = EMPTY_EMAIL
        response = client.post('/showSummary', data={'email': email})
        assert response.status_code == 200
        assert ("Error: field is empty") in response.data.decode()

    def test_post_status_code_200_template(self, client):
        """
        Test that the page is loaded correctly.
        we know that because the page has the status code 200.
        We also know that the page has the right template because
        the title of the page is GUDLFT Registration"""

        email = server.loadClubs()[0]['email']
        response = client.post('/showSummary', data={'email': email})
        assert response.status_code == 200
        assert ("GUDLFT Registration") in response.data.decode()

    def test_competition_list(self, client):
        """
        Test that the competition list is correctly is loaded.
        We know that the list is correctly loaded because
        the competition name can be found in the list of competitions
        We use datetime to determine if the competition is in the past
        or not.
        If it is in the past, it is not displayed in the list
        """

        email = server.loadClubs()[0]['email']

        competition = server.loadCompetitions()
        response = client.post('/showSummary', data={'email': email})

        for competition in competition:
            if datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S') > datetime.now():  # noqa
                assert competition['name'] in response.data.decode()
            else:
                assert competition['name'] not in response.data.decode()


class TestBook():

    def test_status_code_200_template(self, client):
        """
        Test that the page is loaded correctly
        we know that because the page has the status code 200.
        We also know that the page has the right template because
        the page has the title booking for"""

        competition_name = server.loadCompetitions()[0]['name']
        club_name = server.loadClubs()[0]['name']
        response = client.get('/book/' + competition_name + '/' + club_name)
        assert response.status_code == 200
        assert ("Booking for " + competition_name) in response.data.decode()


class TestPurchasePlaces():

    def test_sp_book_too_many_places(self, client):
        """
        Test that the user cannot book more than 12 places
        we can now that because the page contains the error message
        Error: you cannot book more than 12 places
        """
        competition_name = server.loadCompetitions()[0]['name']
        club_name = server.loadClubs()[0]['name']

        response = client.post(
            '/purchasePlaces',
            data={
                'places': '13',
                'competition': competition_name,
                'club': club_name
            }
        )
        assert response.status_code == 200
        assert ("Error: you cannot book more than 12 places") in response.data.decode()  # noqa

    def test_sp_book_no_places_available(self, client):
        """
        Test  that a user cannot book more than the number
        of places available in the competition.
        We know that the system has correctly prevented the user
        from booking more places than the number of places available
        because the page contains the error message
        Error: there are no places available
        """

        competition_name = server.loadCompetitions()[0]['name']
        club_name = server.loadClubs()[0]['name']

        response = client.post(
            '/purchasePlaces',
            data={
                'places': '13',
                'competition': competition_name,
                'club': club_name
            }
        )
        assert response.status_code == 200
        assert ("Error: there are no places available") in response.data.decode()  # noqa

    def test_sp_book_no_enough_points(self, client):
        """
        Test that makes sure that a user cannot book a competition
        if they do not have enough points.
        We know that the user cannot book a competition because
        the page contains the error message
        Error: you do not have enough points
        """

        competition_name = server.loadCompetitions()[0]['name']
        club_name = server.loadClubs()[0]['name']
        club_points = int(server.loadClubs()[0]['points']) + 1

        response = client.post(
            '/purchasePlaces',
            data={
                'places': club_points,
                'competition': competition_name,
                'club': club_name
            }
        )
        assert response.status_code == 200
        assert ("Error: you do not have enough points") in response.data.decode()  # noqa

    def test_hp_book_succeeded_points_are_deducted(self, client):
        competition_name = server.loadCompetitions()[0]['name']
        club_name = server.loadClubs()[0]['name']
        club_points = int(server.loadClubs()[0]['points'])

        response = client.post(
            '/purchasePlaces',
            data={
                'places': club_points,
                'competition': competition_name,
                'club': club_name
            }
        )
        club_points_left = int(server.loadClubs()[0]['points'])
        assert response.status_code == 200
        assert ("Great-booking complete!") in response.data.decode()
        assert (club_points_left == 0)


class TestLogout():

    def test_logout(self, client):
        """
        Test that the user is correctly logged out.
        We know that the user is correctly logged out because
        the status code is 302
        """

        response = client.get('/logout')
        assert response.status_code == 302
