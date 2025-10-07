document.addEventListener("DOMContentLoaded", () => {
    const select = document.getElementById("page-select");
    select.addEventListener("change", () => {
        const page = select.value;
        const params = new URLSearchParams(window.location.search);
        params.set("page", page);
        window.location.search = params.toString();
    });
});
