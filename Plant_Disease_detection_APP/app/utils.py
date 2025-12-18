import re


# ==========================================================
# CLEAN & NORMALIZE
# ==========================================================

def clean_name(x: str) -> str:
    """
    Convert model class name into readable text
    Example:
    Grape___Esca_(Black_Measles) → Grape Esca (Black Measles)
    """
    return x.replace("___", " ").replace("_", " ").strip()


def normalize(text: str) -> str:
    """
    Strong normalization for reliable matching
    Removes brackets, commas, hyphens, etc.
    """
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ==========================================================
# RISK FROM CONFIDENCE
# ==========================================================

def risk_from_prob(p: float) -> str:
    if p >= 0.75:
        return "High"
    elif p >= 0.4:
        return "Medium"
    else:
        return "Low"


def risk_explanation(p: float) -> str:
    if p >= 0.75:
        return "High risk: Strong visual symptoms detected. Immediate action recommended."
    elif p >= 0.4:
        return "Moderate risk: Symptoms present. Monitor and treat if condition worsens."
    else:
        return "Low risk: Weak symptoms detected. Observation advised."


# ==========================================================
# FULL PLANTVILLAGE DISEASE DATABASE (MATCHES YOUR CLASSES)
# ==========================================================

DISEASE_DB = {
    # 🍎 APPLE
    "apple apple scab": (
        "Apple scab detected. Fungal disease causing dark leaf spots.",
        "Apply fungicide and remove fallen leaves."
    ),
    "apple black rot": (
        "Apple black rot detected. Causes fruit and leaf decay.",
        "Prune infected areas and apply fungicide."
    ),
    "apple cedar apple rust": (
        "Cedar apple rust detected. Orange rust lesions on leaves.",
        "Remove nearby cedar trees and apply fungicide."
    ),
    "apple healthy": (
        "Healthy apple leaf detected.",
        "No treatment required."
    ),

    # 🫐 BLUEBERRY
    "blueberry healthy": (
        "Healthy blueberry leaf detected.",
        "No treatment required."
    ),

    # 🍒 CHERRY
    "cherry powdery mildew": (
        "Powdery mildew detected on cherry leaf.",
        "Improve air circulation and apply fungicide."
    ),
    "cherry healthy": (
        "Healthy cherry leaf detected.",
        "No treatment required."
    ),

    # 🌽 CORN
    "corn maize cercospora leaf spot gray leaf spot": (
        "Gray leaf spot detected. Fungal disease in maize.",
        "Use resistant varieties and fungicide."
    ),
    "corn maize common rust": (
        "Common rust detected. Orange-brown pustules.",
        "Apply fungicide if severe."
    ),
    "corn maize northern leaf blight": (
        "Northern leaf blight detected.",
        "Remove crop debris and apply fungicide."
    ),
    "corn maize healthy": (
        "Healthy corn leaf detected.",
        "No treatment required."
    ),

    # 🍇 GRAPE
    "grape black rot": (
        "Grape black rot detected.",
        "Prune infected vines and apply fungicide."
    ),
    "grape esca black measles": (
        "Grape Esca (Black Measles) detected. Serious trunk disease.",
        "Prune infected wood and avoid vine stress."
    ),
    "grape leaf blight isariopsis leaf spot": (
        "Grape leaf blight detected.",
        "Apply fungicide and ensure good airflow."
    ),
    "grape healthy": (
        "Healthy grape leaf detected.",
        "No treatment required."
    ),

    # 🍊 ORANGE
    "orange haunglongbing citrus greening": (
        "Citrus greening disease detected. Very destructive disease.",
        "Remove infected trees and control insect vectors."
    ),

    # 🍑 PEACH
    "peach bacterial spot": (
        "Bacterial spot detected on peach leaf.",
        "Apply copper-based bactericide."
    ),
    "peach healthy": (
        "Healthy peach leaf detected.",
        "No treatment required."
    ),

    # 🌶️ PEPPER
    "pepper bell bacterial spot": (
        "Bacterial spot detected on pepper leaf.",
        "Avoid overhead watering and apply bactericide."
    ),
    "pepper bell healthy": (
        "Healthy pepper leaf detected.",
        "No treatment required."
    ),

    # 🥔 POTATO
    "potato early blight": (
        "Early blight detected on potato leaf.",
        "Apply fungicide and rotate crops."
    ),
    "potato late blight": (
        "Late blight detected. Highly destructive disease.",
        "Remove infected plants and apply fungicide immediately."
    ),
    "potato healthy": (
        "Healthy potato leaf detected.",
        "No treatment required."
    ),

    # 🍓 RASPBERRY
    "raspberry healthy": (
        "Healthy raspberry leaf detected.",
        "No treatment required."
    ),

    # 🌱 SOYBEAN
    "soybean healthy": (
        "Healthy soybean leaf detected.",
        "No treatment required."
    ),

    # 🎃 SQUASH
    "squash powdery mildew": (
        "Powdery mildew detected on squash leaf.",
        "Apply fungicide and improve airflow."
    ),

    # 🍓 STRAWBERRY
    "strawberry leaf scorch": (
        "Leaf scorch detected on strawberry leaf.",
        "Remove infected leaves and apply fungicide."
    ),
    "strawberry healthy": (
        "Healthy strawberry leaf detected.",
        "No treatment required."
    ),

    # 🍅 TOMATO
    "tomato bacterial spot": (
        "Bacterial spot detected on tomato leaf.",
        "Use disease-free seeds and apply bactericide."
    ),
    "tomato early blight": (
        "Early blight detected on tomato leaf.",
        "Remove infected leaves and apply fungicide."
    ),
    "tomato late blight": (
        "Late blight detected. Severe tomato disease.",
        "Apply fungicide immediately and destroy infected plants."
    ),
    "tomato leaf mold": (
        "Leaf mold detected on tomato leaf.",
        "Reduce humidity and apply fungicide."
    ),
    "tomato septoria leaf spot": (
        "Septoria leaf spot detected.",
        "Remove infected leaves and apply fungicide."
    ),
    "tomato spider mites two spotted spider mite": (
        "Spider mite infestation detected.",
        "Use neem oil or insecticidal soap."
    ),
    "tomato target spot": (
        "Target spot disease detected.",
        "Apply fungicide and remove affected leaves."
    ),
    "tomato tomato yellow leaf curl virus": (
        "Yellow leaf curl virus detected.",
        "Remove infected plants and control whiteflies."
    ),
    "tomato tomato mosaic virus": (
        "Tomato mosaic virus detected.",
        "Remove infected plants and disinfect tools."
    ),
    "tomato healthy": (
        "Healthy tomato leaf detected.",
        "No treatment required."
    ),
}


# ==========================================================
# REPORT GENERATOR (FINAL)
# ==========================================================

def generate_leaf_report(class_name: str):
    name = normalize(clean_name(class_name))

    for key, value in DISEASE_DB.items():
        if normalize(key) in name:
            return value

    return (
        "Plant disease detected based on visual symptoms.",
        "Consult an agricultural expert for targeted treatment."
    )
