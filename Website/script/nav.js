var close = true;
/***
 * Responsive navigation bar
 */
const navSlide = () => {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.nav-links');
    const navLinks = document.querySelectorAll('.nav-links li');


    burger.addEventListener('click', () => {
        //Toggle Nav
        nav.classList.toggle('nav-active');

        //Burger animation
        burger.classList.toggle('toggle');
        if (close) {
            burger.style.animation = `burgerMoveOpen forwards 1.1s`;
            close = false;
        } else {
            burger.style.animation = `burgerMoveClose backwards 1.1s`;
            close = true;
        }


        //Animate Links
        navLinks.forEach((link, index) => {
            if (link.style.animation) {
                link.style.animation = "";
            } else {
                link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.5}s`;
            }

        });
    });
}

const app = () => {
    navSlide();
}

app(); 