export class Tester {
    constructor(questions) {
        this.shuffled = this.shuffle(
            questions.map(
                (x) => {
                    return {question: x[0], answer: x[1], cleaned: this.cleanAnswer(x[1])};
                },
            ),
        );
        this.timeout = null;
        this.current = 0;
        document.addEventListener("DOMContentLoaded", () => this.init());
    }

    checkAnswer(isEnter) {
        let a = this.cleanAnswer(this.el.answer.value);
        if (a.includes("?")) {
            this.el.feedback.innerText = "Enter romaji '" + this.shuffled[this.current].answer + "' to continue";
            return;
        }
        if (a === this.shuffled[this.current].cleaned) {
            const t = this.updateCharacter(false);
            this.el.answer.value = "";
            if (this.timeout) {
                clearTimeout(this.timeout);
            }
            this.timeout = setTimeout(() => {this.el.feedback.innerText = "";}, t);
        } else if (isEnter) {
            this.el.feedback.innerText = `Incorrect. Try again.`;
        }
    }

    cleanAnswer(value) {
        return value.toLowerCase().replace(/\s+/g, '');
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
                padding: 20px;
            }
            #character {
                font-size: 40px;
                font-weight: bold;
                margin-bottom: 20px;
            }
            input {
                padding: 10px;
                font-size: 16px;
            }
            button {
                padding: 10px 20px;
                font-size: 16px;
                margin: 10px;
            }
            #feedback {
                font-size: 18px;
                margin-top: 10px;
                width: 200px;
                word-wrap: break-word;
                margin: auto;
            }
        `;
        document.head.appendChild(e);
        document.body.innerHTML = `
            <div id="character"></div>
                <br />
                <form id="practice-form">
                    <input type="text" id="answer" placeholder="Enter romaji">
                </form>
                <br />
                <p id="feedback"></p>
            </div>
        `;
    }

    init() {
        this.content()
        this.el = Object.fromEntries(
            ["answer", "feedback", "character"].map((x) => [x, document.getElementById(x)]),
        );
        document.getElementById("practice-form").addEventListener(
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
        this.updateCharacter(true);
    }

    shuffle(questions) {
        let rv = questions || this.shuffled;
        for (let i = rv.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [rv[i], rv[j]] = [rv[j], rv[i]];
        }
        return rv;
    }

    updateCharacter(isFirstTime) {
        let rv = 500;
        if (isFirstTime) {
            this.el.feedback.innerText = "Answers are checked as you enter them or when you press enter. Type '?' to get the correct answer.";
        }
        else if (++this.current >= this.shuffled.length) {
            this.shuffle();
            this.current = 0;
            this.el.feedback.innerText = "You have completed the set! Restarting...";
            rv *= 2;
        }
        else {
            this.el.feedback.innerText = "Correct!";
        }
        this.el.character.innerText = this.shuffled[this.current].question;
        return rv;
    }
}
