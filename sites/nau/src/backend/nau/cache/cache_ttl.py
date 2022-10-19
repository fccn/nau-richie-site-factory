"""
Cache utility for courses.
"""
from datetime import datetime, timedelta
from typing import List

from django.utils import timezone

from richie.apps.courses.models.course import Course, CourseRun

CACHE_MARGIN = timedelta(seconds=30)


def get_sorted_course_runs_dates(course: Course) -> List[datetime]:
    """
    Returns the course runs dates, start, end, enrollment start and enrollment end, sorted by
    date.
    """

    def get_course_run_dates(run: CourseRun) -> List[datetime]:
        return (
            run.start,
            run.end,
            run.enrollment_start,
            run.enrollment_end,
        )

    nested_list = [get_course_run_dates(r) for r in course.course_runs]
    dates_flat_list = [element for sublist in nested_list for element in sublist]
    # filter `None`, then sort all the dates
    dates_sorted = sorted(list(filter(lambda d: d, dates_flat_list)))
    # return dates_sorted[0] if len(dates_sorted) > 0 else None
    return dates_sorted


# Django CMS Cache
def limit_course_page_cache_ttl(response):
    """
    Limit the cache ttl to be lower than the next course date that could change the course page
    presentation.
    """
    request = response._request  # pylint: disable=protected-access
    page = request.current_page
    if hasattr(page, "course"):
        dates = get_sorted_course_runs_dates(page.course)
        lower = timezone.now() - CACHE_MARGIN
        higher = timezone.now() + CACHE_MARGIN
        for date in dates:
            if date > higher:  # future date
                return int((date - timezone.now() - CACHE_MARGIN).total_seconds())
            if lower <= date <= higher:  # within the cache margin
                return 0  # do not cache
    return None
