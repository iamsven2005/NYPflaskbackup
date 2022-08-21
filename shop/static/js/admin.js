const sideLol = document.querySelector("aside");
const hamBtn = document.querySelector("#ham-btn");
const noBtn = document.querySelector("#no-btn");
const dark = document.querySelector(".dark");

hamBtn.addEventListener('click', () => {
    sideLol.style.display = 'block';
})
noBtn.addEventListener('click', () => {
    sideLol.style.display = 'none';
})
dark.addEventListener('click', () => {
    document.body.classList.toggle('theme');
    dark.querySelector('span:nth-child(1)').classList.toggle('active');
    dark.querySelector('span:nth-child(2)').classList.toggle('active');
})
