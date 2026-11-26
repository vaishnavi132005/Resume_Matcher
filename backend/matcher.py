from sentence_transformers import SentenceTransformer, util
from jobs import JOBS

_model = None
_job_vectors = None


def _load():
    global _model, _job_vectors
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        texts = [j["title"] + ". " + j["description"] + " Skills: " + ", ".join(j["skills"]) for j in JOBS]
        _job_vectors = _model.encode(texts, convert_to_tensor=True)
    return _model, _job_vectors


def rank_jobs(resume_text, resume_skills, years):
    model, job_vectors = _load()
    resume_vec = model.encode(resume_text[:3000], convert_to_tensor=True)
    sims = util.cos_sim(resume_vec, job_vectors)[0].tolist()
    have = {s.lower() for s in resume_skills}
    results = []
    for job, sim in zip(JOBS, sims):
        semantic = max(0.0, min(100.0, (sim - 0.10) / 0.50 * 100))
        needed = {s.lower() for s in job["skills"]}
        matched = [s for s in job["skills"] if s.lower() in have]
        missing = [s for s in job["skills"] if s.lower() not in have]
        skill_score = len(matched) / len(needed) * 100 if needed else 0
        if job["min_years"] == 0:
            exp_score = 100.0
        else:
            exp_score = min(100.0, years / job["min_years"] * 100)
        total = 0.50 * semantic + 0.35 * skill_score + 0.15 * exp_score
        results.append({
            **job,
            "score": round(total, 1),
            "breakdown": {
                "semantic": round(semantic, 1),
                "skills": round(skill_score, 1),
                "experience": round(exp_score, 1),
            },
            "matched": matched,
            "missing": missing,
        })
    results.sort(key=lambda r: r["score"], reverse=True)
    return results
