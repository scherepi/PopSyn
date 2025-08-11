from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from lyrics import getLyrics
from analysis import getColor


app = FastAPI(title="PopSyn API", version="0.1.0")

# Allow requests from any origin (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    artist: str
    title: str


class AnalyzeResponse(BaseModel):
    artist: str
    title: str
    lyrics: Optional[str]
    color_hex: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_song(payload: AnalyzeRequest):
    try:
        normalized_artist, normalized_title, lyrics = getLyrics(
            payload.artist, payload.title
        )
        if not lyrics:
            raise HTTPException(status_code=404, detail="Lyrics not found")
        color_hex = getColor(lyrics)
        return AnalyzeResponse(
            artist=normalized_artist,
            title=normalized_title,
            lyrics=lyrics,
            color_hex=color_hex,
        )
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001 - propagate as HTTP 400
        raise HTTPException(status_code=400, detail=str(exc)) from exc

