from datetime import datetime
from dateutil.relativedelta import relativedelta

class ExperienceCalculator:
    def __init__(self):
        pass

    def calculate_total_experience(self, experiences):
        total_delta = relativedelta()
        for exp in experiences:
            start_date_str = exp.get("start_date")
            end_date_str = exp.get("end_date")
            is_current = exp.get("is_current", False)

            if not start_date_str:
                continue

            try:
                # Handle cases where only year is provided
                if len(start_date_str) == 4 and start_date_str.isdigit():
                    start_date = datetime.strptime(start_date_str, "%Y")
                else:
                    start_date = datetime.strptime(start_date_str, "%b %Y") # e.g., Jan 2020
            except ValueError:
                # Try another common format if "%b %Y" fails
                try:
                    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                except ValueError:
                    print(f"Warning: Could not parse start_date: {start_date_str}")
                    continue

            if is_current:
                end_date = datetime.now()
            elif end_date_str:
                try:
                    if len(end_date_str) == 4 and end_date_str.isdigit():
                        end_date = datetime.strptime(end_date_str, "%Y")
                    else:
                        end_date = datetime.strptime(end_date_str, "%b %Y")
                except ValueError:
                    # Try another common format if "%b %Y" fails
                    try:
                        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                    except ValueError:
                        print(f"Warning: Could not parse end_date: {end_date_str}")
                        continue
            else:
                end_date = datetime.now() # Assume current if no end date and not marked as current (fallback)

            if start_date and end_date and end_date > start_date:
                total_delta += relativedelta(end_date, start_date)

        # Convert total_delta to years. This is an approximation
        # considering 12 months per year and 30 days per month for simplicity.
        # relativedelta directly gives years, months, days.
        total_years = total_delta.years + total_delta.months / 12 + total_delta.days / 365.25
        return round(total_years, 2)
