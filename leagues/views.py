from django.shortcuts import render, redirect
from .models import League, Team, Player

from . import team_maker


def index(request):
    context = {
        # leagues query
        "leagues": League.objects.all(),
        "teams": Team.objects.all(),
        "players": Player.objects.all(),
        "baseball_leagues": League.objects.filter(sport="Baseball"),
        "women_leagues": League.objects.filter(name__contains="Womens"),
        "hockey_leagues": League.objects.filter(sport__contains="Hockey"),
        "no_football_leagues": League.objects.exclude(sport="Football"),
        "conference_leagues": League.objects.filter(name__contains="Conference"),
        "atlantic_leagues": League.objects.filter(name__contains="atlantic"),
        # teams query
        "dallas_location": Team.objects.filter(location="Dallas"),
        "raptors_team": Team.objects.filter(team_name="Raptors"),
        "with_city": Team.objects.filter(location__contains="city"),
        "team_t_start": Team.objects.filter(team_name__startswith="T"),
        "teams_by_location": Team.objects.order_by("location"),
        "team_desc": Team.objects.order_by("-team_name"),
        # players query
        "cooper_last_name": Player.objects.filter(last_name="Cooper"),
        "joshua_name": Player.objects.filter(first_name="Joshua"),
        "cooper_ex_joshua": Player.objects.filter(last_name="Cooper")
        & Player.objects.exclude(first_name="Joshua"),
        "alexander_wyatt": Player.objects.filter(first_name="Alexander")
        | Player.objects.filter(first_name="Wyatt")
        & Player.objects.order_by("first_name"),
    }
    return render(request, "leagues/index.html", context)


def make_data(request):
    team_maker.gen_leagues(10)
    team_maker.gen_teams(50)
    team_maker.gen_players(200)

    return redirect("index")
