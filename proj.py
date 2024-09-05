#shaimaa ahmad dar taha 
#roa makhtoob

import re
import os
from datetime import datetime



class MedicalTestRecord:
    def __init__(self, patient_id, test_name, test_datetime, result, unit, status, result_datetime=""):
        self.patient_id = patient_id
        self.test_name = test_name
        self.test_datetime = test_datetime
        self.result = result
        self.unit = unit
        self.status = status
        self.result_datetime = result_datetime

    def save(self):
        with open("midecalRecord.txt", "a") as file:
            file.write(
                f"{self.patient_id}: {self.test_name}, {self.test_datetime}, {self.result}, {self.unit}, {self.status}")
            if self.status == "Completed":
                file.write(f", {self.result_datetime}")
            file.write("\n")
        print("The test record has been added.\n")


class MedicalTestType:
    def __init__(self, name, normal_range, unit, turnaround_time):
        self.name = name  # Name of the medical test
        self.normal_range = normal_range  # A tuple representing the range. Use None for unbounded limits.
        self.unit = unit  # Unit of measurement for the test result
        self.turnaround_time = turnaround_time  # In the format "DD-hh-mm"

    def __str__(self):
        min_range = f">{self.normal_range[0]}" if self.normal_range[0] is not None else ""
        max_range = f"<{self.normal_range[1]}" if self.normal_range[1] is not None else ""
        range_str = f"{min_range} {max_range}".strip()
        return f"{self.name}: Range ({range_str}), Unit: {self.unit}, Turnaround Time: {self.turnaround_time}"


class MedicalTestTypeManager:
    def __init__(self, file_name="medicalTest.txt"):
        self.file_name = file_name
        self.test_types = {}

    # Load test types from the file
    def load_test_types(self):
        self.test_types = {}
        try:
            with open('medicalTest.txt', 'r') as file:
                for line in file:
                    # Parse the file line to extract test type details
                    test_name_match = re.search(
                        r'Name: .*? \((.*?)\); Range: > ([0-9.]+), < ([0-9.]+); Unit: (.*?), (.*)', line)
                    if test_name_match:
                        shorthand_name = test_name_match.group(1).strip()
                        min_range = float(test_name_match.group(2))
                        max_range = float(test_name_match.group(3))
                        unit = test_name_match.group(4).strip()
                        turnaround_time = test_name_match.group(5).strip()
                        self.test_types[shorthand_name] = MedicalTestType(
                            shorthand_name, (min_range, max_range), unit, turnaround_time)
        except FileNotFoundError:
            print("No test types file found. Starting with an empty list.")

   
   
    
    def format_range(self, normal_range):
        """Format the range back to string, e.g., '> 70, < 99'."""
        min_range = f"> {normal_range[0]}" if normal_range[0] is not None else ""
        max_range = f"< {normal_range[1]}" if normal_range[1] is not None else ""
        return f"{min_range}, {max_range}".strip(', ')

    # Add a new medical test type
    def add_new_test_type(self, name, min_range, max_range, unit, turnaround_time):
        # Check if the test type already exists
        if name in self.test_types:
            print(f"Test type '{name}' already exists.")
            return

        # Validate input data
        try:
            min_range = float(min_range) if min_range else None
            max_range = float(max_range) if max_range else None
            if min_range is not None and max_range is not None and min_range >= max_range:
                raise ValueError("Minimum range should be less than maximum range.")

            if not re.match(r"\d{2}-\d{2}-\d{2}", turnaround_time):
                raise ValueError("Turnaround time must be in the format DD-hh-mm.")

            # Add the new test type
            new_test_type = MedicalTestType(name, (min_range, max_range), unit, turnaround_time)
            self.test_types[name] = new_test_type

            # Save the new test type to the file
            with open(self.file_name, 'a') as file:
                range_str = self.format_range(new_test_type.normal_range)
                file.write(f"Name: {new_test_type.name}; Range: {range_str}; unit: {new_test_type.unit}, {new_test_type.turnaround_time}\n")

            print(f"New test type '{name}' added successfully.")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
    def update_test_type(self):
        test_name = input("Enter the name of the test type to update (exactly as in the file): ").strip()

        # Load current test types from the file
        with open(self.file_name, 'r') as file:
            lines = file.readlines()
        
        updated = False
        new_lines = []
        
        for line in lines:
            line_strip = line.strip()
            if line_strip.startswith(f"Name: {test_name}"):
                print(f"Existing record: {line_strip}")
                
                # Extract existing details
                name_match = re.search(r'Name: (.*?);', line_strip)
                range_match = re.search(r'Range: (.*?);', line_strip)
                unit_match = re.search(r'Unit: (.*?)(,|$)', line_strip)
                turnaround_time_match = re.search(r'(?:Unit: .*?, )(\d{2}-\d{2}-\d{2}[A-Z]?)$', line_strip)
                
                if name_match:
                    name_part = name_match.group(1).strip()
                else:
                    name_part = test_name
                
                if range_match:
                    range_part = range_match.group(1).strip()
                    min_range_match = re.search(r'> ([0-9.]+)', range_part)
                    max_range_match = re.search(r'< ([0-9.]+)', range_part)
                    min_range = min_range_match.group(1) if min_range_match else "0"
                    max_range = max_range_match.group(1) if max_range_match else ""
                else:
                    range_part = "Range: > , < "
                    min_range, max_range = "0", ""
                
                if unit_match:
                    unit_part = unit_match.group(1).strip()
                else:
                    unit_part = ""
                
                if turnaround_time_match:
                    turnaround_time_part = turnaround_time_match.group(1).strip()
                else:
                    turnaround_time_part = ""
                
                # Prompt for new values
                new_name = input(f"Enter new name (current: {name_part}): ").strip() or name_part
                while True:
                    new_min_range = input(f"Enter new minimum range (current: {min_range}): ").strip() or min_range
                    new_max_range = input(f"Enter new maximum range (current: {max_range}): ").strip() or max_range
                    if new_min_range and new_max_range:
                        try:
                            new_min_range = float(new_min_range) if new_min_range else 0
                            new_max_range = float(new_max_range) if new_max_range else float('inf')
                            if new_min_range > new_max_range:
                                print("Error: Minimum range cannot be greater than maximum range. Please enter the values again.")
                            else:
                                break
                        except ValueError:
                            print("Error: Invalid number format. Please enter numeric values for ranges.")
                    else:
                        new_min_range = 0  # Default to 0 if the input is empty
                        new_max_range = float('inf')  # Default to infinity if the input is empty
                
                new_unit = input(f"Enter new unit (current: {unit_part}): ").strip() or unit_part
                new_turnaround_time = input(f"Enter new turnaround time (current: {turnaround_time_part}) (DD-hh-mm): ") or turnaround_time_part
                
                # Construct new range part
                new_range = f"Range: > {new_min_range}, < {new_max_range}"
                
                # Construct new line
                new_line = f"Name: {new_name}; {new_range}; Unit: {new_unit}"
                if new_turnaround_time:
                    new_line += f", {new_turnaround_time}"
                new_line += "\n"
                
                new_lines.append(new_line)
                updated = True
            else:
                new_lines.append(line)
        
        if updated:
            with open(self.file_name, 'w') as file:
                file.writelines(new_lines)
            print(f"Test type '{test_name}' updated successfully.")
        else:
            print(f"No matching test type found to update.")
class MedicalRecordSystem:
    def __init__(self):
        self.status_options = ['Pending', 'Completed', 'Reviewed']

    def retrieve_abnormal_tests(self):
        abnormal_tests = []  # Store abnormal test records
        test_names = {}

        # Read medicalTest.txt and extract test names with their ranges
        with open('medicalTest.txt', 'r') as medical_test_file:
            current_test_name = None
            for line in medical_test_file:
                if "Name: " in line:
                    test_name_match = re.search(r'Name: .*\((.*?)\)', line)
                    if test_name_match:
                        current_test_name = test_name_match.group(1).strip()
                        test_names[current_test_name] = {}

                if current_test_name:  # Ensure that the test name was found before proceeding
                    min_range_match = re.search(r'Range: > ([0-9.]+)', line)
                    max_range_match = re.search(r'< ([0-9.]+)', line)
                    
                    if min_range_match:
                        test_names[current_test_name]['min'] = float(min_range_match.group(1))
                    else:
                        test_names[current_test_name]['min'] = 0  # Default min range

                    if max_range_match:
                        test_names[current_test_name]['max'] = float(max_range_match.group(1))
                    else:
                        test_names[current_test_name]['max'] = float('inf')  # Default max range

        # Read medicalRecord.txt and search for abnormal results
        with open('midecalRecord.txt', 'r') as medical_record_file:
            for line in medical_record_file:
                # Split the line into the patient ID part and the rest of the record
                parts = line.split(':', 1)
                if len(parts) == 2:  # Ensure the line was split correctly
                    patient_id_part, record_part = parts
                    # Now split the rest of the record by commas
                    record = [x.strip() for x in record_part.split(',')]
                    if len(record) == 5:
                        test_name, test_date, value, unit, status = record
                        value = float(re.sub(r'[^\d.]', '', value))  # Clean value to convert to float

                        # Check if the test is in test_names and if the value is abnormal
                        for test_name_key, ranges in test_names.items():
                            if test_name_key.lower() in test_name.lower():  # Match test name case-insensitively
                                if value < ranges['min'] or value > ranges['max']:
                                    abnormal_tests.append(line.strip())  # Add abnormal test to the list
                                break  # No need to check other tests if one matches

        return abnormal_tests  # Return the list of abnormal tests


    def import_from_csv(self):
        if not os.path.exists("medical_records.csv"):
            print("The file 'medical_records.csv' does not exist.")
            return

        with open("medical_records.csv", "r") as csv_file:
            lines = csv_file.readlines()
            with open("midecalRecord.txt", "w") as file:
                for line in lines[1:]:  # skip the header line
                    parts = line.strip().split(",")
                    if len(parts) >= 7:
                        record_id, record_name, record_datetime, result, unit, record_status, result_datetime = parts[:7]
                        if record_status == "Completed":
                            file.write(
                                f"{record_id}: {record_name}, {record_datetime}, {result}, {unit}, {record_status}, {result_datetime}\n")
                        else:
                            file.write(
                                f"{record_id}: {record_name}, {record_datetime}, {result}, {unit}, {record_status}\n")

        print("Medical records imported from medical_records.csv successfully.")

    def parse_turnaround_time(self, time_str):
        """Convert time string (HH:MM) to a datetime object."""
        try:
            return datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            return None  # Return None if parsing fails

    def filter_medical_tests(self):
        filters = {}

        # Get filter criteria from user
        print("Enter filter criteria (press Enter to skip):")
        filters["patient_id"] = input("Patient ID: ")
        filters["test_name"] = input("Test Name: ")
        filters["abnormal"] = input("Show abnormal tests only? (yes/no): ").lower() == "yes"
        filters["start_date"] = input("Start Date (YYYY-MM-DD): ")
        filters["end_date"] = input("End Date (YYYY-MM-DD): ")
        filters["test_status"] = input("Test Status: ")
        filters["min_time"] = input("Minimum Execution Time (HH:MM): ")
        filters["max_time"] = input("Maximum Execution Time (HH:MM): ")

        abnormal_tests = []  # List to hold abnormal tests

        # If filtering by abnormal tests, use retrieve_abnormal_tests function
        if filters.get("abnormal"):
            abnormal_tests = self.retrieve_abnormal_tests()  # Get abnormal tests list

        # Normalize execution times from user input
        min_time = self.parse_turnaround_time(filters["min_time"]) if filters.get("min_time") else None
        max_time = self.parse_turnaround_time(filters["max_time"]) if filters.get("max_time") else None

        # Filter medical tests
        filtered_tests = []
        with open("midecalRecord.txt", "r") as file:
            for line in file:
                parts = line.strip().split(": ")
                if len(parts) > 1:
                    record_id, record_details = parts
                    details_parts = record_details.split(", ")
                    if len(details_parts) >= 5:
                        record_name, record_datetime, result, unit, record_status = details_parts[:5]

                        # Extract the time from the record_datetime (HH:MM)
                        record_time_str = record_datetime.split(" ")[1]
                        record_time = self.parse_turnaround_time(record_time_str)

                        # Apply filters
                        filter_conditions = [
                            (filters.get("patient_id") == record_id if filters.get("patient_id") else True),
                            (filters.get("test_name") == record_name if filters.get("test_name") else True),
                            ((filters.get("start_date") <= record_datetime.split(" ")[0] <= filters.get("end_date")) if filters.get("start_date") and filters.get("end_date") else True),
                            (filters.get("test_status") == record_status if filters.get("test_status") else True),
                        ]

                        # If filtering by abnormal tests, check if this test is in the abnormal tests list
                        if filters.get("abnormal"):
                            filter_conditions.append(line.strip() in abnormal_tests)

                        # Check execution time against user-provided limits
                        if min_time or max_time:
                            min_time = min_time if min_time else datetime.strptime("00:00", "%H:%M").time()
                            max_time = max_time if max_time else datetime.strptime("23:59", "%H:%M").time()

                            if not (min_time <= record_time <= max_time):
                                filter_conditions.append(False)

                        # If all conditions are met, add to filtered tests
                        if all(filter_conditions):
                            filtered_tests.append({
                                "line": line.strip(),
                                "result": float(result),
                                "execution_time": record_time
                            })

        # Display filtered tests
        if filtered_tests:
            print("Filtered medical tests:")
            for test in filtered_tests:
                print(test["line"])

            # Generate summary statistics
            test_values = [test["result"] for test in filtered_tests]
            min_value = min(test_values)
            max_value = max(test_values)
            avg_value = sum(test_values) / len(test_values)

            execution_times = [test["execution_time"] for test in filtered_tests if test["execution_time"]]
            if execution_times:
                min_time = min(execution_times)
                max_time = max(execution_times)
                avg_time = (
                    sum(t.hour for t in execution_times) // len(execution_times),
                    sum(t.minute for t in execution_times) // len(execution_times)
                )

                print(f"\nSummary Statistics:")
                print(f"Minimum Test Value: {min_value}")
                print(f"Maximum Test Value: {max_value}")
                print(f"Average Test Value: {avg_value}")
                print(f"Minimum Execution Time: {min_time.strftime('%H:%M')}")
                print(f"Maximum Execution Time: {max_time.strftime('%H:%M')}")
                print(f"Average Execution Time: {avg_time[0]:02}:{avg_time[1]:02}")
            else:
                print(f"\nSummary Statistics:")
                print(f"Minimum Test Value: {min_value}")
                print(f"Maximum Test Value: {max_value}")
                print(f"Average Test Value: {avg_value}")
        else:
            print("No records found matching the given criteria.")

    def export_to_csv(self):
        if not os.path.exists("midecalRecord.txt"):
            print("The file 'midecalRecord.txt' does not exist.")
            return

        with open("midecalRecord.txt", "r") as file:
            lines = file.readlines()
            with open("medical_records.csv", "w") as csv_file:
                csv_file.write("Patient ID,Test Name,Test Date,Result,Unit,Status,Result Date\n")
                for line in lines:
                    parts = line.strip().split(": ")
                    if len(parts) > 1:
                        record_id, record_details = parts
                        details_parts = record_details.split(", ")
                        if len(details_parts) >= 5:
                            record_name, record_datetime, result, unit, record_status = details_parts[:5]
                            result_datetime = "" if record_status != "Completed" else details_parts[:5]
                            csv_file.write(
                                f"{record_id},{record_name},{record_datetime},{result},{unit},{record_status},{result_datetime}\n")

        print("Medical records exported to medical_records.csv successfully.")

    def add_new_test_type(self, name, min_range, max_range, unit, turnaround_time):
        # Validate input data
        try:
            min_range = float(min_range)
            max_range = float(max_range)
            if min_range >= max_range:
                raise ValueError("Minimum range should be less than maximum range.")

            if not re.match(r"\d{2}-\d{2}-\d{2}", turnaround_time):
                raise ValueError("Turnaround time must be in the format DD-hh-mm.")

            # Add the new test type
            new_test_type = MedicalTestType(name, (min_range, max_range), unit, turnaround_time)
            self.save_test_type(new_test_type)
            print(f"New test type '{name}' added successfully.")

        except ValueError as e:
            print(f"Error: {e}")

    def add_new_test_record(self):
        patient_id = input("Enter patient ID (7 digits): ").strip()
        if not (patient_id.isdigit() and len(patient_id) == 7):
            print("Invalid patient ID. Please enter exactly 7 digits.")
            return

        test_name = input("Enter test name (with length less than 20 characters): ").strip()
        if len(test_name) > 20:
            print("Test name too long. Maximum length is 20 characters.")
            return

        test_datetime = input("Enter test date and time (YYYY-MM-DD hh:mm): ").strip()
        try:
            datetime.strptime(test_datetime, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid date and time format. Please enter YYYY-MM-DD hh:mm format.")
            return

        result = input("Enter test result (floating point): ").strip()
        if not re.match(r"^[0-9]*\.?[0-9]+$", result):
            print("Invalid result format. Please enter a floating point number.")
            return

        unit = input("Enter test result unit: ").strip()

        status = input("Enter test status (Pending, Completed, Reviewed): ").strip().capitalize()
        if status not in self.status_options:
            print("Invalid status entered.")
            return

        result_datetime = ""
        if status == "Completed":
            result_datetime = input("Enter result date and time (YYYY-MM-DD hh:mm): ").strip()
            try:
                datetime.strptime(result_datetime, "%Y-%m-%d %H:%M")
            except ValueError:
                print("Invalid result date and time format. Please enter YYYY-MM-DD hh:mm format.")
                return

        record = MedicalTestRecord(patient_id, test_name, test_datetime, result, unit, status, result_datetime)
        record.save()


    def update_test_result(self):
        patient_id = input("Enter patient ID (7 digits) to update: ").strip()
        if not (patient_id.isdigit() and len(patient_id) == 7):
            print("Invalid patient ID. Please enter exactly 7 digits.")
            return

        test_name = input("Enter test name to update (with length less than 20 characters): ").strip()
        if len(test_name) > 20:
            print("Test name too long. Maximum length is 20 characters.")
            return

        test_datetime = input("Enter test date and time (YYYY-MM-DD hh:mm): ").strip()
        try:
            datetime.strptime(test_datetime, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid date and time format. Please enter YYYY-MM-DD hh:mm format.")
            return

        updated = False
        new_lines = []
        with open("midecalRecord.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                line_strip = line.strip()
                parts = line_strip.split(": ", 1)
                if len(parts) > 1:
                    record_id, record_details = parts
                    if record_id == patient_id:
                        details_parts = record_details.split(", ")
                        if len(details_parts) >= 5:
                            record_name, record_datetime, _, _, record_status = details_parts[:5]
                            if record_name == test_name and record_datetime == test_datetime:
                                print(f"Existing record: {line_strip}")
                                result = input("Enter new test result (floating point): ").strip()
                                if not re.match(r"^[0-9]*\.?[0-9]+$", result):
                                    print("Invalid result format. Update aborted.")
                                    return

                                unit = input("Enter new test result unit: ").strip()
                                status = input(
                                    "Enter new test status: (Pending, Completed, Reviewed) ").strip().capitalize()
                                if status not in self.status_options:
                                    print("Invalid status entered. Update aborted.")
                                    return

                                if status == "Completed":
                                    result_datetime = input(
                                        "Enter new result date and time (YYYY-MM-DD hh:mm): ").strip()
                                    try:
                                        datetime.strptime(result_datetime, "%Y-%m-%d %H:%M")
                                    except ValueError:
                                        print("Invalid result date and time format. Update failed.")
                                        return
                                    new_line = f"{patient_id}: {test_name}, {test_datetime}, {result}, {unit}, {status}, {result_datetime}\n"
                                else:
                                    new_line = f"{patient_id}: {test_name}, {test_datetime}, {result}, {unit}, {status}\n"

                                new_lines.append(new_line)
                                updated = True
                                continue
                new_lines.append(line)

        if updated:
            with open("midecalRecord.txt", "w") as file:
                file.writelines(new_lines)
            print("The test record has been updated.\n")
        else:
            print("No matching record found to update.\n")
            file.close

   
   
   
   
   
   
   
   
   
   
    """ def generate_summary(self, test_name):
        filtered_records = [record for record in self.records if record['test_name'] == test_name]

        if not filtered_records:
            print(f"No records found for test '{test_name}'.")
            return

        test_values = [record['test_value'] for record in filtered_records]

        min_value = min(test_values)
        max_value = max(test_values)
        avg_value = sum(test_values) / len(test_values)

        print(f"Summary for {test_name}:")
        print(f"Minimum Value: {min_value}")
        print(f"Maximum Value: {max_value}")
        print(f"Average Value: {avg_value:.2f}")"""

# Example usage:
medical_system = MedicalRecordSystem()
manager = MedicalTestTypeManager()  # Create an instance of the manager
manager.load_test_types()  # Load existing test types from the file 

while True:
    print("\nMain Menu:")
    print("1- Add new medical test.")
    print("2- Add a new test record.")
    print("3- Update patient records including all fields.")
    print("4- Update medical tests in the medicalTest file.")
    print("5- Filter medical tests.")
    print("6- Export medical records to a comma separated file.")
    print("7- Import medical records from a comma separated file.")
    print("8- Exit.\n")

    choice = input("Enter operation number: ").strip()

    if choice == '1':
        # Add new medical test: the system will allow user to insert new type of medical test and save it in
        # the medicalTest file. The system will check the validity of the input data.
        name = input("Enter the test name: ")
        min_range = input("Enter the minimum normal range value: ")
        max_range = input("Enter the maximum normal range value: ")
        unit = input("Enter the unit of measurement: ")
        turnaround_time = input("Enter the turnaround time (DD-hh-mm): ")

        # Attempt to add the new test type with the provided input
        manager.add_new_test_type(name, min_range, max_range, unit, turnaround_time)




    elif choice == '2':
        # Add a new medical test record: the system will allow the user to store a new medical test with the
        # required data. The system will check the validity of the input data.
        medical_system.add_new_test_record()


    elif choice == '3':
        # Update patient records including all fields.
        medical_system.update_test_result()

    elif choice == '4':
       
        
        manager.update_test_type()  # Pass the string to the method
        
    
    elif choice == '5':
        # Filter medical tests.
        medical_system.filter_medical_tests()
        
    elif choice == '6':
        # Export medical records to a comma separated file,
        medical_system.export_to_csv()
    elif choice == '7':
        # Import medical records from a comma separated file.
        medical_system.import_from_csv()
    elif choice == '8':
        print("thank you for using our programm")
     
        break
    else:
        print("Invalid choice. Please select from the menu options.")
