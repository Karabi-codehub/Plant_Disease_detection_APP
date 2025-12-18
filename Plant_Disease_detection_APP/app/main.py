from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image
import io



from app.predict import predict_pil_image



app = FastAPI()



app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")






@app.get("/", response_class=HTMLResponse)
def home(request: Request):
   return templates.TemplateResponse("index.html", {"request": request})






@app.post("/predict")
async def predict(file: UploadFile = File(...)):
   image_bytes = await file.read()
   image = Image.open(io.BytesIO(image_bytes))
   return predict_pil_image(image)



