import os
import django
import random
import sys
from faker import Faker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Videogames_project.settings')
django.setup()

from videogames_register.models import VideoGame, Genre, Developer, UserProfile, Review, Copy
from django.contrib.auth.models import User

fake = Faker()

def seed():

    Copy.objects.all().delete()
    Review.objects.all().delete()
    VideoGame.objects.all().delete()
    Developer.objects.all().delete()
    UserProfile.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()
    Genre.objects.all().delete()

    GENRE_NAMES = ['Action', 'Adventure', 'RPG', 'Shooter', 'Puzzle', 'Strategy', 'Sports']
    for name in GENRE_NAMES:
        Genre.objects.get_or_create(title=name)

    GAME_TITLES = [
        "Shadowblade", "Galactic Titans", "Mystic Quest", "Steel Reign",
        "Cyber Drift", "Knightfall Chronicles", "Inferno Squad", "Frostbound",
        "Echoes of Oblivion", "Nova Arena", "Crystal Rift", "Phantom Protocol",
        "Neon Shards", "Eternal Siege", "Dark Horizon", "Turbo Strikers",
        "Skyfall Bastion", "Quantum Rift", "Blood Circuit", "Ashen Crown"
    ]

    GAME_DESCRIPTIONS = [
        "A fast-paced action game set in a dystopian future.",
        "Explore ancient ruins and uncover hidden secrets.",
        "Command your troops in a real-time strategy battlefield.",
        "Join the rebellion against the galactic empire.",
        "A fantasy RPG with immersive storytelling and rich lore.",
        "Drive high-tech vehicles in a neon cyberpunk city.",
        "Survive endless waves of enemies in post-apocalyptic arenas.",
        "Build and manage your own medieval kingdom.",
        "Compete in futuristic sports tournaments with deadly consequences.",
        "Navigate political intrigue and betrayal in a space federation.",
        "Hack into networks while avoiding elite AI defenders.",
        "Fly elite starfighters in tactical interstellar battles.",
        "Uncover the mystery behind vanishing cities.",
        "Combine magic and technology to restore a broken world.",
        "Control mythical creatures in turn-based combat.",
        "Battle rogue AIs in a derelict digital wasteland.",
        "Rescue colonies lost to alien infestations.",
        "Rebuild civilization after a massive solar storm.",
        "Explore underwater cities and defend against sea monsters.",
        "Join secret guilds and shape the fate of nations."
    ]

    for _ in range(5):
        Developer.objects.create(
            name=fake.company(),
            founded_year=random.randint(2000, 2025)
        )

    all_genres = list(Genre.objects.all())
    all_devs = list(Developer.objects.all())
    # Create only curated games
    games = []
    for i in range(len(GAME_TITLES)):
        game = VideoGame.objects.create(
            title=GAME_TITLES[i],
            description=GAME_DESCRIPTIONS[i],
            release_date=fake.date_between(start_date='-10y', end_date='today'),
            genre=random.choice(all_genres),
        )
        games.append(game)


    for _ in range(5):
        user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password="testpass123"
        )
        UserProfile.objects.create(
            user=user,
            country=fake.country(),
            age=random.randint(18, 50)
        )
    users = list(User.objects.all())



    for i in range(len(GAME_TITLES)):
        VideoGame.objects.create(
            title=GAME_TITLES[i],
            description=GAME_DESCRIPTIONS[i],
            release_date=fake.date_between(start_date='-10y', end_date='today'),
            genre=random.choice(all_genres),

        )

    for game in games:
        for _ in range(random.randint(1, 3)):
            Copy.objects.create(
                game=game,
                serial_number=fake.uuid4(),
                condition=random.choice(['New', 'Used', 'Mint'])
            )

    for _ in range(30):
        Review.objects.create(
            user=random.choice(users),
            game=random.choice(games),
            rating=random.randint(1, 10),
            comment=fake.sentence()
        )


    for game in games:
        for _ in range(random.randint(1, 3)):
            Copy.objects.create(
                game=game,
                serial_number=fake.uuid4(),
                condition=random.choice(['New', 'Used', 'Mint'])
            )

    print("Done seeding data.")

if __name__ == "__main__":
    seed()
