export class Tester {
    constructor(questions) {
        this.shuffled = this.shuffle(
            questions.map(
                (x) => {
                    return {
                        prompt: x[0],
                        splitPrompt: this.split(x[0]),
                        answer: x[1],
                        cleaned: this.cleanAnswers(this.split(x[1])),
                    };
                },
            ),
        );
        this.promptTimeout = null;
        this.currentIndex = 0;
        this.promptIndex = 0;
        this.currentQuestion = null;
        document.addEventListener("DOMContentLoaded", () => this.init());
    }

    checkAnswer(isEnter) {
        if (this.promptTimeout) {
            clearTimeout(this.promptTimeout);
            this.promptTimeout = null;
        }
        this.showFeedback("");
        let a = this.el.answer.value;
        if (a.includes("?")) {
            this.showFeedback("Enter answer '" + this.currentQuestion.answer + "' to continue");
            this.el.answer.value = a.replace("?", "");
            return;
        }
        if (a.includes("/")) {
            this.shiftPrompt();
            this.el.answer.value = a.replace("/", "");
            return;
        }
        a = this.cleanAnswer(a);
        if (this.currentQuestion.cleaned.includes(a)) {
            this.shiftAnswer(false);
            return;
        }
        if (isEnter) {
            this.showFeedback("Incorrect. Try again.");
            return;
        }
    }

    cleanAnswer(value) {
        return value.toLowerCase().replace(/\W+/g, '');
    }

    cleanAnswers(value) {
        return value.map((x) => this.cleanAnswer(x));
    }

    content() {
        let e = document.createElement("meta");
        e.setAttribute("name", "viewport");
        e.setAttribute("content", "width=device-width, initial-scale=1.0");
        document.head.appendChild(e);
        document.title = window.location.pathname.match(/.*\/(.+)\.html/)[1] + " practice";
        e = document.createElement("style");
        e.textContent = `
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 0;
                margin: 0;
            }
            .content {
                font-size: 40px;
                font-weight: bold;
                margin: auto;
            }
            input {
                padding: 10px;
                font-size: 16px;
                margin: 0;
            }
            #feedback {
                padding-top: 10px;
                font-size: 18px;
                font-weight: normal;
                width: 200px;
                word-wrap: break-word;
                margin: auto;
            }
        `;
        document.head.appendChild(e);
        document.body.innerHTML = `
            <div class="content">
                <div id="prompt"></div>
                <form id="form">
                    <input type="text" id="answer" placeholder="Answer">
                </form>
                <div id="feedback"></div>
            </div>
        `;
    }

    init() {
        this.content()
        this.el = Object.fromEntries(
            ["answer", "feedback", "prompt"].map((x) => [x, document.getElementById(x)]),
        );
        document.getElementById("form").addEventListener(
            "submit", (event) => {
                event.preventDefault();
                this.checkAnswer(true);
            },
        );
        this.el.answer.addEventListener(
            "input", (event) => {
                this.checkAnswer(false)
            },
        );
        this.shiftAnswer(true);
    }

    showFeedback(feedback) {
        this.el.feedback.innerText = feedback;
    }

    shiftAnswer(isFirstTime) {
        this.el.answer.value = "";
        if (isFirstTime) {
            this.showFeedback("Answers are checked as you enter them or when you press enter. Type '?' to get the correct answer.");
        }
        else if (++this.currentIndex >= this.shuffled.length) {
            this.shuffle();
            this.currentIndex = 0;
            this.showFeedback("You have completed the set! Restarting...");
        }
        else {
            this.showFeedback("Correct!");
        }
        this.currentQuestion = this.shuffled[this.currentIndex];
        this.promptIndex = 0;
        this.shiftPrompt();
    }

    shiftPrompt() {
        if ( this.promptTimeout ) {
            clearTimeout(this.promptTimeout);
            this.promptTimeout = null;
        }
        if ( this.promptIndex < this.currentQuestion.prompt.length ) {
            this.el.prompt.innerText = this.currentQuestion.splitPrompt.slice(0, ++this.promptIndex).join("/");
            this.promptTimeout = setTimeout(() => {this.shiftPrompt()}, 3000);
        }
    }

    shuffle(questions) {
        let rv = questions || this.shuffled;
        for (let i = rv.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [rv[i], rv[j]] = [rv[j], rv[i]];
        }
        return rv;
    }

    split(value) {
        return value.split(/\s*\/\s*/);
    }

}
