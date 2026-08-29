from langchain_core.tools import tool


@tool
def get_employee_details(employee_id: int):
    """Get employee details using the employee ID."""

    employees = {
        101: {
            "employee_id": 101,
            "name": "Rahul",
            "department": "IT",
            "designation": "Software Engineer"
        },
        102: {
            "employee_id": 102,
            "name": "Priya",
            "department": "Finance",
            "designation": "Business Analyst"
        }
    }

    return employees.get(employee_id, "Employee not found")