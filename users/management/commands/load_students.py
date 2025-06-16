import json
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from users.models import UniversityStudent
from pathlib import Path

class Command(BaseCommand):
    help = 'Loads student data from JSON file into UniversityStudent model'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_file',
            type=str,
            help='Path to JSON file containing student records'
        )

    def handle(self, *args, **options):
        json_file = options['json_file']
        file_path = Path(json_file)

        if not file_path.exists():
            self.stdout.write(self.style.ERROR(f"File not found: {json_file}"))
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                students = json.load(f)
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"Invalid JSON file: {e}"))
            return

        total = len(students)
        created = 0
        skipped = 0
        errors = 0

        for student in students:
            try:
                # Clean and validate data
                matric_number = student['matric_number'].strip().upper()
                first_name = student['first_name'].strip()
                last_name = student['last_name'].strip()
                middle_name = student.get('middle_name', '').strip()
                faculty = student['faculty'].strip()
                department = student['department'].strip()
                year_admitted = int(student['year_admitted'])
                email = student['email'].strip().lower()

                UniversityStudent.objects.create(
                    matric_number=matric_number,
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    faculty=faculty,
                    department=department,
                    year_admitted=year_admitted,
                    email=email
                )
                created += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Added {matric_number} - {first_name} {last_name}")
                )

            except IntegrityError:
                skipped += 1
                self.stdout.write(
                    self.style.WARNING(f"Skipped duplicate: {student.get('matric_number', 'UNKNOWN')}")
                )
            except KeyError as e:
                errors += 1
                self.stdout.write(
                    self.style.ERROR(f"Missing required field {e} in record: {student}")
                )
            except Exception as e:
                errors += 1
                self.stdout.write(
                    self.style.ERROR(f"Error processing {student.get('matric_number', 'UNKNOWN')}: {e}")
                )

        self.stdout.write("\n" + "="*50)
        self.stdout.write(self.style.SUCCESS(
            f"Import completed!\n"
            f"Total records: {total}\n"
            f"Created: {created}\n"
            f"Skipped (duplicates): {skipped}\n"
            f"Errors: {errors}"
        ))