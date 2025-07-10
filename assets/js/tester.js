// Copyright (c) 2025 Robert Nagler.  All Rights Reserved.
// License: http://www.apache.org/licenses/LICENSE-2.0.html
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
        this.MODE = Object.freeze({first: 1, correct: 2, skip: 3});
        document.addEventListener("DOMContentLoaded", () => this.init());
    }

    checkAnswer(isEnter) {
        const a = this.showHelp();
        if (! a) {
            return
        }
        a = this.cleanAnswer(a);
        if (this.currentQuestion.cleaned.includes(a)) {
            this.shiftAnswer(this.MODE.correct);
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
        this.shiftAnswer(this.MODE.first);
    }

    showFeedback(feedback) {
        this.el.feedback.innerText = feedback;
    }

    showHelp() {
        if (this.promptTimeout) {
            clearTimeout(this.promptTimeout);
            this.promptTimeout = null;
        }
        const SKIP_PREFIX = "Enter answer '";
        const skipped = this.el.feedback.innerText.includes(SKIP_PREFIX);
        this.showFeedback("");
        let a = this.el.answer.value;
        if (! a.includes(".")) {
            return a;
        }
        this.el.answer.value = a.replace(".", "");
        if (this.shiftPrompt()) {
            return;
        }
        if (skipped) {
            this.shiftAnswer(this.MODE.skip);
        }
        else {
            this.showFeedback(SKIP_PREFIX + this.currentQuestion.answer + "' to continue")
        }
        return null;
    }

    shiftAnswer(mode) {
        this.el.answer.value = "";
        if (mode === this.MODE.first) {
            this.showFeedback("Answers are checked as you enter them or when you press enter. Type '.' to get progressive hints.");
        }
        else if (++this.currentIndex >= this.shuffled.length) {
            this.shuffle();
            this.currentIndex = 0;
            this.showFeedback("You have completed the set! Restarting...");
        }
        else {
            this.showFeedback(mode === this.MODE.correct ? "Correct!" : "skipped");
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
        console.log(this.promptIndex);
        if ( this.promptIndex < this.currentQuestion.splitPrompt.length ) {
            this.el.prompt.innerText = this.currentQuestion.splitPrompt.slice(0, ++this.promptIndex).join("/");
            // this.promptTimeout = setTimeout(() => {this.shiftPrompt()}, 3000);
            return true;
        }
        return false;
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
