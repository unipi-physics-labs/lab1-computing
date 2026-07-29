// widgets/base.js

export class BaseConverter {

    constructor(parent, options) {
        this.parent = parent;

        this.fromBase = options.fromBase;
        this.toBase   = options.toBase;

        this.fromLabel = options.fromLabel;
        this.toLabel   = options.toLabel;

        this.render();
    }

    render() {

        this.root = document.createElement("div");
        this.root.className = "base-converter";

        this.input = document.createElement("input");
        this.input.type = "text";
        this.input.className = "base-converter-input";

        this.output = document.createElement("span");
        this.output.className = "base-converter-output";

        this.root.append(
            this.label(this.fromLabel),
            this.input,
            this.arrow(),
            this.label(this.toLabel),
            this.output
        );

        this.parent.appendChild(this.root);

        this.input.addEventListener(
            "input",
            () => this.update()
        );

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
        return span;
    }

    update() {

        const text = this.input.value.trim();

        try {

            const value =
                BigInt(parseInt(text, this.fromBase));

            this.output.textContent =
                value.toString(this.toBase);

            this.output.classList.remove("invalid");
        }

        catch {

            this.output.textContent = "—";
            this.output.classList.add("invalid");
        }
    }

}