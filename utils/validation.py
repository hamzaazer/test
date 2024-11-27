from typing import Dict, Any, List

def validate_student_data(data: Dict[str, Any]) -> List[str]:
    errors = []
    
    if not data.get('first_name'):
        errors.append("First name is required")
    if not data.get('last_name'):
        errors.append("Last name is required")
    if not data.get('student_id'):
        errors.append("Student ID is required")
    if not data.get('academic_year'):
        errors.append("Academic year is required")
    try:
        if data.get('academic_year'):
            year = int(data['academic_year'])
            if year < 1 or year > 6:
                errors.append("Academic year must be between 1 and 6")
    except ValueError:
        errors.append("Academic year must be a number")
    
    return errors

def validate_grade_data(data: Dict[str, Any]) -> List[str]:
    errors = []
    
    if not data.get('subject'):
        errors.append("Subject is required")
    if not data.get('score'):
        errors.append("Score is required")
    try:
        if data.get('score'):
            score = float(data['score'])
            if score < 0 or score > 100:
                errors.append("Score must be between 0 and 100")
    except ValueError:
        errors.append("Score must be a number")
    
    return errors

def validate_attendance_data(data: Dict[str, Any]) -> List[str]:
    errors = []
    
    if not data.get('date'):
        errors.append("Date is required")
    if not data.get('status'):
        errors.append("Status is required")
    if data.get('status') and data['status'] not in ['Present', 'Absent', 'Late']:
        errors.append("Invalid status value")
    
    return errors