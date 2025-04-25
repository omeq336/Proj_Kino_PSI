"""Module containing showing service implementation."""
from datetime import datetime
from typing import Iterable

from cinemaapi.core.domain.showing import Showing, ShowingBroker
from cinemaapi.core.repositories.ishowing import IShowingRepository
from cinemaapi.infrastructure.dto.showingdto import ShowingDTO
from cinemaapi.infrastructure.services.ishowing import IShowingService


class ShowingService(IShowingService):
    """A class implementing the showing service."""

    _repository: IShowingRepository

    def __init__(self, repository: IShowingRepository) -> None:
        """The initializer of the `showing service`.

        Args:
            repository (IShowingRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all(self) -> Iterable[ShowingDTO]:
        """The method getting all showings from the repository.

        Returns:
            Iterable[ShowingDTO]: All showings.
        """

        return await self._repository.get_all_showings()

    async def get_by_id(self, showing_id: int) -> ShowingDTO | None:
        """The method getting showing by provided id.

        Args:
            showing_id (int): The id of the showing.

        Returns:
            ShowingDTO | None: The showing details.
        """

        return await self._repository.get_showing_by_id(showing_id)

    async def get_by_repertoire(self, repertoire_id: int) -> Iterable[ShowingDTO]:
        """The method getting showings assigned to particular repertoire.

        Args:
            repertoire_id (int): The id of the repertoire.

        Returns:
            Iterable[ShowingDTO]: Showings assigned to a repertoire.
        """

        return await self._repository.get_by_repertoire(repertoire_id)

    async def get_showings_by_date(self, showing_date: str) -> Iterable[ShowingDTO]:
        """The method getting showings assigned to date.

        Args:
            showing_date (int): The date of the showing.

        Returns:
            Iterable[ShowingDTO]: Showings assigned to a date.
        """

        return await self._repository.get_showings_by_date(showing_date)


    async def get_showings_by_time(self, showing_time: str) -> Iterable[ShowingDTO]:
        """The method getting showings with time equal to showing_time or above.

        Args:
            showing_time (int): The time of the showing.

        Returns:
            Iterable[ShowingDTO]: Showings within given time or above.
        """

        return await self._repository.get_showings_by_time(showing_time)


    async def get_showings_by_language_ver(self, language_ver: str) -> Iterable[ShowingDTO]:
        """The method getting showings assigned to language version.

        Args:
            language_ver (str): The language version of the showing.

        Returns:
            Iterable[ShowingDTO]: Showings with given language version.
        """

        return await self._repository.get_showings_by_language_ver(language_ver)


    async def get_showings_by_movie_genre(self, genre: str) -> Iterable[ShowingDTO]:
        """The method getting showings assigned to particular movie genre.

        Args:
            genre (str): The genre of the movie.

        Returns:
            Iterable[ShowingDTO]: Showings assigned to genre.
        """

        return await self._repository.get_showings_by_movie_genre(genre)


    async def get_showing_by_movie_title(self, title: str) -> Iterable[ShowingDTO]:
        """The method getting showings assigned to particular title.

        Args:
            title (str): The title of the movie.

        Returns:
            Iterable[ShowingDTO]: Showings with given title.
        """

        return await self._repository.get_showing_by_movie_title(title)


    async def get_showings_by_age_restriction(self, age: int) -> Iterable[ShowingDTO]:
        """The method getting showings with age restriction lower or equal to given age.

        Args:
            age (int): The age restriction of the movie.

        Returns:
            Iterable[ShowingDTO]: Showings with lower or equal age restriction.
        """

        return await self._repository.get_showings_by_age_restriction(age)

    async def add_showing(self, data: ShowingBroker) -> Showing | None:
        """The method adding new showing to the data storage.

        Args:
            data (ShowingBroker): The details of the new showing.

        Returns:
            Showing | None: Full details of the newly added showing.
        """

        return await self._repository.add_showing(data)

    async def update_showing(
            self,
            showing_id: int,
            data: ShowingBroker,
    ) -> Showing | None:
        """The method updating showing data in the data storage.

         Args:
             showing_id (int): The id of the showing.
             data (ShowingBroker): The details of the updated showing.

         Returns:
             Showing | None: The updated showing details.
         """

        return await self._repository.update_showing(
            showing_id=showing_id,
            data=data,
        )

    async def delete_showing(self, showing_id: int) -> bool:
        """The method removing showing from the data storage.

        Args:
            showing_id (int): The id of the showing.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_showing(showing_id)

    async def validate_showing(self, data: ShowingBroker) -> str | None:
        """The method responsible for validating data.

        Args:
            data (ShowingBroker): The data of the showing.

        Returns:
            str | None: Validation status.
        """

        if data.language_ver not in ["Subtitles", "subtitles", "Dubbing", "dubbing", "Lector", "lector"]:
            return "showing-language_version-invalid"

        if data.price < 0:
            return "showing-price-invalid"

        time_split = data.time.split(":")
        if len(time_split) != 2:
            return "showing-time-invalid"

        try:
            hour = int(time_split[0])
            minute = int(time_split[1])
        except:
            return "showing-time-invalid"

        if hour > 23 or hour < 0 or minute > 59 or minute < 0:
            return "showing-time-invalid"

        try:
            converted_date = datetime.strptime(data.date, "%Y-%m-%d").date()
        except:
            return "showing-date-invalid"

        if showing_iter := await self._repository.get_showings_by_date(data.date):
            for showing in showing_iter:
                if showing.hall_id == data.hall_id \
                    and not await self._check_availability(data, showing):
                    return "showing-hall-occupied"

        return None

    async def _check_availability(self, showing_to_check: ShowingBroker, established_showing: ShowingDTO) -> bool:
        """The private method responsible for checking hall availability.

        Args:
            showing_to_check (ShowingBroker): The data of the showing we want to insert.
            established_showing (ShowingDTO): The data of the already existing showing.

        Returns:
            bool: Success of the operation.
        """

        showing_time = established_showing.time.split(":")
        showing_duration = await self._repository.fetch_showing_duration(established_showing.movie.id)

        hour = int(showing_time[0])
        minutes = int(showing_time[1])

        duration = showing_duration.split(".")
        duration_hours = int(duration[0])
        duration_minutes = int(duration[1])

        end_hour = hour
        end_minutes = minutes

        if minutes + duration_minutes >= 60:
            end_minutes = (minutes + duration_minutes) - 60
            end_hour += 1
        else:
            end_minutes += duration_minutes

        if hour + duration_hours >= 24:
            end_hour = (duration_hours + hour) - 24
        else:
            end_hour += duration_hours

        time_to_check = showing_to_check.time
        time_split = time_to_check.split(":")
        th = int(time_split[0])
        tm = int(time_split[1])

        if hour <= th <= end_hour and minutes <= tm <= end_minutes:
            return False
        else:
            return True
