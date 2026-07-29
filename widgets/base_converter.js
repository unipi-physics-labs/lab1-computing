// widgets/base.js

export class BaseConverter {
    constructor(parent, options = {}) {
        if (!(parent instanceof Element)) {
            throw new TypeError("parent must be a DOM element");
        }

        this.parent = parent;
        this.inputBase = options.inputBase ?? 10;
        this.outputBase = options.outputBase ?? 2;
        this.inputLabel = options.inputLabel ?? `Base ${this.inputBase}`;
        this.outputLabel = options.outputLabel ?? `Base ${this.outputBase}`;
        this.initialValue = options.initialValue ?? "";

        this.validateBase(this.inputBase);
        this.validateBase(this.outputBase);

        this.render();
    }

    render() {
        this.root = document.createElement("div");
        this.root.className = "base-converter";

        this.input = document.createElement("input");
        this.input.type = "text";
        this.input.className = "base-converter-input";
        this.input.value = this.initialValue;
        this.input.autocomplete = "off";
        this.input.spellcheck = false;
        this.input.inputMode = "text";
        this.input.setAttribute(
            "aria-label",
            `${this.inputLabel} number`
        );

        this.output = document.createElement("code");
        this.output.className = "base-converter-output";
        this.output.setAttribute("aria-live", "polite");

        this.root.append(
            this.label(this.inputLabel),
            this.input,
            this.arrow(),
            this.label(this.outputLabel),
            this.output
        );

        this.parent.replaceChildren(this.root);

        this.input.addEventListener("input", () => this.update());

        this.update();
    }

    label(text) {
        const span = document.createElement("span");
        span.className = "base-converter-label";
        span.textContent = text;
        return span;
    }

    arrow() {
        const span = document.createElement("span");
        span.className = "base-converter-arrow";
        span.textContent = "→";
        span.setAttribute("aria-hidden", "true");
        return span;
    }

    update() {
        const text = this.input.value.trim();

        if (text === "") {
            this.setOutput("—", false);
            return;
        }

        try {
            const value = this.parseInteger(text, this.inputBase);
            if (this.outputBase == 2) {
                this.setOutput(`0b${value.toString(2)}`, true);
            }
            else {
                this.setOutput(value.toString(this.outputBase), true);
            }
        } catch {
            this.setOutput("Invalid input", false);
        }
    }

    setOutput(text, valid) {
        this.output.textContent = text;
        this.output.classList.toggle("invalid", !valid);
    }

    parseInteger(text, base) {
        const match = text.match(/^([+-]?)([0-9a-z]+)$/i);

        if (!match) {
            throw new Error("Invalid integer");
        }

        const sign = match[1] === "-" ? -1n : 1n;
        const digits = match[2].toLowerCase();

        let value = 0n;
        const bigBase = BigInt(base);

        for (const character of digits) {
            const digit = this.digitValue(character);

            if (digit >= base) {
                throw new Error(
                    `Digit ${character} is invalid in base ${base}`
                );
            }

            value = value * bigBase + BigInt(digit);
        }

        return sign * value;
    }

    digitValue(character) {
        const code = character.codePointAt(0);

        if (code >= 48 && code <= 57) {
            return code - 48;
        }

        if (code >= 97 && code <= 122) {
            return code - 97 + 10;
        }

        throw new Error("Invalid digit");
    }

    validateBase(base) {
        if (!Number.isInteger(base) || base < 2 || base > 36) {
            throw new RangeError("Bases must be integers from 2 to 36");
        }
    }
}