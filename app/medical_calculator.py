
def calculate_bmi(weight_kg, height_m):
    try:
        bmi = weight_kg / (height_m ** 2)
        status = "Normal"
        if bmi < 18.5: status = "Underweight"
        elif bmi >= 25 and bmi < 30: status = "Overweight"
        elif bmi >= 30: status = "Obese"
        return f"BMI is {bmi:.1f} ({status})"
    except Exception as e:
        return f"Error calculating BMI: {e}"

def calculate_map(systolic, diastolic):
    try:
        map_val = (systolic + 2 * diastolic) / 3
        return f"Mean Arterial Pressure (MAP) is {map_val:.1f} mmHg"
    except Exception as e:
        return f"Error calculating MAP: {e}"

def calculate_egfr(creatinine, age, is_female, is_black):
    # Simplified MDRD formula
    try:
        kappa = 0.7 if is_female else 0.9
        alpha = -0.329 if is_female else -0.411
        min_val = min(creatinine / kappa, 1)
        max_val = max(creatinine / kappa, 1)
        
        # CKD-EPI 2021 (simplified, without race coefficient as per new guidelines)
        egfr = 142 * (min_val ** alpha) * (max_val ** -1.200) * (0.9938 ** age)
        if is_female: egfr *= 1.012
        
        return f"eGFR (CKD-EPI 2021) is {egfr:.1f} mL/min/1.73m²"
    except Exception as e:
        return f"Error calculating eGFR: {e}"
