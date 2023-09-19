from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

questions_and_answers = {
    "you": {
        "question_number": 1,
        "question_code": "you",
        "question":
        "%E4%B8%8B%E4%B8%80%E5%80%8B%E6%9C%88%E7%9A%84%E5%A3%BD%E6%98%9F%E6%98%AF%E8%AA%B0",
        "answer": "ink",
        "next_question_code": "are",
        "template": "question_template.html"
    },
    "are": {
        "question_number": 2,
        "question_code": "are",
        "question": "Caesar says: Phrz-phrz'v fdwfkskudvh.",
        "answer": "此時此刻",
        "next_question_code": "my",
        "template": "question_template.html"
    },
    "my": {
        "question_number": 3,
        "question_code": "my",
        "question": "",
        "hidden_question": "誰跟我們共享辦公室",
        "answer": "饌元",
        "next_question_code": "fire",
        "template": "question_template.html"
    },
    "fire": {
        "question_number": 4,
        "question_code": "fire",
        "question": "g;4p y94b41p31o4w. 2k7g.31ul3yjo4c.4fm4xk7s83xu3",
        "answer": "菲律賓",
        "next_question_code": "the",
        "template": "question_template.html"
    },
    "the": {
        "question_number": 5,
        "question_code": "the",
        "question":
        "在處成家春复秋，嚇春未必多煙雨。\n鼠況今朝杏園裡。人生貴賤那得知。\n事與浮雲去絕踪，件榮富壽難兼得。\n裡漏三聲燭半條，誰人嗟此樂難當。\n給山當面照銀鉤，小樓吹徹玉笙寒。\n老僧倚杖青松側，鼠河落天走東海。\n最愛梅花蘸水香，後取三千世界來。\n一曲風飄海頭滿，擊苑春衫細細風。",
        "answer": "hong",
        "next_question_code": "one",
        "template": "question_template.html"
    },
    "one": {
        "question_number":
        6,
        "question_code":
        "one",
        "question":
        "In a world of uncertainties, where time slips away," +
        "The sun rises, and a new day comes into play. " +
        "Steven, a name known in the company, they say," +
        "Oversleeping, an incident that caused dismay. " +
        "Incident after incident, life presents challenges. " +
        "Who would have known, as the morning turned gray," +
        "Called the office, with news that led the way. " +
        "The mystery unraveling, like a puzzle at bay," +
        "Company, determined to find truth, no delay." +
        "To discover the answers, they'd work night and day, " +
        "Discover the truth, they must, without delay. " +
        "Steven's absence, a riddle they'd repay. " +
        "Unexplained, yet a story in the company's array, " +
        "Absence, a chapter they'd remember, come what may.",
        "answer":
        "媽媽",
        "next_question_code":
        "desire",
        "template":
        "question_template.html"
    },
    "desire": {
        "question_number": 7,
        "question_code": "desire",
        "question":
        "- .... . / --- -. .-.. -.-- / .-. . -.-. --- -- -- . -. -.. . -.. / .-- . -... ... .. - . / ..-. --- .-. / . -. --. .-.. .. ... .... / .--. .-. --- -. ..- -. -.-. .. .- - .. --- -.",
        "answer": "youglish",
        "next_question_code": "believe",
        "template": "question_template.html"
    },
    "believe": {
        "question_number": 8,
        "question_code": "believe",
        "question_img_path": "/static/images/q8.png",
        "answer": "我喜歡你",
        "next_question_code": "when",
        "template": "question_template.html"
    },
    "when": {
        "question_number": 9,
        "question_code": "when",
        "question_autdio_path": "/static/q9.mp3",
        "answer": "9",
        "next_question_code": "i",
        "template": "question_template.html"
    },
    "i": {
        "question_number": 10,
        "question_code": "i",
        "question_img_path": "/static/images/zipped_heijin.jpeg",
        "answer": "哇靠林董有槍啊",
        "next_question_code": "say",
        "template": "question_template.html"
    },
    "say": {
        "question_number": 11,
        "question_code": "say",
        "question": "所有的題目串起了一首歌曲\n請唱出下一句歌詞",
        "answer": "I want it that way",
        "next_question_code": "final",
        "template": "question_template.html"
    },
    "final": {
        "question_number": 12,
        "template": "final.html"
    }
}


@app.get("/you", response_class=HTMLResponse)
@app.get("/are", response_class=HTMLResponse)
@app.get("/my", response_class=HTMLResponse)
@app.get("/fire", response_class=HTMLResponse)
@app.get("/the", response_class=HTMLResponse)
@app.get("/one", response_class=HTMLResponse)
@app.get("/desire", response_class=HTMLResponse)
@app.get("/believe", response_class=HTMLResponse)
@app.get("/when", response_class=HTMLResponse)
@app.get("/i", response_class=HTMLResponse)
@app.get("/say", response_class=HTMLResponse)
@app.get("/final", response_class=HTMLResponse)
def read_item(request: Request, hint: str = None):
    path_segments = request.url.path.split("/")
    question_code = path_segments[-1]
    question = questions_and_answers[question_code]

    question['request'] = request

    if hint is not None:
        question['hint'] = hint

    return templates.TemplateResponse(question['template'], question)


@app.post("/submit_answer/")
def submit_answer(answer: str = Form(...), question_code: str = Form(...)):
    question = questions_and_answers[question_code]
    if question["answer"] == answer:
        return RedirectResponse(url=f"/{question['next_question_code']}",
                                status_code=303)
    else:
        return RedirectResponse(url=f"/{question['question_code']}?hint=答错了",
                                status_code=303)