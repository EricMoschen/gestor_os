function autoResize(el) {
    const lineHeight = 16; // ajuste conforme seu CSS
    const maxHeight = lineHeight * 5;

    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, maxHeight) + "px";
}