from django.shortcuts import render, redirect
from .models import League, Team, Player
from django.db.models import Count
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


def index2(request): 
    try:
        wichitas = Team.objects.get(team_name = "Vikings", location = "Wichita")
        wichita_players = wichitas.all_players.all()
        wichita_current_ids = [player.id for player in wichitas.curr_players.all()]
        wichita = [player for player in wichita_players if player.id not in wichita_current_ids]
        
        jg = Player.objects.get(first_name='Jacob', last_name='Gray')
        jg_teams = jg.all_teams.all()
        colts =  Team.objects.filter(team_name='Colts'),
        teams_jg= [team for team in jg_teams if jg.curr_team.id not in colts]

    except Team.DoesNotExist:
        wichita = []
        teams_jg = []   
      
    context = {
        "leagues": League.objects.all(),
        "teams": Team.objects.all(),
        "players": Player.objects.all(),
        "atlantic_soccer": Team.objects.filter(league__id = '5'),
        "boston_penguins":Player.objects.filter(curr_team__id='28'),
        "international_CBC": Player.objects.filter(curr_team__league__id='2'),
        "conferencia_lopez": Player.objects.filter(curr_team__league__id='7') & Player.objects.filter(last_name__contains='Lopez'),
        "football_players":Player.objects.filter(curr_team__league__sport='Football'),
        "sophia_teams": Team.objects.filter(curr_players__first_name='Sophia'),
        "sophia_leagues": League.objects.filter(teams__curr_players__first_name='Sophia'),
        "flores_no_WR": Player.objects.filter(last_name='Flores').exclude(curr_team__team_name='Roughriders'),
        "samuel_evans_teams": Team.objects.filter(all_players__first_name='Samuel') & Team.objects.filter(all_players__last_name='Evans'),
        "tiger_cat":Player.objects.filter(all_teams__team_name='Tiger-Cats'),
        "wichita": wichita,
        "teams_jg":teams_jg,
        "joshua": Player.objects.filter(first_name='Joshua', all_teams__league__id='3'),
        "teams_with_12plus":Team.objects.annotate(Count('all_players')).filter(all_players__count__gt=12),
        "teams4player": Player.objects.annotate(Count('all_teams')).order_by('all_teams__count'),

    }
    return render(request, "leagues/index2.html", context)
  
def make_data(request):
    team_maker.gen_leagues(10)
    team_maker.gen_teams(50)
    team_maker.gen_players(200)

    return redirect("index")

