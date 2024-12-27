"""
This file was created by NAU to generate a csv
output of all courses data
"""

import time

from django.core.management.base import BaseCommand

from richie.apps.courses.models.course import Course


class Command(BaseCommand):
    """
    Extracts courses information to a csv easy format

    Usage: python manage.py extract_courses_data
    """

    def _generate_data(self, courses: list[Course]):
        """
        This method generates the courses information output
        """

        data = []
        output = ""

        for course in courses:
            organization = course.get_organizations().first()
            if course.extended_object and organization:
                plugins = (
                    course.extended_object.get_placeholders()
                    .get(slot="course_teaser")
                    .get_plugins()
                )

                teaser_link = "N/A"
                if plugins:
                    teaser_link = plugins[0].get_bound_plugin().embed_link

                url = course.extended_object.get_absolute_url()
                page_title = course.extended_object.get_title()
                org_name = organization.extended_object.get_title()

                line = f"{url};{page_title};{teaser_link};{org_name};{organization.code};\n"
                if line not in output:
                    output += line
                    data.append(
                        {
                            "url": url,
                            "title": page_title,
                            "teaser_link": teaser_link,
                            "org_name": org_name,
                            "org_code": organization.code,
                        }
                    )

        self.stdout.write("\n----------- GET HERE THE OUTPUT -----------\n")
        self.stdout.write(output)
        self.stdout.write("\n------------------------------------ \n")

        return data

    def handle(self, *args, **options):
        """
        This method starts the script execution
        """

        self.stdout.write("Starting extraction...")
        start = time.time()

        courses = Course.objects.all()
        if len(courses) > 0:
            self.stdout.write("Generating the content...")
            data = self._generate_data(courses)
            finish = time.time() - start
            self.stdout.write(
                f"Finished data extraction with {len(data)} registers and took {finish} seconds"
            )

            return

        self.stdout.write("None course was found")
