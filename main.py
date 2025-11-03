from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes.clinic_routes import router as clinic_router
from routes.auth_routes import router as auth_router  # New import
from routes.states_routes import router as state_router
import logging
import time



app = FastAPI(title="Clinic API")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("server.log"),  # saves logs in a file
        logging.StreamHandler()             # also prints to terminal
    ]
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    if "multipart/form-data" not in request.headers.get("content-type", ""):
        body = await request.body()
    else:
        body = b"<multipart skipped>"

    method = request.method
    url = request.url.path

    logging.info(f" {method} {url} - Body: {body.decode('utf-8') or 'EMPTY'} - Headers: {dict(request.headers)}")

    try:
        response = await call_next(request)
    except Exception as e:
        logging.exception(f" Error processing {method} {url}: {e}")
        raise

    process_time = (time.time() - start_time) * 1000
    logging.info(f" {method} {url} - Status: {response.status_code} - Time: {process_time:.2f} ms")

    return response

# CORS for Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with Flutter app URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])  # New
app.include_router(clinic_router, prefix="/clinics", tags=["clinics"])
app.include_router(state_router, prefix="/states", tags=["States"])


@app.get("/")
async def root():
    return {"message": "Clinic API is running"}