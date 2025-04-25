"""Module providing containers injecting dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from cinemaapi.infrastructure.repositories.moviedb import \
    MovieRepository
from cinemaapi.infrastructure.repositories.reviewdb import \
    ReviewRepository
from cinemaapi.infrastructure.repositories.repertoiredb import \
    RepertoireRepository
from cinemaapi.infrastructure.repositories.showingdb import \
    ShowingRepository
from cinemaapi.infrastructure.repositories.halldb import \
    HallRepository
from cinemaapi.infrastructure.repositories.reservationdb import \
    ReservationRepository
from cinemaapi.infrastructure.repositories.userdb import UserRepository

from cinemaapi.infrastructure.services.repertoire import RepertoireService
from cinemaapi.infrastructure.services.review import ReviewService
from cinemaapi.infrastructure.services.showing import ShowingService
from cinemaapi.infrastructure.services.movie import MovieService
from cinemaapi.infrastructure.services.hall import HallService
from cinemaapi.infrastructure.services.reservation import ReservationService
from cinemaapi.infrastructure.services.user import UserService



class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    movie_repository = Singleton(MovieRepository)
    review_repository = Singleton(ReviewRepository)
    repertoire_repository = Singleton(RepertoireRepository)
    showing_repository = Singleton(ShowingRepository)
    hall_repository = Singleton(HallRepository)
    reservation_repository = Singleton(ReservationRepository)
    user_repository = Singleton(UserRepository)
    
    movie_service = Factory(
        MovieService,
        repository=movie_repository,
    )
    review_service = Factory(
        ReviewService,
        repository=review_repository,
    )
    repertoire_service = Factory(
        RepertoireService,
        repository=repertoire_repository,
    )
    showing_service = Factory(
        ShowingService,
        repository=showing_repository,
    )
    hall_service = Factory(
        HallService,
        repository=hall_repository,
    )
    reservation_service = Factory(
        ReservationService,
        repository=reservation_repository,
    )
    user_service = Factory(
        UserService,
        repository=user_repository,
    )