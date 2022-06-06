const heroHeading = document.querySelector('.hero__heading')
const heroText = document.querySelector('.hero__text')

function setHeroMargins(){
    let margin = heroHeading.offsetHeight / 1.5
    let marginBig = margin * 2
    if (margin < 16) {
        margin = 16
    }
    heroHeading.style.margin = `${margin}px 0`;
    heroText.style.margin = `${marginBig}px 0`;
    console.log(margin)
}

document.addEventListener('DOMContentLoaded', setHeroMargins)
window.addEventListener('resize', setHeroMargins)