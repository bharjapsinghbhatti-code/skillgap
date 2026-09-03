from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from engine.recommendation_engine import SkillGapEngine
from engine.roadmap_engine import RoadmapEngine


# =========================================================
# APP
# =========================================================

app = FastAPI(
    title="SkillGap API",
    description="Career skill gap recommendation engine",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://skillgap-1-3fki.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# ENGINES
# =========================================================

engine = SkillGapEngine()
roadmap_engine = RoadmapEngine()


# =========================================================
# REQUEST MODEL
# =========================================================

class RecommendationRequest(BaseModel):
    current_level: str
    target_level: str
    target_role: str
    skills: dict[str, int]


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return {
        "message": "SkillGap API is running",
        "status": "ok"
    }


# =========================================================
# AVAILABLE SKILLS
# =========================================================

@app.get("/skills")
def get_skills():

    return {
        "skills": engine.get_skills()
    }


# =========================================================
# RECOMMENDATION
# =========================================================

@app.post("/recommend")
def recommend(request: RecommendationRequest):

    try:

        # -------------------------------------------------
        # RUN EXISTING RECOMMENDATION ENGINE
        # -------------------------------------------------

        results = engine.recommend(
            current_skills=request.skills,
            current_level=request.current_level,
            target_level=request.target_level
        )


        # -------------------------------------------------
        # PREPARE ROADMAP INPUT
        # -------------------------------------------------

        recommended_skills = []

        for category in [
            "core",
            "growth",
            "specialized"
        ]:

            dataframe = results.get(category)

            if dataframe is None or dataframe.empty:
                continue


            for _, row in dataframe.iterrows():

                recommended_skills.append({

                    "canonical_skill":
                        row["canonical_skill"],

                    "priority":
                        row["priority"],

                    "priority_score":
                        float(
                            row["priority_score"]
                        )

                })


        # -------------------------------------------------
        # SORT BY PRIORITY SCORE
        # -------------------------------------------------

        recommended_skills = sorted(
            recommended_skills,
            key=lambda x: x["priority_score"],
            reverse=True
        )


        # -------------------------------------------------
        # BUILD 90-DAY ROADMAP
        # -------------------------------------------------

        roadmap = roadmap_engine.build_roadmap(
            recommended_skills[:5]
        )


        # -------------------------------------------------
        # FORMAT RECOMMENDATION RESULTS
        # -------------------------------------------------

        def format_results(dataframe):

            if dataframe is None or dataframe.empty:
                return []


            records = []


            for _, row in dataframe.iterrows():

                level = int(
                    row["current_skill_level"]
                )


                # -----------------------------------------
                # SKILL LEVEL LABEL
                # -----------------------------------------

                if level == 0:

                    skill_label = "None"

                elif level == 1:

                    skill_label = "Beginner"

                elif level == 2:

                    skill_label = "Intermediate"

                else:

                    skill_label = "Advanced"


                records.append({

                    "canonical_skill":
                        row["canonical_skill"],

                    "priority_score":
                        round(
                            float(
                                row["priority_score"]
                            ),
                            2
                        ),

                    "priority":
                        row["priority"],

                    "current_skill_level":
                        level,

                    "current_skill_label":
                        skill_label,

                    "target_level":
                        request.target_level,

                    "skill_gap":
                        round(
                            float(
                                row["skill_gap"]
                            ),
                            2
                        ),

                    "demand_percentage":
                        round(
                            float(
                                row["demand_percentage"]
                            ),
                            2
                        ),

                    "career_growth":
                        round(
                            float(
                                row["career_growth"]
                            ),
                            2
                        ),

                    "reason":
                        row["reason"]

                })


            return records


        # -------------------------------------------------
        # FINAL RESPONSE
        # -------------------------------------------------

        return {

            "current_level":
                request.current_level,

            "target_level":
                request.target_level,

            "target_role":
                request.target_role,

            "core":
                format_results(
                    results["core"]
                ),

            "growth":
                format_results(
                    results["growth"]
                ),

            "specialized":
                format_results(
                    results["specialized"]
                ),

            "roadmap":
                roadmap

        }


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


