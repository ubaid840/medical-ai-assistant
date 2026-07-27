from database import get_connection

def create_patient_profile(name, age, gender, chronic_conditions, allergies, medications):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patient_profiles (name, age, gender, chronic_conditions, allergies, medications)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, age, gender, chronic_conditions, allergies, medications))
    conn.commit()
    patient_id = cursor.lastrowid
    conn.close()
    return patient_id

def get_all_patients():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patient_profiles ORDER BY name ASC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_patient(patient_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patient_profiles WHERE id = ?", (patient_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_patient_profile(patient_id, name, age, gender, chronic_conditions, allergies, medications):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE patient_profiles
        SET name = ?, age = ?, gender = ?, chronic_conditions = ?, allergies = ?, medications = ?
        WHERE id = ?
    """, (name, age, gender, chronic_conditions, allergies, medications, patient_id))
    conn.commit()
    conn.close()

def delete_patient(patient_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patient_profiles WHERE id = ?", (patient_id,))
    conn.commit()
    conn.close()

def format_patient_context(patient_id):
    patient = get_patient(patient_id)
    if not patient:
        return ""
    
    context = f"**Patient Profile Context:**\n"
    context += f"- Name: {patient['name']}\n"
    if patient['age']: context += f"- Age: {patient['age']}\n"
    if patient['gender']: context += f"- Gender: {patient['gender']}\n"
    if patient['chronic_conditions']: context += f"- Chronic Conditions: {patient['chronic_conditions']}\n"
    if patient['allergies']: context += f"- Allergies: {patient['allergies']}\n"
    if patient['medications']: context += f"- Current Medications: {patient['medications']}\n"
    
    return context
