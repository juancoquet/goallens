const menuBtn = document.querySelector('.nav__menu');
const menuClose = document.querySelector('.nav__menu-close');
const navItems = document.querySelectorAll('.nav__item');
const menu = document.querySelector('.mobile-menu');
const navRight = document.querySelector('.nav-items--right');

menuBtn.addEventListener('click', openMenu);
menuClose.addEventListener('click', closeMenu);

async function openMenu() {
    menuBtn.classList.toggle('hidden');
    menuClose.classList.toggle('hidden');

    navItems.forEach(item => {
        menu.appendChild(item);
        item.style.display = 'block';
    });

    menu.classList.remove('hidden');

}

async function closeMenu() {
    menuBtn.classList.toggle('hidden');
    menuClose.classList.toggle('hidden');
    menu.classList.add('hidden')
    await sleep(0.25);

    navItems.forEach(item => {
        navRight.appendChild(item);
        item.style.display = 'none';   
    });
}

window.addEventListener('resize', calculateMenu);

function calculateMenu() {
    if (window.innerWidth > 485) {
        navItems.forEach(item => {
            navRight.appendChild(item);
            item.style.display = 'block';
        });
    } else {
        navItems.forEach(item => {
            menu.appendChild(item);
            item.style.display = 'none';
        });
    }
    menuClose.classList.add('hidden');
    menuBtn.classList.remove('hidden');
}