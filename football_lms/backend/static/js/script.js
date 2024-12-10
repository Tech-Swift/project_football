document.addEventListener("scroll", function () {
    const header = document.querySelector(".site-header");
    const scrollTop = document.querySelector(".scroll-top");
    if (window.scrollY > 50) {
        header.classList.add("scrolled");
        scrollTop.style.display = "block";
    } else {
        header.classList.remove("scrolled");
        scrollTop.style.display = "none";
    }
});
